from django.test import TestCase
from rest_framework.test import RequestsClient
from json.decoder import JSONDecodeError
from django.contrib.auth.models import User
from innovation.models import Company
from innovation.serializers import CompanySerializer

BASE_URL = 'http://localhost:8000'


class TestCompanies(TestCase):
    def setUp(self):
        self.company_json = {
            "user": 1,
            "company_name": "name_test",
            "bio": "bio_test"
            }
        User.objects.create_superuser(username='test',password='test')
        self.client = RequestsClient()
        response = self.client.post(BASE_URL + '/api-token-auth/', 
            {'username':'test', 'password':'test'})
        token = response.json()['token']
        self.headers = {'Authorization': f'Token {token}'}
        try:
            self.client.post(BASE_URL + '/companies/', self.company_json,
                headers = self.headers)
        except JSONDecodeError:
            self.fail("/companies/ endpoint for POST request not implemented correctly")

    def test_get_companies(self):
        r = self.client.get(BASE_URL + '/companies/1', headers = self.headers)
        self.assertEqual(r.status_code, 200)
        json_data = r.json()
        serialized_data = CompanySerializer(Company.objects.last()).data
        self.assertEquals(json_data, serialized_data)