import time

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def setup_method(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = register_data["email"]
        self.firstName = register_data["firstName"]
        self.password = register_data["password"]
        self.user_id = self.get_json_value(response1, "id")

    def test_edit_just_created_user(self):
        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_without_auth(self):
        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": "360d9c46809155f647da48f1eaf82a853b5cb5c9f3bd3fd699529f5aa9c91232470ac153"},
                                 cookies={"auth_sid": "09586d0fe18f8744087f3a589383204ef3bd3fd699529f5aa9c91232470ac053"},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_content(response3, '{"error":"Auth token not supplied"}')

    def test_edit_user_with_another_auth(self):
        # REGISTER2
        time.sleep(2)
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        user_id2 = self.get_json_value(response2, "id")

        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }

        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # EDIT
        new_name = "New name"

        response4 = MyRequests.put(f"/user/{user_id2}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response4, 400)
        Assertions.assert_content(response4, '{"error":"This user can only edit their own data."}')

    def test_edit_email_user(self):
        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = "vinkotovexample.com"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"email": new_email})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_content(response3, '{"error":"Invalid email format"}')

    def test_edit_to_short_name(self):
        # LOGIN
        login_data = {
            "email": self.email,
            "password": self.password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "1"

        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_content(response3, '{"error":"The value for field `firstName` is too short"}')
