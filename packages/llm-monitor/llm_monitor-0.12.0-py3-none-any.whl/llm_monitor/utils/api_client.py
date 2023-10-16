from os import getenv
from time import time
from typing import Any, Callable, Dict, Optional, Union

import jwt
from pydantic import UUID4
from requests import get, post

from llm_monitor.constants.routes import Routes
from llm_monitor.schema.transaction import TransactionRecordBatch
from llm_monitor.utils.request import HttpHeaders, make_request


class ApiClient:
    def __init__(self, project_name: str):
        self.project_id = None
        self.api_url = self.get_api_url()
        if self.healthcheck():
            self.token = self.get_token()
            self.project_id = self.get_project_id_by_name(project_name)

    def get_api_url(self) -> str:
        console_url = getenv("GALILEO_CONSOLE_URL")
        if console_url is None:
            raise Exception("GALILEO_CONSOLE_URL must be set")
        if any(map(console_url.__contains__, ["localhost", "127.0.0.1"])):
            api_url = "http://localhost:8088"
        else:
            api_url = console_url.replace("console", "api")
        return api_url

    def get_token(self) -> str:
        username = getenv("GALILEO_USERNAME")
        password = getenv("GALILEO_PASSWORD")
        if username is None or password is None:
            raise Exception("GALILEO_USERNAME and GALILEO_PASSWORD must be set")
        return self.username_login(username, password).get("access_token", "")

    def healthcheck(self) -> bool:
        make_request(get, base_url=self.base_url, endpoint=Routes.healthcheck)
        return True

    def username_login(self, username: str, password: str) -> Dict[str, str]:
        return make_request(
            post,
            base_url=self.base_url,
            endpoint=Routes.login,
            data={
                "username": username,
                "password": password,
                "auth_method": "email",
            },
        )

    @property
    def base_url(self) -> str:
        return self.api_url

    @property
    def auth_header(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def _make_request(
        self,
        request_method: Callable,
        endpoint: str,
        body: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        timeout: Union[int, None] = None,
        json_request_only: bool = False,
    ) -> Any:
        # Check to see if our token is expired before making a request
        # and refresh token if it's expired
        if endpoint is not Routes.login and self.token:
            claims = jwt.decode(self.token, options={"verify_signature": False})
            if claims.get("exp", 0) < time():
                self.token = self.get_token()

        if json_request_only:
            content_headers = HttpHeaders.accept_json()
        else:
            content_headers = HttpHeaders.json()
        headers = {**self.auth_header, **content_headers}
        return make_request(
            request_method=request_method,
            base_url=self.base_url,
            endpoint=endpoint,
            body=body,
            data=data,
            files=files,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    def ingest_batch(self, transaction_batch: TransactionRecordBatch) -> Dict[str, str]:
        return self._make_request(
            post,
            endpoint=Routes.ingest.format(project_id=self.project_id),
            body=transaction_batch.dict(),
        )

    def get_project_id_by_name(self, project_name: str) -> UUID4:
        projects = self._make_request(
            get,
            endpoint=Routes.projects,
            params={"project_name": project_name, "type": "llm_monitor"},
        )
        if len(projects) < 1:
            raise Exception({"msg": "Galileo project {project_name} not found"})
        return projects[0]["id"]
