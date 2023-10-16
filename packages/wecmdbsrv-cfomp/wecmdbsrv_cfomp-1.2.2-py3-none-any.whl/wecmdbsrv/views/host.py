#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import base64
import os
from urllib.parse import quote
from elasticsearch import Elasticsearch
from flask import request, session, render_template, current_app, url_for, redirect, Blueprint

bp = Blueprint("host", __name__)


def authorize_url_and_session():
    state = request.args['state']
    myredirect = base64.b64encode(request.full_path.encode())
    redirect_url = quote(
        current_app.config['EXTERNAL_URL'] + url_for('oauth.oauthredirect', myredirect=myredirect))
    session['state'] = state
    session['UserId'] = request.args['fromuser']
    wx_authrize = f"https://open.weixin.qq.com/connect/oauth2/authorize?"\
        f"appid={current_app.config['WEWORK_CORPID']}&redirect_uri={redirect_url}&response_type=code"\
        f"&scope=snsapi_base&state={state}#wechat_redirect"

    return wx_authrize


@bp.route("/hostlist/", methods=["GET"])
def hostlist():
    if not session.get("Authorized"):
        return redirect(authorize_url_and_session())
    from_ = int(request.args.get("from", 0))
    size = int(request.args.get("size", current_app.config.get("ES_SIZE")))
    from_ = 0 if from_ < 0 else from_
    size = 1 if size < 0 else size
    es = Elasticsearch(os.environ.get("ES_HOSTS"))
    index = f"zabbix-raw-host-info-{time.strftime('%Y.%m.%d', time.localtime())}"
    res = es.search(
        index=index,
        q=request.args.get("q"),
        timeout=current_app.config.get("ES_TIMEOUT"),
        from_=from_,
        size=current_app.config.get("ES_SIZE")
    )
    return render_template("hostlist.html.j2", data=res, from_=from_, size=size)


@bp.route("/hostdetail/<id>", methods=["GET"])
def hostdetail(id):
    if not session.get('Authorized'):
        return redirect(authorize_url_and_session())
    es = Elasticsearch(os.environ.get("ES_HOSTS"))
    index = f"zabbix-raw-host-info-{time.strftime('%Y.%m.%d', time.localtime())}"
    source_ = es.get(index=index, id=id).get("_source")
    inventory = source_.get("inventory")
    interfaces = source_.get("interfaces")
    groups = source_.get("groups")
    data = {
        "主机名称": inventory.get("name") if inventory else "",
        "主机别名": inventory.get("alias") if inventory else "",
        "接口地址": ", ".join(
            [interface.get("ip") for interface in interfaces]
        ) if interfaces else "",
        "主机组": ", ".join(
            [group.get("name") for group in groups]
        ) if groups else "",
        "OS": inventory.get("os") if inventory else "",
        "OS_FULL": inventory.get("os_full") if inventory else "",
        "OS_SHORT": inventory.get("os_short") if inventory else "",
        "资产标签": inventory.get("asset_tag") if inventory else "",
        "负责人":
            inventory.get("poc_1_name") + " " + inventory.get("poc_2_name")
            if inventory else "",
        "机架": inventory.get("chassis") if inventory else "",
        "子网掩码": inventory.get("host_netmask") if inventory else "",
        "主机网络": inventory.get("host_networks") if inventory else "",
        "机房": inventory.get("location") if inventory else "",
        "机柜": inventory.get("site_rack") if inventory else "",
        "序列号": inventory.get("serialno_a") if inventory else "",
        "管理IP": inventory.get("oob_ip") if inventory else "",
        "MAC":
            inventory.get("macaddress_a") + " " + inventory.get("macaddress_b")
            if inventory else "",
        "硬件架构": inventory.get("hw_arch") if inventory else "",
        "标签": inventory.get("tag") if inventory else "",
        "类型": inventory.get("type") if inventory else "",
        "具体类型": inventory.get("type_full") if inventory else "",
        "型号": inventory.get("model") if inventory else "",
        "供应商": inventory.get("vendor") if inventory else "",
    }
    return render_template("hostdetail.html.j2", data=data)
