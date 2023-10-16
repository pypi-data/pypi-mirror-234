
from elasticsearch import Elasticsearch, ElasticsearchException
from flask import url_for
import http
import unittest
from unittest import mock
from wecmdbsrv import create_flask_app
from urllib.parse import urlparse, parse_qs, unquote, urlsplit
import base64
import json
import os


# def test_miss_mandatory_query_params():

class TestHostlist(unittest.TestCase):
    
    def __init__(self, methodName: str) -> None:
        self.cfg = {
            'WEWORK_TOKEN': 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo', 
            'WEWORK_ENCODING_AES_KEY': '6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt', 
            'WEWORK_CORPID': 'ww1436e0e65a779aee',
            'EXTERNAL_URL': 'https://www.example.com'
        }

        # self.app = create_flask_app(WEWORK_TOKEN="hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo", WEWORK_ENCODING_AES_KEY="6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt", WEWORK_CORPID="ww1436e0e65a779aee", TESTING=True)
        self.app = create_flask_app(**self.cfg, TESTING=True)

        self.client = self.app.test_client()
        super().__init__(methodName=methodName)

    def test_unauthorized(self):
        with self.app.test_request_context():
            origin_url = url_for('host.hostlist', state='state', fromuser='ZhangSan')
            rsp = self.client.get(origin_url)

            self.assertEqual(rsp.status_code, http.HTTPStatus.FOUND)
            o = urlparse(rsp.location)
            print(o)
            self.assertEqual(o.scheme, 'https')
            self.assertEqual(o.netloc, 'open.weixin.qq.com')
            self.assertEqual(o.path, '/connect/oauth2/authorize')
            # self.assertEqual(o.query)
            self.assertEqual(o.fragment, 'wechat_redirect')

            qs = parse_qs(o.query)
            print(qs)
            self.assertEqual(qs['appid'], [self.app.config['WEWORK_CORPID']])
            self.assertEqual(qs['response_type'], ['code'])
            self.assertEqual(qs['scope'], ['snsapi_base'])
            self.assertIn('redirect_uri', qs)

            redirect_uri = urlparse(unquote(qs['redirect_uri'][0]))
            self.assertEqual(redirect_uri.path, url_for('oauth.oauthredirect'))
            redirect_uri_qs = parse_qs(redirect_uri.query)
            self.assertIn('myredirect', redirect_uri_qs)

            myredirect = urlsplit(base64.b64decode(redirect_uri_qs['myredirect'][0]))
            self.assertEqual(myredirect.geturl(), origin_url.encode())
            print(rsp.location)

    def test_es_error(self):
        with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess['Authorized'] = True

            with mock.patch.object(Elasticsearch, 'search', side_effect=ElasticsearchException) as mock_es_search:
                with self.assertRaises(ElasticsearchException):
                    qs = {'from': 0, 'size': 20, 'q': '*'}
                    rv = self.client.get(url_for('host.hostlist', **qs))
   
    def test_render_template(self):
       with self.app.test_request_context():
            with self.client.session_transaction() as sess:
                sess['Authorized'] = True

            res = {''}
            jp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'essearchres.json')
            with open(jp, mode='r', encoding='utf-8') as fp:
                res = json.load(fp, )

            with mock.patch.object(Elasticsearch, 'search', return_value=res) as mock_es_search:
                qs = {'from': 0, 'size': 20, 'q': '*'}
                rv = self.client.get(url_for('host.hostlist', **qs))
                self.assertEqual(rv.status_code, http.HTTPStatus.OK)
  

    # def test_authorized(self):
    #     # with self.app.test_client() as c:
    #     with self.app.test_request_context():
    #         with self.client.session_transaction() as sess:
    #             sess['Authorized'] = True

    #         qs = {'from': 0, 'size': 20, 'q': '*'}
    #         rv = self.client.get(url_for('host.hostlist', **qs))
    #         print(rv)

            

# @pytest.fixture
# def myapp(monkeypatch):
   
