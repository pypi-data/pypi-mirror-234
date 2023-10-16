from collections import deque
from flask import request, session, current_app, url_for, Blueprint
import werkzeug.exceptions
from wework_callback.WXBizMsgCrypt3 import WXBizMsgCrypt
import xmltodict
import IPy

bp = Blueprint('basic', __name__)
MSG_IDS = deque(maxlen=1000)


def isIP(str):
    try:
        IPy.IP(str)
    except ValueError:
        return False
    return True


@bp.route('/', methods=['GET'])
def basic_get():
    '''
        *企业开启回调模式时，企业号会向验证url发送一个get请求 
        假设点击验证时，企业收到类似请求：
        * GET /cgi-bin/wxpush?msg_signature=5c45ff5e21c57e6ad56bac8758b79b1d9ac89fd3&timestamp=1409659589&nonce=263014780&echostr=P9nAzCzyDtyTWESHep1vC5X9xho%2FqYX3Zpb4yKa9SKld1DsH3Iyt3tP3zNdtp%2B4RPcs8TgAE7OaBO%2BFZXvnaqQ%3D%3D 
        * HTTP/1.1 Host: qy.weixin.qq.com

        接收到该请求时，企业应	1.解析出Get请求的参数，包括消息体签名(msg_signature)，时间戳(timestamp)，随机数字串(nonce)以及企业微信推送过来的随机加密字符串(echostr),
        这一步注意作URL解码。
        2.验证消息体签名的正确性 
        3. 解密出echostr原文，将原文当作Get请求的response，返回给企业微信
        第2，3步可以用企业微信提供的库函数VerifyURL来实现。
   '''

    wxcpt = WXBizMsgCrypt(
        current_app.config['WEWORK_TOKEN'], current_app.config['WEWORK_ENCODING_AES_KEY'], current_app.config['WEWORK_CORPID'])
    ret, sEchoStr = wxcpt.VerifyURL(request.args['msg_signature'], request.args['timestamp'],
                                    request.args['nonce'], request.args['echostr'])

    if ret:
        current_app.logger.error(f'VerifyURL ret: {ret}')
        raise werkzeug.exceptions.BadRequest()
    return sEchoStr


@bp.route('/', methods=['POST'])
def basic_post():
    '''
   用户回复消息或者点击事件响应时，企业会收到回调消息，此消息是经过企业微信加密之后的密文以post形式发送给企业，密文格式请参考官方文档
   假设企业收到企业微信的回调消息如下：
   POST /cgi-bin/wxpush? msg_signature=477715d11cdb4164915debcba66cb864d751f3e6&timestamp=1409659813&nonce=1372623149 HTTP/1.1
   Host: qy.weixin.qq.com
   Content-Length: 613
   <xml> <ToUserName><![CDATA[wx5823bf96d3bd56c7]]></ToUserName><Encrypt><![CDATA[RypEvHKD8QQKFhvQ6QleEB4J58tiPdvo+rtK1I9qca6aM/wvqnLSV5zEPeusUiX5L5X/0lWfrf0QADHHhGd3QczcdCUpj911L3vg3W/sYYvuJTs3TUUkSUXxaccAS0qhxchrRYt66wiSpGLYL42aM6A8dTT+6k4aSknmPj48kzJs8qLjvd4Xgpue06DOdnLxAUHzM6+kDZ+HMZfJYuR+LtwGc2hgf5gsijff0ekUNXZiqATP7PF5mZxZ3Izoun1s4zG4LUMnvw2r+KqCKIw+3IQH03v+BCA9nMELNqbSf6tiWSrXJB3LAVGUcallcrw8V2t9EL4EhzJWrQUax5wLVMNS0+rUPA3k22Ncx4XXZS9o0MBH27Bo6BpNelZpS+/uh9KsNlY6bHCmJU9p8g7m3fVKn28H3KDYA5Pl/T8Z1ptDAVe0lXdQ2YoyyH2uyPIGHBZZIs2pDBS8R07+qN+E7Q==]]></Encrypt>
   <AgentID><![CDATA[218]]></AgentID>
   </xml>

   企业收到post请求之后应该 1.解析出url上的参数，包括消息体签名(msg_signature)，时间戳(timestamp)以及随机数字串(nonce)
   2.验证消息体签名的正确性。 3.将post请求的数据进行xml解析，并将<Encrypt>标签的内容进行解密，解密出来的明文即是用户回复消息的明文，明文格式请参考官方文档
   第2，3步可以用企业微信提供的库函数DecryptMsg来实现。
   '''

    # current_app.logger.debug('Callback request body: ' +
    #                          request.get_data().decode('utf-8'))
    if not (request.args.get('msg_signature') and request.args.get('timestamp') and request.args.get('nonce')):
        current_app.logger.error('The mandatory query parameter missed')
        raise werkzeug.exceptions.BadRequest()

    wxcpt = WXBizMsgCrypt(
        current_app.config['WEWORK_TOKEN'], current_app.config['WEWORK_ENCODING_AES_KEY'], current_app.config['WEWORK_CORPID'])

    ret, sMsg = wxcpt.DecryptMsg(request.get_data(
    ), request.args['msg_signature'], request.args['timestamp'], request.args['nonce'])
    if ret:
        current_app.logger.error(f'DecryptMsg ret: {ret}')
        raise werkzeug.exceptions.BadRequest()

    current_app.logger.debug('DecryptMsg is ' + sMsg.decode('utf-8'))

    dMsg = xmltodict.parse(sMsg)['xml']

    global MSG_IDS
    if 'MsgId' in dMsg:
        if dMsg['MsgId'] in MSG_IDS:
            current_app.logger.warning(
                f"Receive dumplicated Message, MsgId is {dMsg['MsgId']}")
            return
        else:
            MSG_IDS.appendleft(dMsg['MsgId'])

    if not 'MsgType' in dMsg:
        current_app.logger.error('Can not find MsgType element in xml')
        raise werkzeug.exceptions.BadRequest()

    session['state'] = request.args['msg_signature']
    external_url = current_app.config['EXTERNAL_URL']
    url = external_url + url_for('host.hostlist', q=dMsg.get('Content'), fromuser=dMsg.get(
        'FromUserName'), state=request.args['msg_signature']) if external_url else None

    _inner = f'<a href=\"{url}\">{dMsg.get("Content")}</a>' if isIP(dMsg.get("Content")) else dMsg.get("Content")
    content = f'收到\"{_inner}\"查询请求, <a href=\"{url}\">点击链接查看查询结果</a>'

    dRsp = {'xml': {
        'ToUserName': dMsg.get('FromUserName'),
        'FromUserName': dMsg.get('ToUserName'),
        'CreateTime': request.args.get('timestamp'),
        'MsgType': 'text',
        'Content': content
    }}

    ret, sEncryptMsg = wxcpt.EncryptMsg(
        xmltodict.unparse(dRsp), request.args['nonce'], request.args['timestamp'])
    if ret:
        current_app.logger.error(f'EncryptMsg ret: {ret}')
        raise werkzeug.exceptions.InternalServerError()
    current_app.logger.debug(f'EncryptMsg is {sEncryptMsg}')

    return sEncryptMsg

