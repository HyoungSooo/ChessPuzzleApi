from unittest import TestCase
from django.test import Client

client = Client()


class TestUserAPI(TestCase):

    def test_user_can_register(self):
        res = client.post(
            '/api/auth/register', data={'username': 'testcase', 'password': 'testcase'})
        print(res)
        return res
