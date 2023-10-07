import asyncio
import json
import logging
import os
import sys
import types
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Any, AsyncIterator, List, Optional, Type, TypeVar, Union
from urllib.parse import urlparse

import aiofiles
import aiohttp
import jwt
from aiohttp_retry import RetryClient, ExponentialRetry
from strong_typing.serialization import json_dump_string, json_to_object, object_to_json

from . import __version__
from .dap_error import (
    AccountDisabledError,
    AccountNotOnboardedError,
    AuthenticationError,
    NotFoundError,
    OutOfRangeError,
    ProcessingError,
    ServerError,
    SnapshotRequiredError,
    ValidationError,
)
from .dap_types import (
    CompleteIncrementalJob,
    CompleteSnapshotJob,
    Credentials,
    DownloadTableDataResult,
    GetTableDataResult,
    IncrementalQuery,
    Job,
    JobID,
    JobStatus,
    Object,
    Query,
    Resource,
    ResourceResult,
    SnapshotQuery,
    TableList,
    TokenProperties,
    VersionedSchema,
)
from .networking import KeepAliveClientRequest, get_content_type

logger = logging.getLogger("dap")

T = TypeVar("T")

# prevent "RuntimeError: Event loop is closed" on Windows platforms
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class DAPClientError(RuntimeError):
    pass


REQUEST_RETRY_COUNT = 3


class DAPClient:
    """
    Client proxy for the Data Access Platform (DAP) server-side API.

    In order to invoke high-level functionality such as initializing and synchronizing a database or data warehouse, or
    low-level functionality such as triggering a snapshot or incremental query, you need to instantiate a client, which
    acts as a proxy to DAP API.
    """

    _base_url: str
    _credentials: Credentials
    _session: Optional["DAPSession"]

    def __init__(
        self,
        base_url: Optional[str] = None,
        credentials: Optional[Credentials] = None,
    ) -> None:
        "Initializes a new client proxy to communicate with the DAP back-end."

        if base_url is None:
            base_url = os.getenv("DAP_API_URL")
            if not base_url:
                raise DAPClientError("missing base URL")

        if credentials is None:
            client_id = os.getenv("DAP_CLIENT_ID")
            client_secret = os.getenv("DAP_CLIENT_SECRET")
            if not client_id or not client_secret:
                raise DAPClientError("missing credentials")

            credentials = Credentials.create(
                client_id=client_id, client_secret=client_secret
            )

        self._base_url = base_url.rstrip("/")
        self._credentials = credentials

        logger.debug(f"Client region: {self._credentials.client_region}")

    async def __aenter__(self) -> "DAPSession":
        "Initiates a new client session."

        session = aiohttp.ClientSession(
            headers={"User-Agent": f"DataAccessPlatform/{__version__}"},
            timeout=aiohttp.ClientTimeout(total=30 * 60, connect=30),
            request_class=KeepAliveClientRequest,
        )
        self._session = DAPSession(session, self._base_url, self._credentials)
        return self._session

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[types.TracebackType],
    ) -> None:
        "Terminates a client session."

        if self._session is not None:
            await self._session.close()
            self._session = None


class AccessToken:
    """
    A JWT access token. This object is immutable.

    The access token counts as sensitive information not to be exposed (e.g. in logs).
    """

    _token: str
    _expiry: datetime

    def __init__(self, jwt_token: str) -> None:
        "Creates a new JWT access token."

        self._token = jwt_token
        decoded_jwt = jwt.decode(jwt_token, options={"verify_signature": False})
        expiry = int(decoded_jwt["exp"])
        self._expiry = datetime.fromtimestamp(expiry, tz=timezone.utc)

    def __str__(self) -> str:
        "Returns the string representation of the JWT access token."

        return self._token

    def is_expiring(self) -> bool:
        """
        Checks if the token is about to expire.

        :returns: True if the token is about to expire.
        """

        latest_accepted_expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=5)
        return self._expiry < latest_accepted_expiry


