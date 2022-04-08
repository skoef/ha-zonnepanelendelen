"""Zonnepanelendelen API client"""
import requests
import json

ZPD_API_HOST = "mijnstroom.zonnepanelendelen.nl"
ZPD_API_PREFIX = "/api/v1"
ZPD_AUTH_HEADER = "Authorization"


class AuthenticationError(Exception):
    pass


class API:
    """Zonnepanelendelen API client"""

    auth_token: str
    username: str
    password: str

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def _get_url(path):
        if not path.startswith("/"):
            path = "/" + path
        return "https://%s%s" % (ZPD_API_HOST, ZPD_API_PREFIX) + path

    def _get_headers(self):
        return {ZPD_AUTH_HEADER: "Token %s" % self.auth_token}

    def _check_login(self):
        if self.auth_token == "":
            raise Exception("API not logged in")

    def projects(self):
        """Get all projects from API"""

        self._check_login()

        resp = requests.get(
            API._get_url("/projects/?view=index_only"), headers=self._get_headers()
        )
        if resp.status_code != 200:
            raise Exception(resp.text)

        return json.loads(resp.text)

    def project(self, project_id: int):
        """Get details of all specific project"""

        self._check_login()

        url = API._get_url("/project/%d" % project_id)
        resp = requests.get(url, headers=self._get_headers())
        if resp.status_code != 200:
            raise Exception(resp.text)

        return json.loads(resp.text)

    def login(self) -> None:
        """Login to the API by obtaining an authorization token"""

        pload = {"username": self.username, "password": self.password}
        resp = requests.post(
            API._get_url("/obtain-auth-token/"),
            data=pload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if resp.status_code != 200:
            raise AuthenticationError(
                "login failed: (%d) %s" % (resp.status_code, resp.text)
            )

        data = json.loads(resp.text)
        self.auth_token = data["token"]
