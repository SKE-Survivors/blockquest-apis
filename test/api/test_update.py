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
        print(self.dbh.find_user("testemail@email.com").to_dict())

        body = {"email": "testemail@email.com", "password": "eemail"}
        resp = requests.post(
            self.base_url + "/api/auth/login",
            data=json.dumps(body),
            headers=self.headers,
        )
        self.login_resp_body = resp.json()

        print()

    @classmethod
    def tearDownClass(self) -> None:
        self.dbh.delete_user("testemail@email.com")

    def assert_checker(self, url, status_code, body_status, body_msg):
        session_resp = requests.post(self.base_url + url, headers=self.headers)
        self.assertEqual(session_resp.status_code, status_code)

        session_resp_body = session_resp.json()
        self.assertEqual(session_resp_body["STATUS"], body_status)
        self.assertEqual(session_resp_body["MESSAGE"], body_msg)

    def test_unlock_section_happy_path(self):

        update_session = {
            "email": "testemail@email.com",
            "token": self.login_resp_body["MESSAGE"]["token"],
            "id": "l1",
        }

        self.assert_checker(
            f"/api/update/section/unlock?email={update_session['email']}&id={update_session['id']}&token={update_session['token']}",
            201,
            "SUCCESS",
            "Section L1 unlocked",
        )

    def test_unlock_section_with_invalid_email(self):
        update_session = {"email": None, "token": "test token", "id": "l1"}

        self.assert_checker(
            f"/api/update/section/unlock?id={update_session['id']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: email",
        )

    def test_unlock_section_with_invalid_token(self):
        update_session = {"email": "testemail@email.com", "token": None, "id": "l1"}

        self.assert_checker(
            f"/api/update/section/unlock?email={update_session['email']}&id={update_session['id']}",
            400,
            "FAILED",
            "Missing argument: token",
        )

    def test_unlock_section_with_invalid_section_id(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "id": None,
        }

        self.assert_checker(
            f"/api/update/section/unlock?email={update_session['email']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: section_id",
        )

    def test_unlock_section_with_unlogin_account(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "id": "l1",
        }

        self.assert_checker(
            f"/api/update/section/unlock?email={update_session['email']}&id={update_session['id']}&token={update_session['token']}",
            400,
            "FAILED",
            "Permission denied",
        )

    ###
    # def test_unlock_section_with_unregistered_account(self):
    #     update_session = {
    #         "email": "test.email@email.com",
    #         "token": "test token",
    #         "id": "l1"
    #     }

    #     self.assert_checker(f"/api/update/section/unlock?email={update_session['email']}&id={update_session['id']}&token={update_session['token']}", 400, "FAILED", "User does not exist")

    def test_unlock_section_with_currently_unavailable_section_for_loggedin_account(
        self,
    ):
        update_session = {
            "email": "testemail@email.com",
            "token": self.login_resp_body["MESSAGE"]["token"],
            "id": "l5",
        }

        self.assert_checker(
            f"/api/update/section/unlock?email={update_session['email']}&id={update_session['id']}&token={update_session['token']}",
            400,
            "FAILED",
            "Section does not exist (for this user)",
        )

    def test_lock_section_happy_path(self):
        update_session = {
            "email": "testemail@email.com",
            "token": self.login_resp_body["MESSAGE"]["token"],
            "id": "l1",
        }
        self.assert_checker(
            f"/api/update/section/lock?email={update_session['email']}&id={update_session['id']}&token={update_session['token']}",
            201,
            "SUCCESS",
            "Section L1 locked",
        )

    def test_lock_section_with_invalid_email(self):
        update_session = {"email": None, "token": "test token", "id": "l1"}

        self.assert_checker(
            f"/api/update/section/lock?id={update_session['id']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: email",
        )

    def test_lock_section_with_invalid_token(self):
        update_session = {"email": "testemail@email.com", "token": None, "id": "l1"}

        self.assert_checker(
            f"/api/update/section/lock?email={update_session['email']}&id={update_session['id']}",
            400,
            "FAILED",
            "Missing argument: token",
        )

    def test_lock_section_with_invalid_section_id(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "id": None,
        }

        self.assert_checker(
            f"/api/update/section/lock?email={update_session['email']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: section_id",
        )

    def test_lock_section_with_unlogin_account(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "id": "l1",
        }

        self.assert_checker(
            f"/api/update/section/lock?email={update_session['email']}&id={update_session['id']}&token={update_session['token']}",
            400,
            "FAILED",
            "Permission denied",
        )

    # def test_lock_section_with_unregistered_account(self):
    #     update_session_body = {
    #         "email": "test.email@email.com",
    #         "token": "test token",
    #         "id": "l1"
    #     }

    #     self.assert_checker("/api/update/section/lock", update_session_body, 400, "FAILED", "User does not exist")

    def test_lock_section_with_currently_unavailable_section_for_loggedin_account(self):
        update_session = {
            "email": "testemail@email.com",
            "token": self.login_resp_body["MESSAGE"]["token"],
            "id": "l5",
        }

        self.assert_checker(
            f"/api/update/section/lock?email={update_session['email']}&id={update_session['id']}&token={update_session['token']}",
            400,
            "FAILED",
            "Section does not exist (for this user)",
        )

    def test_add_item_happy_path(self):
        update_session = {
            "email": "testemail@email.com",
            "token": self.login_resp_body["MESSAGE"]["token"],
            "item": "test item",
        }

        self.assert_checker(
            f"/api/update/bag/add?email={update_session['email']}&item={update_session['item']}&token={update_session['token']}",
            201,
            "SUCCESS",
            "test item added",
        )

    def test_add_item_with_invalid_email(self):
        update_session = {"email": None, "token": "test token", "item": "test item"}

        self.assert_checker(
            f"/api/update/bag/add?item={update_session['item']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: email",
        )

    def test_add_item_with_invalid_token(self):
        update_session = {
            "email": "testemail@email.com",
            "token": None,
            "item": "test item",
        }

        self.assert_checker(
            f"/api/update/bag/add?email={update_session['email']}&item={update_session['item']}",
            400,
            "FAILED",
            "Missing argument: token",
        )

    def test_add_item_with_invalid_item(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "item": None,
        }

        self.assert_checker(
            f"/api/update/bag/add?email={update_session['email']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: item",
        )

    def test_add_item_with_unlogin_account(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "item": "test item",
        }

        self.assert_checker(
            f"/api/update/bag/add?email={update_session['email']}&item={update_session['item']}&token={update_session['token']}",
            400,
            "FAILED",
            "Permission denied",
        )

    def test_remove_item_happy_path(self):
        update_session = {
            "email": "testemail@email.com",
            "token": self.login_resp_body["MESSAGE"]["token"],
            "item": "test item",
        }

        self.assert_checker(
            f"/api/update/bag/remove?email={update_session['email']}&item={update_session['item']}&token={update_session['token']}",
            201,
            "SUCCESS",
            "test item removed",
        )

    def test_remove_item_with_invalid_email(self):
        update_session = {"email": None, "token": "test token", "item": "test item"}

        self.assert_checker(
            f"/api/update/bag/remove?item={update_session['item']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: email",
        )

    def test_remove_item_with_invalid_token(self):
        update_session = {
            "email": "testemail@email.com",
            "token": None,
            "item": "test item",
        }

        self.assert_checker(
            f"/api/update/bag/remove?email={update_session['email']}&item={update_session['item']}",
            400,
            "FAILED",
            "Missing argument: token",
        )

    def test_remove_item_with_invalid_item(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "item": None,
        }

        self.assert_checker(
            f"/api/update/bag/remove?email={update_session['email']}&token={update_session['token']}",
            400,
            "FAILED",
            "Missing argument: item",
        )

    def test_remove_item_with_unlogin_account(self):
        update_session = {
            "email": "testemail@email.com",
            "token": "test token",
            "item": "test item",
        }

        self.assert_checker(
            f"/api/update/bag/remove?email={update_session['email']}&item={update_session['item']}&token={update_session['token']}",
            400,
            "FAILED",
            "Permission denied",
        )
