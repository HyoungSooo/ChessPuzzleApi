from django.test import Client, TestCase
from jwt_auth.models import User
import json


class TestUserAPI(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.data = {'username': 'testcase',
                     'password': 'testcase',
                     'email': 'test@test.com'}
        return super().setUp()

    def register(self):
        user = User.objects.create_user(**self.data)
        token = self.client.post(
            '/api/token/pair',
            json.dumps(self.data),
            content_type='application/json'
        )

        return json.loads(token.content).get('access')

    def test_user_can_register(self):
        res = self.client.post(
            '/api/auth/register',
            json.dumps(self.data),
            content_type='application/json'
        )

        self.assertEqual(json.loads(res.content)['message'], 'testcase')
        self.assertEqual(res.status_code, 200)

        qs = User.objects.filter(username='testcase').first()
        self.assertEqual(qs.username, 'testcase')

        return res

    def test_user_can_get_token(self):
        self.register()
        res = self.client.post(
            '/api/token/pair',
            json.dumps(self.data),
            content_type='application/json'
        )

        data = json.loads(res.content)

        self.assertTrue(data.get('username'))
        self.assertTrue(data.get('refresh'))
        self.assertTrue(data.get('access'))
