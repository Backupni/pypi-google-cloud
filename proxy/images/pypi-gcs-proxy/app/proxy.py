from __future__ import annotations

import base64
import binascii
import os
import sys
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Dict, Final, List, Set, Tuple

from asgiref.sync import sync_to_async
from google.auth import compute_engine, default
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request as TransportRequest
from google.cloud.secretmanager import SecretManagerServiceClient
from google.cloud.secretmanager_v1.proto.service_pb2 import AccessSecretVersionResponse
from google.cloud.storage import Blob, Bucket, Client
from starlette.applications import Starlette
from starlette.authentication import AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser, requires
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import HTTPConnection, Request
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from starlette.routing import BaseRoute, Route

STATIC_BUCKET_NAME: Final[str] = os.getenv('STATIC_BUCKET_NAME') or sys.exit('You MUST set STATIC_BUCKET_NAME environment variable.')
PACKAGES_BUCKET_NAME: Final[str] = os.getenv('PACKAGES_BUCKET_NAME') or sys.exit('You MUST set PACKAGES_BUCKET_NAME environment variable.')
TOKEN_NAME: Final[str] = os.getenv('TOKEN_NAME') or sys.exit('You MUST set TOKEN_NAME environment variable (ex. "projects/123/secrets/pypi-token/versions/1").')
EXPIRES_MINUTES: Final[int] = 30

auth_request: TransportRequest = TransportRequest()
credentials, project = default()
storage_client: Client = Client(project, credentials)
STATIC_BUCKET: Final[Bucket] = storage_client.lookup_bucket(STATIC_BUCKET_NAME) or sys.exit('Static website bucket was not found')
PACKAGES_BUCKET: Final[Bucket] = storage_client.lookup_bucket(PACKAGES_BUCKET_NAME) or sys.exit('Packages bucket was not found')
SIGNING_CREDENTIALS: Final[Credentials] = compute_engine.IDTokenCredentials(auth_request, '', service_account_email=credentials.service_account_email)

HEADERS: Final[Dict[str, str]] = {
    'WWW-Authenticate': 'Basic realm="Restricted Area"',
}

NOT_FOUND_RESPONSE: Final[Response] = JSONResponse({'code': int(HTTPStatus.NOT_FOUND), 'message': HTTPStatus.NOT_FOUND.phrase})


@requires('authenticated')
async def html_homepage(request: Request) -> Response:
    blob: Blob = STATIC_BUCKET.blob('index.html')
    if not await sync_to_async(blob.exists)():
        return NOT_FOUND_RESPONSE
    html_content: bytes = await sync_to_async(blob.download_as_string)()
    return HTMLResponse(content=html_content, headers=HEADERS)


@requires('authenticated')
async def html_simple(request: Request) -> Response:
    blob: Blob = STATIC_BUCKET.blob('simple/index.html')
    if not await sync_to_async(blob.exists)():
        return NOT_FOUND_RESPONSE
    html_content: bytes = await sync_to_async(blob.download_as_string)()
    return HTMLResponse(content=html_content, headers=HEADERS)


@requires('authenticated')
async def html_project(request: Request) -> Response:
    project_name: str = request.path_params['project_name']
    blob: Blob = STATIC_BUCKET.blob('simple/{project_name}/index.html'.format(project_name=project_name))
    if not await sync_to_async(blob.exists)():
        return NOT_FOUND_RESPONSE
    html_content: bytes = await sync_to_async(blob.download_as_string)()
    return HTMLResponse(content=html_content, headers=HEADERS)


@requires('authenticated')
async def json_api_project(request: Request) -> Response:
    project_name: str = request.path_params['project_name']
    blob: Blob = STATIC_BUCKET.blob('pypi/{project_name}/json'.format(project_name=project_name))
    if not await sync_to_async(blob.exists)():
        return NOT_FOUND_RESPONSE
    json_content: bytes = await sync_to_async(blob.download_as_string)()
    return Response(content=json_content, headers=HEADERS, media_type='application/json')


@requires('authenticated')
async def whl_file(request: Request) -> Response:
    file_name: str = request.path_params['file_name']
    blob: Blob = PACKAGES_BUCKET.blob('raw/{file_name}.whl'.format(file_name=file_name))
    if not await sync_to_async(blob.exists)():
        return NOT_FOUND_RESPONSE
    expires_at_ms: datetime = datetime.now() + timedelta(minutes=EXPIRES_MINUTES)
    signed_url: str = await sync_to_async(blob.generate_signed_url)(expiration=expires_at_ms, credentials=SIGNING_CREDENTIALS, version='v4')
    return RedirectResponse(url=signed_url, status_code=int(HTTPStatus.TEMPORARY_REDIRECT))


routes: List[BaseRoute] = [
    Route('/', endpoint=html_homepage),
    Route('/simple/', endpoint=html_simple),
    Route('/simple/{project_name}/', endpoint=html_project),
    Route('/pypi/{project_name}/json', endpoint=json_api_project),
    Route('/raw/{file_name}.whl', endpoint=whl_file),
]


class BasicAuthSecretManagerBackend(AuthenticationBackend):
    def __init__(self):
        self.client: SecretManagerServiceClient = SecretManagerServiceClient()

    async def authenticate(self, request: Request) -> Tuple[AuthCredentials, SimpleUser]:
        if 'Authorization' not in request.headers:
            raise AuthenticationError('Please, authenticate')

        auth = request.headers['Authorization']
        try:
            scheme, credentials = auth.split()
        except ValueError:
            raise AuthenticationError('Invalid basic auth credentials')

        if scheme.lower() != 'basic':
            raise AuthenticationError('Please, use basic authentication')

        try:
            decoded = base64.b64decode(credentials).decode('ascii')
        except (binascii.Error, UnicodeDecodeError, ValueError):
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, token = decoded.partition(':')
        if username != '__token__':
            raise AuthenticationError('Incorrect username. Only token are allowed. Please, set username to __token__')

        token_response: AccessSecretVersionResponse = await sync_to_async(self.client.access_secret_version)(TOKEN_NAME)
        token_response_data: str = token_response.payload.data.decode()
        auth_tokens: Set[str] = set(token_response_data.split())

        if token not in auth_tokens:
            raise AuthenticationError('Incorrect token')
        return AuthCredentials(['authenticated']), SimpleUser(username)


def on_error(conn: HTTPConnection, exc: Exception) -> Response:
    return PlainTextResponse(str(exc), headers=HEADERS, status_code=int(HTTPStatus.UNAUTHORIZED))


middleware: List[Middleware] = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthSecretManagerBackend(), on_error=on_error),
]

app: Starlette = Starlette(routes=routes, middleware=middleware)
