import json
import string
import hashlib
import random
import time
import urllib

import requests

from main.settings import BASE_DIR
from django.core.cache import cache
from pathlib import Path
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from ..utils.model_handle import parse_data, util_response

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

appid = main_config_dict.wechat_subscription_app_id or module_config_dict.wechat_subscription_app_id or ""
sceret = main_config_dict.wechat_subscription_app_secret or module_config_dict.wechat_subscription_app_secret or ""

sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""
sub_app_secret = main_config_dict.wechat_merchant_app_secret or module_config_dict.wechat_merchant_app_secret or ""

subscription_app_id = main_config_dict.wechat_subscription_app_id or module_config_dict.wechat_subscription_app_id or ""
subscription_app_secret = main_config_dict.wechat_subscription_app_secret or module_config_dict.wechat_subscription_app_secret or ""


class Sign:

    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))  # 创建随机字符串

    def __create_timestamp(self):
        return int(time.time())  # 创建一个时间戳

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])  # 根据字符的ASCII值进行排序，拼接
        self.ret['signature'] = hashlib.sha1(string.encode('utf-8')).hexdigest()  # 对字符串进行sha1加密
        return self.ret


def get_token(type, identifying=""):
    if type == "APPLET":
        appid = sub_appid
        sceret = sub_app_secret
    else:
        appid = subscription_app_id
        sceret = subscription_app_secret
    # ACCESS_TOKEN = cache.get('wx:' + str(identifying) + '_ACCESS_TOKEN')  # 从redis中获取ACCESS_TOKEN
    # print(ACCESS_TOKEN)

    # if ACCESS_TOKEN:
        # print('wx:' + str(type) + '_ACCESS_TOKEN', ACCESS_TOKEN)
        # return ACCESS_TOKEN
    try:
        token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
            appid, sceret)  # 创建获取token的url
        print(token_url)
        response = urllib.request.urlopen(token_url)
        b = response.read().decode('utf-8')
        token = json.loads(b)
        ACCESS_TOKEN = token.get("access_token")
        # cache.set('wx:' + str(identifying) + '_ACCESS_TOKEN', ACCESS_TOKEN,
        #           7200)  # 将获取到的 ACCESS_TOKEN 存入redis中并且设置过期时间为7200s
        # print("2", ACCESS_TOKEN)
        return ACCESS_TOKEN
    except Exception as e:
        return e


def get_ticket():
    ticket = cache.get('wx:ticket')  # 获取redis数据库中ticket
    if ticket:
        tic = str(ticket)
        return tic
    else:
        try:
            token = get_token("SUBSCRIBE")
            ticket_url = " https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi".format(token)
            get_ticket = urllib.request.urlopen(ticket_url)
            c = get_ticket.read().decode("utf-8")
            js_ticket = json.loads(c)
            ticket = js_ticket.get("ticket")
            cache.set('wx:ticket', ticket, 7200)
            return ticket
        except Exception as e:
            return e


# 小程序发送模板
def applet_subscribe_message(json):
    """
        属性	            类型	必填	说明
        access_token	    string	是	    接口调用凭证，该参数为 URL 参数，非 Body 参数。使用access_token或者authorizer_access_token
        template_id	        string	是	    所需下发的订阅模板id
        page	            string	否	    点击模板卡片后的跳转页面，仅限本小程序内的页面。支持带参数,（示例index?foo=bar）。该字段不填则模板无跳转
        touser	            string	是	    接收者（用户）的 openid
        data	            string	是	    模板内容，格式形如 { "key1": { "value": any }, "key2": { "value": any } }的object
        miniprogram_state	string	是	    跳转小程序类型：developer为开发版；trial为体验版；formal为正式版；默认为正式版
        lang	            string	是	    进入小程序查看”的语言类型，支持zh_CN(简体中文)、en_US(英文)、zh_HK(繁体中文)、zh_TW(繁体中文)，默认为zh_CN
        返回参数
        :return:
    """
    try:
        token = get_token("APPLET", json['touser'])
        subscribe_message_url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}".format(
            token)
        header = {'content-type': 'application/json'}
        response = requests.post(subscribe_message_url, json=json, headers=header).json()
        return response
    except Exception as e:
        return e


# 公众号发送模板(订阅消息)
def subscribe_message(json):
    """
        属性	        类型	        必填	说明
        access_token	string		    是	    接口调用凭证
        tid	            string		    是	    模板标题 id，可通过getPubTemplateTitleList接口获取，也可登录公众号后台查看获取
        kidList     	Array.<number>	是	    开发者自行组合好的模板关键词列表，关键词顺序可以自由搭配（例如 [3,5,4] 或 [4,5,3]），最多支持5个，最少2个关键词组合
        sceneDesc	    string		    是	    服务场景描述，15个字以内
        :return:
    """
    try:
        token = get_token("SUBSCRIBE", json['touser'])
        subscribe_message_url = "https://api.weixin.qq.com/cgi-bin/message/subscribe/bizsend?access_token={}".format(
            token)
        header = {'content-type': 'application/json'}
        response = requests.post(subscribe_message_url, json=json, headers=header).json()
        return response
    except Exception as e:
        return e

def template_message(json):
    """
        属性	        类型	        必填	说明
        access_token	string		    是	    接口调用凭证
        tid	            string		    是	    模板标题 id，可通过getPubTemplateTitleList接口获取，也可登录公众号后台查看获取
        kidList     	Array.<number>	是	    开发者自行组合好的模板关键词列表，关键词顺序可以自由搭配（例如 [3,5,4] 或 [4,5,3]），最多支持5个，最少2个关键词组合
        sceneDesc	    string		    是	    服务场景描述，15个字以内
        :return:
    """
    try:
        token = get_token("SUBSCRIBE", json['touser'])
        print(token)
        subscribe_message_url = "https://api.weixin.qq.com/cgi-bin/message/template/send??access_token={}".format(
            token)
        header = {'content-type': 'application/json'}
        response = requests.post(subscribe_message_url, json=json, headers=header).json()
        return response
    except Exception as e:
        return e

def jssdk_config(url):
    ticket = get_ticket()
    sign = Sign(ticket, url)
    data = sign.sign()
    result = {
        "appId": appid,
        "nonceStr": data['nonceStr'],
        "jsapi_ticket": data['jsapi_ticket'],
        "timestamp": data['timestamp'],
        "url": data['url'],
        "signature": data['signature'],
    }
    return result
