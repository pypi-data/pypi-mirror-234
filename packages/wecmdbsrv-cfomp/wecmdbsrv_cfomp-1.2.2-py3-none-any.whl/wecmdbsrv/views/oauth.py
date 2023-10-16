from flask import request, session, current_app, redirect, Blueprint
import werkzeug.exceptions
from urllib.parse import urljoin
from weworkapi.CorpApi import CorpApi, CORP_API_TYPE
import base64

bp = Blueprint('oauth', __name__)
WEWORK_ACCESS_TOKEN = None


@bp.route('/oauthredirect', methods=['GET'])
def oauthredirect():
    code = request.args['code']
    state = request.args['state']
    myredirect = base64.b64decode(request.args['myredirect'])

    if session.get('state') != state:
        raise werkzeug.exceptions.BadRequest()

    corpapi = CorpApi(
        current_app.config['WEWORK_CORPID'], current_app.config['WEWORK_SECRET'])

    global WEWORK_ACCESS_TOKEN
    setattr(corpapi, 'access_token', WEWORK_ACCESS_TOKEN)
    res = corpapi.httpCall(
        CORP_API_TYPE['GET_USER_INFO_BY_CODE'], {'code': code})
    current_app.logger.info(
        'CorpApi.httpCall GET_USER_INFO_BY_CODE return {res}')
    # res = corpapi.httpCall(CORP_API_TYPE['GET_USER_INFO_BY_CODE'], {'code': 'invalid'})
    WEWORK_ACCESS_TOKEN = corpapi.getAccessToken()

    if res['UserId'] != session.get('UserId'):
        current_app.logger.error(
            f"UserId between session[{session.get('UserId')}] and GET_USER_INFO_BY_CODE result[{res['UserId']} unequal!]")
        raise werkzeug.exceptions.Forbidden()
    session['Authorized'] = True
    return redirect(urljoin(current_app.config['EXTERNAL_URL'], myredirect.decode()))

