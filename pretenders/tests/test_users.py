
import json
import time
import unittest

from tests.base import BaseTestCase

from pretenders import db
from dao.user_dao import add_user
from api.models import BlacklistToken


def register_user(self, username, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json',
    )


def login_user(self, username, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json',
    )


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""
    def test_encode_auth_token(self):
        from api.models import User
        user = add_user('test@test.com', 'test')
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        from api.models import User
        user = add_user('test@test.com', 'test')
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered username"""
        add_user('joe@gmail.com', 'test')
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            resp_register = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json',
            )
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)

            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    username='joe@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    username='joey@gmail.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        """ Test for user status """

        register_user(self, 'joe@gmail.com', '123456')
        resp_login = login_user(self, 'joe@gmail.com', '123456')

        response = self.client.get(
            '/auth/status',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['data'] is not None)
        self.assertTrue(data['data']['username'] == 'joe@gmail.com')
        self.assertEqual(response.status_code, 200)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token"""
        register_user(self, 'joe@gmail.com', '123456')
        resp_login = login_user(self, 'joe@gmail.com', '123456')
        response = self.client.get(
            '/auth/status',
            headers=dict(
                Authorization='Bearer' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Bearer token malformed.')
        self.assertEqual(response.status_code, 401)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        # user registration
        resp_register = register_user(self, 'joe@gmail.com', '123456')
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['message'] == 'Successfully registered.')
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user(self, 'joe@gmail.com', '123456')
        data_login = json.loads(resp_login.data.decode())
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['auth_token'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        # valid token logout
        response = self.client.post(
            '/auth/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(response.status_code, 200)

    # def test_invalid_logout(self):
    #     """ Testing logout after the token expires """
    #     with self.client:
    #         # user registration
    #         resp_register = register_user(self, 'joe@gmail.com', '123456')
    #         data_register = json.loads(resp_register.data.decode())
    #         self.assertTrue(data_register['status'] == 'success')
    #         self.assertTrue(
    #             data_register['message'] == 'Successfully registered.')
    #         self.assertTrue(data_register['auth_token'])
    #         self.assertTrue(resp_register.content_type == 'application/json')
    #         self.assertEqual(resp_register.status_code, 201)
    #         # user login
    #         resp_login = login_user(self, 'joe@gmail.com', '123456')
    #         data_login = json.loads(resp_login.data.decode())
    #         self.assertTrue(data_login['status'] == 'success')
    #         self.assertTrue(data_login['message'] == 'Successfully logged in.')
    #         self.assertTrue(data_login['auth_token'])
    #         self.assertTrue(resp_login.content_type == 'application/json')
    #         self.assertEqual(resp_login.status_code, 200)
    #         # invalid token logout
    #         time.sleep(6)
    #         response = self.client.post(
    #             '/auth/logout',
    #             headers=dict(
    #                 Authorization='Bearer ' + json.loads(
    #                     resp_login.data.decode()
    #                 )['auth_token']
    #             )
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['status'] == 'fail')
    #         self.assertTrue(
    #             data['message'] == 'Signature expired. Please log in again.')
    #         self.assertEqual(response.status_code, 401)

    # def test_valid_blacklisted_token_logout(self):
    #     """ Test for logout after a valid token gets blacklisted """
    #
    #     from api.models import BlacklistToken
    #
    #     with self.client:
    #         # user registration
    #         resp_register = register_user(self, 'joe@gmail.com', '123456')
    #         data_register = json.loads(resp_register.data.decode())
    #         self.assertTrue(data_register['status'] == 'success')
    #         self.assertTrue(
    #             data_register['message'] == 'Successfully registered.')
    #         self.assertTrue(data_register['auth_token'])
    #         self.assertTrue(resp_register.content_type == 'application/json')
    #         self.assertEqual(resp_register.status_code, 201)
    #
    #         # user login
    #         resp_login = login_user(self, 'joe@gmail.com', '123456')
    #         data_login = json.loads(resp_login.data.decode())
    #         self.assertTrue(data_login['status'] == 'success')
    #         self.assertTrue(data_login['message'] == 'Successfully logged in.')
    #         self.assertTrue(data_login['auth_token'])
    #         self.assertTrue(resp_login.content_type == 'application/json')
    #         self.assertEqual(resp_login.status_code, 200)
    #
    #
    #         # blacklist a valid token
    #         blacklist_token = BlacklistToken(
    #             token=json.loads(resp_login.data.decode())['auth_token'])
    #         db.session.add(blacklist_token)
    #         db.session.commit()
    #
    #         # blacklisted valid token logout
    #         response = self.client.post(
    #             '/auth/logout',
    #             headers=dict(
    #                 Authorization='Bearer ' + json.loads(
    #                     resp_login.data.decode()
    #                 )['auth_token']
    #             )
    #         )
    #         data = json.loads(response.data.decode())
    #         self.assertTrue(data['status'] == 'fail')
    #         self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
    #         self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        """ Test for user status with a blacklisted valid token """

        register_user(self, 'joe@gmail.com', '123456')
        resp_login = login_user(self, 'joe@gmail.com', '123456')

        # blacklist a valid token
        blacklist_token = BlacklistToken(
            token=json.loads(resp_login.data.decode())['auth_token'])
        db.session.add(blacklist_token)
        db.session.commit()
        response = self.client.get(
            '/auth/status',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'This token has expired.')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
