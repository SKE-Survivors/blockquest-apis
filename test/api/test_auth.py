import json
import unittest

import requests
import sys

from mongoengine import errors

sys.path.append("c:\\Users\\DELL\\GitHub\\blockquest-api\\test\\api\\..\\..\\src\\handler")
sys.path.insert(0,"c:\\Users\\DELL\\GitHub\\blockquest-api\\src\\utils")

print(sys.path)
from handler.database import DatabaseHandler
from utils.password import encode_pwd

class TestAuth(unittest.TestCase):
    base_url = "http://localhost:3000"
    headers = {'Content-Type': 'application/json' } 
    body = {
            "email": "testgmail@gmail.com",
            "username": "gmail",
            "password": "ggmail",
            "confirm-password": "ggmail",
        }
    
    @classmethod
    def setUpClass(self) -> None:
        self.dbh = DatabaseHandler()
        self.dbh.add_user("testemail@email.com", "emailer", encode_pwd("eemail"))
    
    def test_signup_happy_path(self):
        resp = requests.post(self.base_url+"/api/auth/signup", data=json.dumps(self.body), headers=self.headers)
        self.assertEqual(resp.status_code, 201)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "SUCCESS")
        self.assertEqual(resp_body["MESSAGE"], "Registration Successfully")
        
    def test_signup_with_invalid_email(self):
        body = {
            "email": None,
            "username": "gmail",
            "password": "ggmail",
            "confirm-password": "ggmail",
        }
        resp = requests.post(self.base_url+"/api/auth/signup", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Email is required")
   
    def test_signup_with_invalid_password(self):
        body = {
            "email": "test2gmail@gmail.com",
            "username": "gmail",
            "password": None,
            "confirm-password": "ggmail",
        }
        resp = requests.post(self.base_url+"/api/auth/signup", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Password is required")
    
    def test_signup_with_invalid_confirm_password(self):
        body = {
            "email": "test2gmail@gmail.com",
            "username": "gmail",
            "password": "password",
            "confirm-password": "ggmail",
        }
        resp = requests.post(self.base_url+"/api/auth/signup", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Confirm password is wrong")
        
    def test_signup_user_already_exist(self):
        resp = requests.post(self.base_url+"/api/auth/signup", data=json.dumps(self.body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "User already exist")
        
    def test_email_validation_error(self):
        body = {
            "email": 123,
            "username": "gmail",
            "password": "ggmail",
            "confirm-password": "ggmail",
        }
        resp = requests.post(self.base_url+"/api/auth/signup", data=json.dumps(body), headers=self.headers)
    
        self.assertEqual(resp.status_code, 400)
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Registration failed: ValidationError (User:123) (StringField only accepts string values: ['email'])")
        
        body = {
            "email": "aaaaa",
            "username": "gmail",
            "password": "ggmail",
            "confirm-password": "ggmail",
        }
        resp = requests.post(self.base_url+"/api/auth/signup", data=json.dumps(body), headers=self.headers)
    
        self.assertEqual(resp.status_code, 400)
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Registration failed: ValidationError (User:aaaaa) (Invalid email address: aaaaa: ['email'])")
    
    def test_login_happy_path(self):
        body = {
            "email": "testemail@email.com",
            "password": "eemail"
        }
        resp = requests.post(self.base_url+"/api/auth/login", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 201)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "SUCCESS")
        
    def test_login_with_invalid_email(self):
        body = {
            "email": None,
            "password": "eemail"
        }
        resp = requests.post(self.base_url+"/api/auth/login", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Email is required")
   
    def test_login_with_invalid_password(self):
        body = {
            "email": "testemail@email.com",
            "password": None
        }
        resp = requests.post(self.base_url+"/api/auth/login", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Password is required")
    
    def test_login_with_non_existing_user(self):
        body = {
            "email": "notexist@email.com",
            "password": "eeeee"
        }
        resp = requests.post(self.base_url+"/api/auth/login", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "User does not exist")
    
    def test_login_with_wrong_password(self):
        body = {
            "email": "testemail@email.com",
            "password": "wrong_password"
        }
        resp = requests.post(self.base_url+"/api/auth/login", data=json.dumps(body), headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        
        resp_body = resp.json()
        self.assertEqual(resp_body["STATUS"], "FAILED")
        self.assertEqual(resp_body["MESSAGE"], "Wrong password")
        
    def test_logout_happy_path(self):
        body = {
            "email": "testemail@email.com",
            "password": "eemail"
        }
        resp = requests.post(self.base_url+"/api/auth/login", data=json.dumps(body), headers=self.headers)
        resp_body = resp.json()
        
        resp_logout = requests.get(self.base_url+"/api/auth/logout?email=testemail@email.com&token="+resp_body["MESSAGE"]["token"], headers=self.headers)
        self.assertEqual(resp_logout.status_code, 200)
        
        resp_logout_body = resp_logout.json()
        self.assertEqual(resp_logout_body["STATUS"], "SUCCESS")
        self.assertEqual(resp_logout_body["MESSAGE"], "Logout successfully")
        
    def test_logout_with_non_existing_user(self):
        resp_logout = requests.get(self.base_url+"/api/auth/logout?email=fake@email.com&token=123", headers=self.headers)
        self.assertEqual(resp_logout.status_code, 400)
        
        resp_logout_body = resp_logout.json()
        self.assertEqual(resp_logout_body["STATUS"], "FAILED")
        self.assertEqual(resp_logout_body["MESSAGE"], "User does not exist")
    
    def test_check_endpoint_happy_path(self):
        body = {
            "email": "testemail@email.com",
            "password": "eemail"
        }
        resp = requests.post(self.base_url+"/api/auth/login", data=json.dumps(body), headers=self.headers)
        resp_body = resp.json()
        
        resp_check = requests.get(self.base_url+"/api/auth/check?email=testemail@email.com&token="+resp_body["MESSAGE"]["token"], headers=self.headers)
        self.assertEqual(resp_check.status_code, 200)
        
        resp_check_body = resp_check.json()
        self.assertEqual(resp_check_body["STATUS"], "SUCCESS")
        self.assertEqual(resp_check_body["MESSAGE"], "User is authorized")
        
    def test_check_endpoint_with_unauthorized_user(self):
        resp_check = requests.get(self.base_url+"/api/auth/check?email=testemail@email.com&token=123", headers=self.headers)
        self.assertEqual(resp_check.status_code, 200)
        
        resp_check_body = resp_check.json()
        self.assertEqual(resp_check_body["STATUS"], "SUCCESS")
        self.assertEqual(resp_check_body["MESSAGE"], "User is not authorized")
    
    def test_check_endpoint_with_non_existing_user(self):
        resp_check = requests.get(self.base_url+"/api/auth/check?email=fake@email.com&token=123", headers=self.headers)
        self.assertEqual(resp_check.status_code, 400)
        
        resp_check_body = resp_check.json()
        self.assertEqual(resp_check_body["STATUS"], "FAILED")
        self.assertEqual(resp_check_body["MESSAGE"], "User does not exist")
    
    @classmethod
    def tearDownClass(self) -> None:
        self.dbh.delete_user("testgmail@gmail.com")
        self.dbh.delete_user("testemail@email.com")
        
