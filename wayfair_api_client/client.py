import json

import requests as rq
from gql import gql, Client as GQLClient
from gql.transport.requests import RequestsHTTPTransport
import six

from . import (
    utils,
    queries
)

class WayfairAPICLient:
    BASE_URL = 'https://api.wayfair.com'
    SANDBOX_BASE_URL = 'https://sandbox.api.wayfair.com'
    AUTH_URL = 'https://sso.auth.wayfair.com/oauth/token'

    def __init__(self, client_id, client_secret, queries=queries.Queries, sandbox=False):
        self._session = rq.Session()
        self._sandbox = sandbox
        self._client_id = client_id
        self._client_secret = client_secret
        self._queries = queries

        self._authtenticate()
        self._init_gql_client()

    @property
    def endpoints(self):
        api_base_url = self.SANDBOX_BASE_URL if self._sandbox else self.BASE_URL
        endpoints = {
            'api': api_base_url,
            'gql': utils.urljoin(api_base_url, 'v1/graphql'),
        }
        return endpoints

    def _init_gql_client(self):
        session_auth_header_value = self._session.headers.get('Authorization')
        self._gql_client = GQLClient(transport=RequestsHTTPTransport(
            url=self.endpoints.get('gql'),
            headers={'Authorization': session_auth_header_value}))

    def _authtenticate(self):
        payload = {
            "grant_type":"client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "audience": self.BASE_URL
        }
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }
        res = self._session.post(self.AUTH_URL, data=json.dumps(payload), headers=headers)
        if res.status_code != 200:
            raise ValueError('Authentication Failed, Please check your credentials')

        self._token_type, self._access_token = res.json().get('token_type'), res.json().get('access_token')
        auth_headers = {
            'Authorization': '{} {}'.format(self._token_type, self._access_token),
            'Content-Type': 'application/json',
        }
        self._session.headers.update(auth_headers)
        return res.json()

    def execute(self, query, params=None):
        if isinstance(query, six.string_types):
            query = gql(query)
        return self._gql_client.execute(query, params)

    def fetch_purchase_order_list(self, limit=100):
        params = {'limit': limit}
        res = self.execute(self._queries.purchase_order_list_query, params=params)
        return res.get('purchaseOrders', [])
    
    def fetch_purchase_order(self, poNumber):
        params = {'poNumber': poNumber}
        res = self.execute(self._queries.purchase_order_query, params=params)
        return res.get('purchaseOrders', [])