class DAPSession:
    """
    Represents an authenticated session to DAP.
    """

    _base_url: str
    _session: aiohttp.ClientSession
    _credentials: Credentials
    _access_token: Optional[AccessToken] = None
    _retry_client: RetryClient

    def __init__(
        self, session: aiohttp.ClientSession, base_url: str, credentials: Credentials
    ) -> None:
        """
        Creates a new logical session by encapsulating a network connection.
        """

        self._base_url = base_url
        self._session = session
        self._credentials = credentials
        self._retry_client = RetryClient(
            client_session=self._session,
            retry_options=ExponentialRetry(attempts=REQUEST_RETRY_COUNT)
        )

    async def close(self) -> None:
        """
        Closes the underlying network socket.
        """

        await self._session.close()

    async def _get(self, path: str, response_type: Type[T]) -> T:
        """
        Sends a request to the server and parses the response into the expected type.

        :param path: The path component of the endpoint to invoke.
        :param response_type: The object type the endpoint returns on success.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        await self.authenticate()
        async with self._retry_client.get(f"{self._base_url}{path}") as response:
            return await self._process(response, response_type)

    def _map_to_error_type(
        self, status_code: int, response_body: Any
    ) -> Union[
        ValidationError,
        NotFoundError,
        OutOfRangeError,
        SnapshotRequiredError,
        AuthenticationError,
        AccountDisabledError,
        AccountNotOnboardedError,
        ProcessingError,
        ServerError,
    ]:
        """
        Maps error body and status to Python error object.
        """

        if "error" not in response_body:
            return ServerError(response_body)

        response_body_error = response_body["error"]
        try:
            if status_code == HTTPStatus.UNAUTHORIZED.value:
                return json_to_object(AuthenticationError, response_body_error)
            elif status_code == HTTPStatus.FORBIDDEN.value:
                return json_to_object(
                    Union[AccountDisabledError, AccountNotOnboardedError],
                    response_body_error,
                )
            else:
                return json_to_object(
                    Union[
                        ValidationError,
                        NotFoundError,
                        OutOfRangeError,
                        SnapshotRequiredError,
                        ProcessingError,
                    ],
                    response_body_error,
                )
        except:
            return ServerError(response_body_error)

    async def _post(self, path: str, request_data: Any, response_type: Type[T]) -> T:
        """
        Sends a request to the server by serializing a payload object, and parses the response into the expected type.

        :param path: The path component of the endpoint to invoke.
        :param request_data: The object to pass in the request body.
        :param response_type: The object type the endpoint returns on success.
        :returns: The object returned on success.
        :raises Exception: The object returned on failure.
        """

        await self.authenticate()

        request_payload = object_to_json(request_data)
        logger.debug(f"POST request payload:\n{repr(request_payload)}")

        async with self._session.post(
            f"{self._base_url}{path}",
            data=json_dump_string(request_payload),
            headers={"Content-Type": "application/json"},
        ) as response:
            return await self._process(response, response_type)

    async def _post_auth_request(self, basic_credentials: str) -> TokenProperties:
        """
        Sends an authentication request to the Identity Service through Instructure API Gateway,
        and parses the response into a TokenProperties object.

        :param basic_credentials: Basic credentials.
        :returns: An access token and metadata.
        :raises Exception: The object returned on failure.
        """

        async with self._session.post(
            f"{self._base_url}/ids/auth/login",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": "Basic " + basic_credentials},
        ) as response:
            return await self._process(response, TokenProperties, suppress_output=True)

    async def _process(
        self,
        response: aiohttp.ClientResponse,
        response_type: Type[T],
        suppress_output: bool = False,
    ) -> T:
        """
        Extracts an object instance from an HTTP response body.
        """

        content_type = get_content_type(response.headers.get("Content-Type", ""))
        if content_type == "application/json":
            response_payload = await response.json()
        else:
            response_text = await response.text()
            if response_text:
                logger.error(f"malformed HTTP response:\n{response_text}")

            raise DAPClientError("malformed HTTP response")

        if not suppress_output:
            logger.debug(f"GET/POST response payload:\n{repr(response_payload)}")

        # HTTP status codes between 400 (inclusive) and 600 (exclusive) indicate an error
        # (includes non-standard 5xx server-side error codes)
        if HTTPStatus.BAD_REQUEST.value <= response.status < 600:
            error_object = self._map_to_error_type(response.status, response_payload)
            logger.warning(f"Received error in response: {error_object}")
            raise error_object
        else:
            response_object = json_to_object(response_type, response_payload)
            return response_object

    async def authenticate(self) -> None:
        """
        Authenticates with API key to receive a JWT.
        """

        if self._access_token is not None and not self._access_token.is_expiring():
            return

        logger.debug(
            f"Authenticating to DAP in region {self._credentials.client_region}"
        )

        # drop expired auth header, re-authentication will set new one
        self._session.headers.pop("X-InstAuth", None)

        properties = await self._post_auth_request(self._credentials.basic_credentials)
        self._access_token = AccessToken(properties.access_token)
        self._session.headers.update({"X-InstAuth": str(self._access_token)})

    async def query_snapshot(
        self, namespace: str, table: str, query: SnapshotQuery
    ) -> Job:
        """
        Starts a snapshot query.
        """

        logger.debug(f"Query snapshot of table: {table}")
        job = await self._post(f"/dap/query/{namespace}/table/{table}/data", query, Job)  # type: ignore
        return job

    async def query_incremental(
        self, namespace: str, table: str, query: IncrementalQuery
    ) -> Job:
        """
        Starts an incremental query.
        """

        logger.debug(f"Query updates for table: {table}")
        job = await self._post(f"/dap/query/{namespace}/table/{table}/data", query, Job)  # type: ignore
        return job

    async def get_tables(self, namespace: str) -> List[str]:
        """
        Retrieves the list of tables available for querying.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :returns: A list of tables available for querying in the given namespace.
        """

        logger.debug(f"Get list of tables from namespace: {namespace}")
        table_list = await self._get(f"/dap/query/{namespace}/table", TableList)
        return table_list.tables

    async def get_table_schema(self, namespace: str, table: str) -> VersionedSchema:
        """
        Retrieves the versioned schema of a table.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :returns: The schema of the table as exposed by DAP API.
        """

        logger.debug(f"Get schema of table: {table}")
        versioned_schema = await self._get(
            f"/dap/query/{namespace}/table/{table}/schema", VersionedSchema
        )
        return versioned_schema

    async def download_table_schema(
        self, namespace: str, table: str, output_directory: str
    ) -> None:
        """
        Saves the schema as a JSON file into a local directory.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :param output_directory: Path to the directory to save the JSON file to.
        """

        versioned_schema = await self.get_table_schema(namespace, table)
        schema_version = versioned_schema.version
        json_object = object_to_json(versioned_schema)

        os.makedirs(output_directory, exist_ok=True)
        file_name = f"{table}_schema_version_{schema_version}.json"
        file_path = os.path.join(output_directory, file_name)
        with open(file_path, "w") as file:
            json.dump(json_object, file, indent=4)
        logger.info(f"JSON schema downloaded to folder: {output_directory}")

    async def get_job(self, job_id: JobID) -> Job:
        """
        Retrieve job status.
        """

        logger.debug(f"Retrieving job state for job {job_id}")
        job = await self._get(f"/dap/job/{job_id}", Job)  # type: ignore
        return job

    async def get_job_status(self, job_id: JobID) -> JobStatus:
        """
        Retrieve job status.
        """

        job = await self.get_job(job_id)
        return job.status

    async def get_objects(self, job_id: JobID) -> List[Object]:
        """
        Retrieve object IDs once the query is completed successfully.
        """

        logger.debug(f"Retrieving object IDs for job {job_id}")
        job = await self._get(f"/dap/job/{job_id}", Job)  # type: ignore
        return job.objects

    async def get_resources(self, objects: List[Object]) -> List[Resource]:
        """
        Retrieve URLs to data stored remotely.
        """

        logger.debug("Retrieve resource URLs for objects:")
        logger.debug([o.id for o in objects])

        response = await self._post("/dap/object/url", objects, ResourceResult)
        resource_list = [response.urls[resource_id] for resource_id in response.urls]
        return resource_list

    async def download_resources(
        self, resources: List[Resource], output_directory: str
    ) -> List[str]:
        """
        Save data stored remotely into a local directory.

        :param resources: List of output resources to be downloaded.
        :param output_directory: Path to the target directory to save downloaded files to.
        :returns: A list of paths to files saved in the local file system.
        """

        local_files: List[str] = []
        os.makedirs(output_directory, exist_ok=True)
        for resource in resources:
            url = str(resource.url)
            url_path = urlparse(url).path
            file_base_name = os.path.basename(url_path)
            file_path = os.path.join(output_directory, file_base_name)
            logger.debug(f"Downloading: {url} to {file_path}")

            async with self.stream_resource(resource) as stream:
                async with aiofiles.open(file_path, "wb") as file:
                    # save gzip data to file without decompressing
                    async for chunk in stream.iter_chunked(64 * 1024):
                        await file.write(chunk)

                logger.debug(f"Download complete of {url} to {file_path}")

            local_files.append(file_path)
        logger.info(f"Files from server downloaded to folder: {output_directory}")
        return local_files

    @asynccontextmanager
    async def stream_resource(
        self, resource: Resource
    ) -> AsyncIterator[aiohttp.StreamReader]:
        """
        Creates a stream reader for the given resource.

        :param resource: Resource to download.
        :yields: An object that can be used with an asynchronous context manager.
        :raises DownloadError: Raised when the host returns an HTTP error response, and rejects the request.
        """

        async with self._retry_client.get(str(resource.url)) as response:
            if not response.ok:
                raise DownloadError(f"HTTP status: {response.status}")

            yield response.content

    async def await_job(self, job: Job) -> Job:
        """
        Wait until a job terminates.

        :param job: A job that might be still running.
        :returns: A job that has completed with success or terminated with failure.
        """

        while not job.status.isTerminal():
            delay = 5
            logger.info(
                f"Query job still in status: {job.status.value}. Checking again in {delay} seconds..."
            )
            await asyncio.sleep(delay)

            job = await self.get_job(job.id)

        logger.debug(f"Query job finished with status: {job.status.value}")
        return job

    async def execute_job(
        self,
        namespace: str,
        table: str,
        query: Query,
    ) -> Job:
        """
        Start a query job and wait until it terminates.
        """

        if isinstance(query, SnapshotQuery):
            job = await self.query_snapshot(namespace, table, query)
        elif isinstance(query, IncrementalQuery):
            job = await self.query_incremental(namespace, table, query)
        else:
            raise TypeError(f"type mismatch for parameter `query`: {type(query)}")

        logger.info(f"Query started with job ID: {job.id}")

        job = await self.await_job(job)
        return job

    async def download_table_data(
        self, namespace: str, table: str, query: Query, output_directory: str
    ) -> DownloadTableDataResult:
        """
        Executes a query job and downloads data to a local directory.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :param query: An object that encapsulates the parameters of the snapshot or incremental query to execute.
        :param output_directory: Path to the directory to save downloaded files to.
        :returns: Result of the query, including a list of paths to files saved in the local file system.
        :raises DAPClientError: Raised when the query returned an error or fetching data has failed.
        """

        # fail early if output directory does not exist and cannot be created
        os.makedirs(output_directory, exist_ok=True)

        job = await self.execute_job(namespace, table, query)

        if job.status is not JobStatus.Complete:
            raise DAPClientError(f"query job ended with status: {job.status.value}")

        objects = await self.get_objects(job.id)
        downloaded_files = []
        for object in objects:
            resources = await self.get_resources([object])
            dir = os.path.join(output_directory, f"job_{job.id}")
            downloaded_files.extend(await self.download_resources(resources, dir))

        if isinstance(job, CompleteSnapshotJob):
            logger.info(
                f"Snapshot query results have been successfully retrieved:\n{job.json()}"
            )
            return DownloadTableDataResult(
                job.schema_version, job.at, job.id, downloaded_files
            )
        elif isinstance(job, CompleteIncrementalJob):
            logger.info(
                f"Incremental query results have been successfully retrieved:\n{job.json()}"
            )
            return DownloadTableDataResult(
                job.schema_version, job.until, job.id, downloaded_files
            )
        else:
            raise DAPClientError(f"unexpected job type: {type(job)}")

    async def get_table_data(
        self, namespace: str, table: str, query: Query
    ) -> GetTableDataResult:
        """
        Executes a query job on a given table.

        :param namespace: A namespace identifier such as `canvas` or `mastery`.
        :param table: A table identifier such as `submissions`, `quizzes`, or `users`.
        :param query: An object that encapsulates the parameters of the snapshot or incremental query to execute.
        :returns: Result of the query, including metadata.
        :raises DAPClientError: Raised when the query returned an error or fetching data has failed.
        """

        job = await self.execute_job(namespace, table, query)

        if job.status is JobStatus.Complete:
            objects = await self.get_objects(job.id)

            if isinstance(job, CompleteSnapshotJob):
                logger.info(f"Data has been successfully retrieved:\n{job.json()}")
                return GetTableDataResult(job.schema_version, job.at, job.id, objects)

            elif isinstance(job, CompleteIncrementalJob):
                logger.info(f"Data has been successfully retrieved:\n{job.json()}")
                return GetTableDataResult(
                    job.schema_version, job.until, job.id, objects
                )

            else:
                raise DAPClientError(f"unexpected job type: {type(job)}")

        else:
            raise DAPClientError(f"query job ended with status: {job.status.value}")


class DownloadError(DAPClientError):
    def __init__(self, response_str: str) -> None:
        super().__init__(f"download error: {response_str}")