#     monkeypatch.setenv('WEWORK_TOKEN', 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo')
#     monkeypatch.setenv('WEWORK_ENCODING_AES_KEY', '6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt')
#     monkeypatch.setenv('WEWORK_CORPID', 'ww1436e0e65a779aee')
#     monkeypatch.setenv('ES_HOSTS', '10.189.67.26:9200')
#     from wecmdbsrv import app
#     app.config['TESTING'] = True
#     yield app

# # @pytest.fixture
# # def client(app):
# #     return app.test_client()

# def test_no_session(myapp):
#     resp = myapp.test_client().get('/hostlist/')
#     assert resp.status_code == http.HTTPStatus.FORBIDDEN

# def test_session_mismatch(myapp):
#     sReqMsgSig = "0c3914025cb4b4d68103f6bfc8db550f79dcf48e"
#     sReqTimeStamp = "1476422779"
#     sReqNonce = "1597212914"
#     sReqData = "<xml><ToUserName><![CDATA[ww1436e0e65a779aee]]></ToUserName>\n<Encrypt><![CDATA[Kl7kjoSf6DMD1zh7rtrHjFaDapSCkaOnwu3bqLc5tAybhhMl9pFeK8NslNPVdMwmBQTNoW4mY7AIjeLvEl3NyeTkAgGzBhzTtRLNshw2AEew+kkYcD+Fq72Kt00fT0WnN87hGrW8SqGc+NcT3mu87Ha3dz1pSDi6GaUA6A0sqfde0VJPQbZ9U+3JWcoD4Z5jaU0y9GSh010wsHF8KZD24YhmZH4ch4Ka7ilEbjbfvhKkNL65HHL0J6EYJIZUC2pFrdkJ7MhmEbU2qARR4iQHE7wy24qy0cRX3Mfp6iELcDNfSsPGjUQVDGxQDCWjayJOpcwocugux082f49HKYg84EpHSGXAyh+/oxwaWbvL6aSDPOYuPDGOCI8jmnKiypE+]]></Encrypt>\n<AgentID><![CDATA[1000002]]></AgentID>\n</xml>"

#     url = f'/?msg_signature={sReqMsgSig}&timestamp={sReqTimeStamp}&nonce={sReqNonce}'
#     client = myapp.test_client()
#     wrsp = client.post(url, data=sReqData)
#     wrsp = client.get(f'/hostlist/?state=invalidstate')
#     assert wrsp.status_code == http.HTTPStatus.BAD_REQUEST

# def test_search(myapp):
#     sReqMsgSig = "0c3914025cb4b4d68103f6bfc8db550f79dcf48e"
#     sReqTimeStamp = "1476422779"
#     sReqNonce = "1597212914"
#     sReqData = "<xml><ToUserName><![CDATA[ww1436e0e65a779aee]]></ToUserName>\n<Encrypt><![CDATA[Kl7kjoSf6DMD1zh7rtrHjFaDapSCkaOnwu3bqLc5tAybhhMl9pFeK8NslNPVdMwmBQTNoW4mY7AIjeLvEl3NyeTkAgGzBhzTtRLNshw2AEew+kkYcD+Fq72Kt00fT0WnN87hGrW8SqGc+NcT3mu87Ha3dz1pSDi6GaUA6A0sqfde0VJPQbZ9U+3JWcoD4Z5jaU0y9GSh010wsHF8KZD24YhmZH4ch4Ka7ilEbjbfvhKkNL65HHL0J6EYJIZUC2pFrdkJ7MhmEbU2qARR4iQHE7wy24qy0cRX3Mfp6iELcDNfSsPGjUQVDGxQDCWjayJOpcwocugux082f49HKYg84EpHSGXAyh+/oxwaWbvL6aSDPOYuPDGOCI8jmnKiypE+]]></Encrypt>\n<AgentID><![CDATA[1000002]]></AgentID>\n</xml>"

#     url = f'/?msg_signature={sReqMsgSig}&timestamp={sReqTimeStamp}&nonce={sReqNonce}'
#     client = myapp.test_client()
#     wrsp = client.post(url, data=sReqData)
#     wrsp = client.get(f'/hostlist/?state=0c3914025cb4b4d68103f6bfc8db550f79dcf48e')

 