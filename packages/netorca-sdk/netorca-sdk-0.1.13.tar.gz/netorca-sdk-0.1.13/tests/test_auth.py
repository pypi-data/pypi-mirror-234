import unittest
from unittest.mock import patch

from netorca_sdk.auth import NetorcaAuth
from netorca_sdk.exceptions import NetorcaException


class TestNetorcaAuth(unittest.TestCase):
    def setUp(self):
        self.fqdn = "https://example.com"
        self.username = "username"
        self.password = "password"
        self.api_key = "api_key"
        self.url = "https://example.com/test"
        self.data = {"key": "value"}

    @patch("netorca_sdk.auth.requests.post")
    def test_login_with_username_and_password(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"token": "test_token"}

        auth = NetorcaAuth(self.fqdn, username=self.username, password=self.password)
        self.assertEqual(auth.token, "test_token")

    def test_login_with_api_key(self):
        auth = NetorcaAuth(self.fqdn, api_key=self.api_key)
        self.assertEqual(auth.headers["Authorization"], f"Api-Key {self.api_key}")

    @patch("netorca_sdk.auth.requests.post")
    def test_failed_authentication(self, mock_post):
        mock_post.return_value.status_code = 401
        mock_post.return_value.json.return_value = {"detail": "Invalid credentials"}

        with self.assertRaises(NetorcaException):
            NetorcaAuth(self.fqdn, username=self.username, password="wrong_password")

    @patch("netorca_sdk.auth.requests.get")
    def test_get_teams_info(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"results": [{"id": 1, "name": "team1"}]}

        auth = NetorcaAuth(self.fqdn, api_key=self.api_key)
        teams_info = auth.get_teams_info()

        self.assertEqual(teams_info, [{"id": 1, "name": "team1"}])

    @patch("netorca_sdk.auth.requests.get")
    def test_get_teams_info_failure(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"detail": "Internal Server Error"}

        auth = NetorcaAuth(self.fqdn, api_key=self.api_key)

        with self.assertRaises(NetorcaException):
            auth.get_teams_info()

    def test_init_missing_credentials(self):
        with self.assertRaises(NetorcaException):
            NetorcaAuth(self.fqdn)

    @patch("netorca_sdk.auth.requests.get")
    def test_get(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test_data"}

        auth = NetorcaAuth(self.fqdn, api_key=self.api_key)
        response = auth.get(url=self.url)

        self.assertEqual(response.json(), {"data": "test_data"})

    @patch("netorca_sdk.auth.requests.post")
    def test_post(self, mock_post):
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"data": "test_data"}

        auth = NetorcaAuth(self.fqdn, api_key=self.api_key)
        response = auth.post(url=self.url, data=self.data)

        self.assertEqual(response.json(), {"data": "test_data"})

    @patch("netorca_sdk.auth.requests.put")
    def test_put(self, mock_put):
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"data": "test_data"}

        auth = NetorcaAuth(self.fqdn, api_key=self.api_key)
        response = auth.put(url=self.url, data=self.data)

        self.assertEqual(response.json(), {"data": "test_data"})

    @patch("netorca_sdk.auth.requests.patch")
    def test_patch(self, mock_patch):
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = {"data": "test_data"}

        auth = NetorcaAuth(self.fqdn, api_key=self.api_key)
        response = auth.patch(url=self.url, data=self.data)

        self.assertEqual(response.json(), {"data": "test_data"})


if __name__ == "__main__":
    unittest.main()
