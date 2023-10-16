import unittest
import json
import os
from elasticsearch import Elasticsearch
import http
from unittest import mock
from flask import url_for
from wecmdbsrv import create_flask_app

class TestHostdetail(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.cfg = {
            'WEWORK_TOKEN': 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo', 
            'WEWORK_ENCODING_AES_KEY': '6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt', 
            'WEWORK_CORPID': 'ww1436e0e65a779aee',
            'EXTERNAL_URL': 'https://www.example.com'
        }

        # self.app = create_flask_app(WEWORK_TOKEN="hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo", WEWORK_ENCODING_AES_KEY="6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt", WEWORK_CORPID="ww1436e0e65a779aee", TESTING=True)
        self.app = create_flask_app(**self.cfg, TESTING=True)

        self.client = self.app.test_client()

    
    def test_hostdetail(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess['Authorized'] = True
            
            res = {''}
            jp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'esgetres.json')
            with open(jp, mode='r', encoding='utf-8') as fp:
                res = json.load(fp, )

            with mock.patch.object(Elasticsearch, 'get', return_value=res) as mock_es_get:
                rv = self.client.get(url_for('host.hostdetail', id=11196))
                self.assertEqual(rv.status_code, http.HTTPStatus.OK)
            