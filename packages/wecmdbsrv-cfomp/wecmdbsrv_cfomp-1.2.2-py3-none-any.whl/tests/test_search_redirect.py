# import pytest
import http
from flask import url_for
from wecmdbsrv import create_flask_app
# import unittest
from unittest import TestCase, mock
from xml.dom.minidom import parseString
# import os


# @mock.patch.dict(os.environ, {"WEWORK_TOKEN": "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo", "WEWORK_ENCODING_AES_KEY": ""})
# def test_app_config():
#     from wecmdbsrv import create_flask_app
#     app = create_flask_app()
#     assert app.config['WEWORK_TOKEN'] == 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo'


# @mock.patch.dict(os.environ, {"WEWORK_TOKEN": "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo", "WEWORK_ENCODING_AES_KEY": "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt", "WEWORK_CORPID": "ww1436e0e65a779aee"})
class TestBasicPost(TestCase):

    def __init__(self, methodName: str) -> None:
        self.sReqMsgSig = "0c3914025cb4b4d68103f6bfc8db550f79dcf48e"
        self.sReqTimeStamp = "1476422779"
        self.sReqNonce = "1597212914"
        self.sReqData = "<xml><ToUserName><![CDATA[ww1436e0e65a779aee]]></ToUserName>\n<Encrypt><![CDATA[Kl7kjoSf6DMD1zh7rtrHjFaDapSCkaOnwu3bqLc5tAybhhMl9pFeK8NslNPVdMwmBQTNoW4mY7AIjeLvEl3NyeTkAgGzBhzTtRLNshw2AEew+kkYcD+Fq72Kt00fT0WnN87hGrW8SqGc+NcT3mu87Ha3dz1pSDi6GaUA6A0sqfde0VJPQbZ9U+3JWcoD4Z5jaU0y9GSh010wsHF8KZD24YhmZH4ch4Ka7ilEbjbfvhKkNL65HHL0J6EYJIZUC2pFrdkJ7MhmEbU2qARR4iQHE7wy24qy0cRX3Mfp6iELcDNfSsPGjUQVDGxQDCWjayJOpcwocugux082f49HKYg84EpHSGXAyh+/oxwaWbvL6aSDPOYuPDGOCI8jmnKiypE+]]></Encrypt>\n<AgentID><![CDATA[1000002]]></AgentID>\n</xml>"
        # from wecmdbsrv import app
        self.app = create_flask_app(WEWORK_TOKEN="hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo", WEWORK_ENCODING_AES_KEY="6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt", WEWORK_CORPID="ww1436e0e65a779aee", TESTING=True)

        super().__init__(methodName=methodName)

    # def setUp(self, monkeypatch) -> None:
    #     monkeypatch.setenv('WEWORK_TOKEN', 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo')
    #     monkeypatch.setenv('WEWORK_ENCODING_AES_KEY',
    #                    '6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt')
    #     monkeypatch.setenv('WEWORK_CORPID', 'ww1436e0e65a779aee')
    #     return super().setUp()

    def test_app_config(self):
        self.assertEqual(self.app.config['WEWORK_TOKEN'], 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo')
        self.assertEqual(self.app.testing, True)

    def test_msg_signature_absence(self):
        with self.app.test_request_context():
            wrsp = self.app.test_client().post(url_for('basic.basic_post',timestamp=self.sReqTimeStamp, nonce=self.sReqNonce), data=self.sReqData)
            self.assertEqual(wrsp.status_code, http.HTTPStatus.BAD_REQUEST)
    
    
    def test_redirect(self):
        with self.app.test_request_context():
            wrsp = self.app.test_client().post(url_for('basic.basic_post', msg_signature=self.sReqMsgSig, timestamp=self.sReqTimeStamp, nonce=self.sReqNonce), data=self.sReqData)
            self.assertEqual(wrsp.status_code, http.HTTPStatus.OK)
            data = wrsp.get_data().decode('utf-8')
            print(data)
            domtree = parseString(data)
            xmlroot = domtree.documentElement

            self.assertEqual(len(xmlroot.getElementsByTagName('Encrypt')), 1)
            self.assertEqual(len(xmlroot.getElementsByTagName('MsgSignature')), 1)
            self.assertEqual(len(xmlroot.getElementsByTagName('TimeStamp')), 1)
            self.assertEqual(len(xmlroot.getElementsByTagName('Nonce')), 1)
  

# def test_basic_post(monkeypatch):

#     monkeypatch.setenv('WEWORK_TOKEN', 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo')
#     monkeypatch.setenv('WEWORK_ENCODING_AES_KEY',
#                        '6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt')
#     monkeypatch.setenv('WEWORK_CORPID', 'ww1436e0e65a779aee')

#     sReqMsgSig = "0c3914025cb4b4d68103f6bfc8db550f79dcf48e"
#     sReqTimeStamp = "1476422779"
#     sReqNonce = "1597212914"
#     sReqData = "<xml><ToUserName><![CDATA[ww1436e0e65a779aee]]></ToUserName>\n<Encrypt><![CDATA[Kl7kjoSf6DMD1zh7rtrHjFaDapSCkaOnwu3bqLc5tAybhhMl9pFeK8NslNPVdMwmBQTNoW4mY7AIjeLvEl3NyeTkAgGzBhzTtRLNshw2AEew+kkYcD+Fq72Kt00fT0WnN87hGrW8SqGc+NcT3mu87Ha3dz1pSDi6GaUA6A0sqfde0VJPQbZ9U+3JWcoD4Z5jaU0y9GSh010wsHF8KZD24YhmZH4ch4Ka7ilEbjbfvhKkNL65HHL0J6EYJIZUC2pFrdkJ7MhmEbU2qARR4iQHE7wy24qy0cRX3Mfp6iELcDNfSsPGjUQVDGxQDCWjayJOpcwocugux082f49HKYg84EpHSGXAyh+/oxwaWbvL6aSDPOYuPDGOCI8jmnKiypE+]]></Encrypt>\n<AgentID><![CDATA[1000002]]></AgentID>\n</xml>"

#     url = f'/?msg_signature={sReqMsgSig}&timestamp={sReqTimeStamp}&nonce={sReqNonce}'
#     from wecmdbsrv import app
#     app.config['TESTING'] = True
#     assert app.config['WEWORK_TOKEN'] == 'hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo'

#     with app.test_request_context():
#         wrsp = app.test_client().post(url_for('basic.basic_post', msg_signature=sReqMsgSig,
#                                               timestamp=sReqTimeStamp, nonce=sReqNonce), data=sReqData)

#     print(wrsp)
 
