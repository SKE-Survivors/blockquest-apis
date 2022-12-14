import json
import unittest
import requests

from handler.database import DatabaseHandler
from handler.session import SessionHandler
from utils.password import encode_pwd


class TestUpdate(unittest.TestCase):

    base_url = "http://localhost:3000"
    headers = {"Content-Type": "application/json"}

    @classmethod
    def setUpClass(self) -> None:
        self.dbh = DatabaseHandler()
        self.dbh.add_user("testemail@email.com", "emailer", encode_pwd("eemail"))

        self.sh = SessionHandler()

        body = {"email": "testemail@email.com", "password": "eemail"}
        resp = requests.post(
            self.base_url + "/api/auth/login",
            data=json.dumps(body),
            headers=self.headers,
        )
        self.login_resp_body = resp.json()

        self.dbh.add_user("emailtoedit@email.com", "emailer", encode_pwd("eemail"))
        test_body = {"email": "emailtoedit@email.com", "password": "eemail"}
        test_resp = requests.post(
            self.base_url + "/api/auth/login",
            data=json.dumps(test_body),
            headers=self.headers,
        )
        self.login_resp_test_body = test_resp.json()

        self.dbh.add_user("emailtodel@email.com", "emailer", encode_pwd("eemail"))
        test_body_to_delete = {"email": "emailtodel@email.com", "password": "eemail"}
        test_resp_to_delete = requests.post(
            self.base_url + "/api/auth/login",
            data=json.dumps(test_body_to_delete),
            headers=self.headers,
        )
        self.login_resp_test_body_to_delete = test_resp_to_delete.json()

        self.dbh.add_user("invalidemail@email.com", "emailer", encode_pwd("eemail"))

    @classmethod
    def tearDownClass(self) -> None:
        self.dbh.delete_user("testemail@email.com")
        self.dbh.delete_user("emailtoedit@email.com")
        self.dbh.delete_user("invalidemail@email.com")

    def assert_checker(self, session_resp, status_code, body_status, body_msg):

        session_resp_body = session_resp.json()
        self.assertEqual(session_resp.status_code, status_code)

        self.assertEqual(session_resp_body["STATUS"], body_status)
        self.assertEqual(session_resp_body["MESSAGE"], body_msg)

    def test_get_user_happy_path(self):
        session_resp = requests.get(
            self.base_url + "/api/user/profile?email=testemail@email.com",
            headers=self.headers,
        )
        self.assertEqual(session_resp.status_code, 201)

        session_resp_body = session_resp.json()
        self.assertEqual(session_resp_body["STATUS"], "SUCCESS")
        self.assertEqual(
            session_resp_body["userInfo"],
            [
                {
                    "email": "testemail@email.com",
                    "username": "emailer",
                    "unlocked_lesson": {"L1": False, "L2": False, "L3": False},
                    "unlocked_story": {"S1": False, "S2": False},
                    "bag": [],
                }
            ],
        )

    def test_user_with_invalid_email(self):
        session_resp = requests.get(
            self.base_url + "/api/user/profile", headers=self.headers
        )
        self.assert_checker(session_resp, 400, "FAILED", "Missing argument: email")

    def test_user_with_non_existing_email(self):
        session_resp = requests.get(
            self.base_url + "/api/user/profile?email=fake.email@email.com",
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "User does not exist")

    def test_edit_user_happy_path(self):
        body = {
            "username": "new_emailer",
            "password": "new+pwd",
            "confirm-password": "new+pwd",
        }
        session_resp = requests.put(
            self.base_url
            + f"/api/user/profile?email=emailtoedit@email.com&token={self.login_resp_test_body['MESSAGE']['token']}",
            data=json.dumps(body),
            headers=self.headers,
        )
        self.assert_checker(
            session_resp, 201, "SUCCESS", "Update user emailtoedit@email.com"
        )

    def test_edit_user_with_invlid_token(self):
        body = {
            "username": "new_emailer",
            "password": "new+pwd",
            "confirm-password": "new+pwd",
        }
        session_resp = requests.put(
            self.base_url + "/api/user/profile?email=emailtoedit@email.com",
            data=json.dumps(body),
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "Missing argument: token")

    def test_edit_user_with_invalid_body(self):
        session_resp = requests.put(
            self.base_url
            + f"/api/user/profile?email=emailtoedit@email.com&token={self.login_resp_test_body['MESSAGE']['token']}",
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "Missing body")

    def test_edit_user_with_unloggedin_user(self):
        body = {
            "username": "new_emailer",
            "password": "new+pwd",
            "confirm-password": "new+pwd",
        }
        session_resp = requests.put(
            self.base_url
            + f"/api/user/profile?email=emailtoedit@email.com&token=token",
            data=json.dumps(body),
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "Permission denied")

    def test_edit_user_with_missing_field_confirm_password(self):
        body = {
            "username": "new_emailer",
            "password": "new+pwd",
        }
        session_resp = requests.put(
            self.base_url
            + f"/api/user/profile?email=emailtoedit@email.com&token={self.login_resp_test_body['MESSAGE']['token']}",
            data=json.dumps(body),
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "Missing confirm-password")

    def test_edit_user_password_mismatch(self):
        body = {
            "username": "new_emailer",
            "password": "new+pwd",
            "confirm-password": "pwd",
        }
        session_resp = requests.put(
            self.base_url
            + f"/api/user/profile?email=emailtoedit@email.com&token={self.login_resp_test_body['MESSAGE']['token']}",
            data=json.dumps(body),
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "Confirm password mismatch")

    def test_delete_user_happy_path(self):
        session_resp = requests.delete(
            self.base_url
            + f"/api/user/profile?email=emailtodel@email.com&token={self.login_resp_test_body_to_delete['MESSAGE']['token']}",
            headers=self.headers,
        )
        self.assert_checker(
            session_resp, 201, "SUCCESS", "Delete user emailtodel@email.com"
        )

    def test_delete_user_invalid_token(self):
        session_resp = requests.delete(
            self.base_url + f"/api/user/profile?email=testemail@email.com",
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "Missing argument: token")

    def test_delete_user_with_unlogin_user(self):
        session_resp = requests.delete(
            self.base_url
            + f"/api/user/profile?email=invalidemail@email.com&token=test-token",
            headers=self.headers,
        )
        self.assert_checker(session_resp, 400, "FAILED", "Permission denied")
