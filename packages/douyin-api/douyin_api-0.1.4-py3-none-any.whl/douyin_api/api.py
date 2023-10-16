"""
抖音官方开放接口

抖音官方文档地址：https://developer.open-douyin.com/docs/resource/zh-CN/dop/overview/usage-guide

注：上传文件需要 requests-toolbelt
"""

import os
import json
import time
import hashlib
import random
from pathlib import Path
from pprint import pprint as pp

import requests

from requests import Response
from requests_toolbelt import MultipartEncoder
from urllib.parse import urlparse

from .utils import need_login, BaseClient
from .exception import LoginError, NeedAccessTokenException

HEADERS_JSON = {
    "Content-Type": "application/json",  # application/json;charset=UTF-8
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}

HEADERS_X_WWW_FORM_URLENCODED = {
    "Content-Type": "application/x-www-form-urlencoded",
}


class DouYin(BaseClient):

    def __init__(self, client_key, client_secret, base_url='https://open.douyin.com', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_key = client_key  # 应用唯一标识
        self.client_secret = client_secret  # 应用唯一标识对应的密钥
        self.base_url = base_url
        self.set_headers(HEADERS_JSON)
        self.data = {}
        self._access_token = None
        self._open_id = None

    def set_access_token(self, access_token, open_id):
        """
        设置用户授权
        """
        headers = {
            "Content-Type": "application/json",
            "access-token": access_token,
        }
        self.set_headers(headers)
        # 我们获取消息数量，检查是否已经登录成功

        self._access_token = access_token
        self._open_id = open_id

    def need_access_token(self):
        """
        检查是否已登录，我们还是只简单检查有没有 access_token
        """
        # self.get_count_message()
        if self._access_token is None:
            raise NeedAccessTokenException()

    def get_response_data(self, resp):
        """
        解析接口返回的数据
        """
        try:
            self.data = resp.json()
        except Exception as e:
            return {
                "data": {
                    "description": f"转换json数据失败：{e}",
                    "error_code": 88888888,
                }
            }

        # 我们不检查信息是否错误，在获取信息的时候在检查
        # if self.data['data'].get('error_code', None) != 0:
        #     raise ValueError(f'{self.data}')

        return self.data

    def client_token(self, ):
        """
        该接口用于获取接口调用的凭证 client_token。该接口适用于抖音授权。

        业务场景
        client_token 用于不需要用户授权就可以调用的接口。

        注意事项
        client_token 的有效时间为 2 个小时，重复获取 client_token 后会使上次的 client_token 失效（但有 5 分钟的缓冲时间，连续多次获取 client_token 只会保留最新的两个 client_token）。

        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/client-token
        """
        data = {
            "grant_type": "client_credential",
            "client_key": self.client_key,
            "client_secret": self.client_secret,
        }
        url = f"{self.base_url}/oauth/client_token/"
        r = self._session.post(url, json=data)
        return self.get_response_data(r)

    def get_permission_code_url(self, scope, redirect_uri, state=None):
        """
        该接口只适用于抖音获取授权临时票据（code）。请求该 URL，会跳转到开放平台提供的授权扫码页，用户扫码即可授权。
        前提条件
        需要去官网为应用申请 scope 的使用权限。
        需要在本接口的 scope 传参中填上需要用户授权的 scope，多个 scope 以逗号分割。
        用户授权通过后，应用有权限通过 access_token 调用相应接口。

        注意事项
        抖音的 OAuth API 以 https://open.douyin.com 开头
        打开该 URL 后，页面会出现一个二维码，用户扫描该二维码即可授权。在抖音 App 支持端内唤醒的版本内打开的话会弹出客户端原生授权页面。
        获取的 code 可以用来调用 https://open.douyin.com/oauth/access_token/ 换取用户 acccess_token。

        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/douyin-get-permission-code
              https://open.douyin.com/platform/oauth/connect
        """
        url = f'https://open.douyin.com/platform/oauth/connect?client_key={self.client_key}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&state={state}'
        return url

    def access_token(self, code):
        """
        该接口用于获取用户授权第三方接口调用的凭证 access_token；该接口适用于抖音授权

        使用限制
        无

        业务场景
        access_token 为用户授权第三方接口调用的凭证，存储在客户端，可能会被窃取，泄露后可能会发生用户隐私数据泄露的风险，建议存储在服务端

        注意事项
        获取到 access_token 后授权临时票据 (code) 不要再授权刷新，否则会导致上一次获取的 code 过期。
        Scope: 无
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/get-access-token
        """
        data = {
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "client_key": self.client_key,
        }
        url = f"{self.base_url}/oauth/access_token/"
        r = self._session.post(url, json=data)
        return self.get_response_data(r)

    def renew_refresh_token(self, refresh_token):
        """
        该接口用于刷新 refresh_token 的有效期，适用于抖音授权

        使用前提
        client_key 必须拥有 renew_refresh_token 权限

        注意事项
        抖音的 OAuth API 以https://open.douyin.com/ 开头
        刷新操作需要在 refresh_token 过期前进行
        通过旧的 refresh_token 获取新的 refresh_token，调用后旧 refresh_token 会失效，新 refresh_token 有 30 天有效期。最多只能获取 5 次新的 refresh_token，5 次过后需要用户重新授权

        Scope: 无
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/refresh-token
        """
        data = {
            "client_key": self.client_key,
            "refresh_token": refresh_token,
        }
        # print(data)
        url = f"{self.base_url}/oauth/renew_refresh_token/"
        r = requests.post(url, data=data, headers=HEADERS_X_WWW_FORM_URLENCODED)
        return self.get_response_data(r)

    def refresh_token(self, refresh_token):
        """
        该接口用于刷新 access_token 的有效期，适用于抖音授权

        access_token 有效期说明
        当 access_token 过期（过期时间 15 天）后，可以通过该接口使用 refresh_token（过期时间 30 天）进行刷新。刷新后获得一个有效期为15天的 access_token，但是 refresh_token 的有效期保持不变。
        若 refresh_token 过期，获取 access_token 会报错（error_code=10010），此时需要重新引导用户授权。
        用户可以在抖音-我-设置（右上角）-帐号与安全-授权管理 中取消对应用的授权，取消授权后原有 access_token 会立即失效。
        抖音开放平台会定期对用户授权进行检查，取消不合规的 access_token 授权。

        Scope: 无
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/refresh-access-token
        """
        data = {
            "grant_type": "refresh_token",
            "client_key": self.client_key,
            "refresh_token": refresh_token,
        }
        url = f"{self.base_url}/oauth/refresh_token/"
        r = requests.post(url, data=data, headers=HEADERS_X_WWW_FORM_URLENCODED)
        return self.get_response_data(r)

    def get_jsb_ticket(self):
        """
        该接口用于获取 jsapi_ticket；需要申请权限，不需要用户授权。本接口适用于抖音

        注意：
        抖音的OAuth API以https://open.douyin.com/开头。
        jsapi_ticket（同一个ticket的有效期大约在7200秒左右，开发者需要根据接口实际返回的过期时间为准）。

        Scope: js.ticket
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/tools-ability/jsb-management/get-jsb-ticket
        """
        headers = {
            "access-token": self.client_token()['data']['access_token'],
            "Content-Type": "application/json",
        }
        url = f"{self.base_url}/js/getticket/"
        r = requests.post(url, headers=headers)
        return self.get_response_data(r)

    def userinfo(self):
        """
        该接口获取用户的抖音公开信息，包含昵称和头像，适用于抖音、抖音极速版。

        注意事项
        若需要获取用户手机号，需要用户额外授权 mobile_alert 权限，本接口会额外返回 encrypt_mobile 字段，详见获取用户手机号。
        为加强用户隐私保护，抖音支持用户选择虚拟头像和昵称，若获取到的昵称头像为以下数据，则表明用户选择了虚拟身份。

        Scope: user_info
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-management/get-account-open-info
        """
        self.need_access_token()
        data = {
            "access_token": self._access_token,
            "open_id": self._open_id,
        }
        url = f"{self.base_url}/oauth/userinfo/"
        r = requests.post(url, data=data, headers=HEADERS_X_WWW_FORM_URLENCODED)
        return self.get_response_data(r)

    def fans(self, date_type=7):
        """
        该接口用于获取用户粉丝数

        open_id	通过/oauth/access_token/获取，用户唯一标志	ba253642-0590-40bc-9bdf-9a1334b94059
        date_type	近7/15天；输入7代表7天、15代表15天、30代表30天

        需要申请权限。路径：抖音开放平台控制台 > 应用详情 > 能力管理 > 数据权限
        需要用户授权
        注：用户首次授权应用后，需要第二天才会产生全部的数据。

        Scope: data.external.user
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/server/data-open/user-homepage-data/get-user-fans-count
        """
        self.need_access_token()
        url = f"{self.base_url}/data/external/user/fans/?open_id={self._open_id}&date_type={date_type}"
        r = self._session.get(url, )
        return self.get_response_data(r)

    def video_list(self, cursor=0, count=10):
        """
        该接口用于分页获取用户所有视频的数据，返回的数据是实时的。该接口适用于抖音

        cursor: 分页游标, 第一页请求cursor是0, response中会返回下一页请求用到的cursor, 同时response还会返回has_more来表明是否有更多的数据
        count: 每页数量

        注意：
        抖音的 OAuth API 以https://open.douyin.com/开头。
        目前暂不支持时间过滤，但相关功能正在评估开发中

        Scope: video.list.bind
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/search-video/account-video-list/
        """
        self.need_access_token()
        url = f"{self.base_url}/api/douyin/v1/video/video_list/?open_id={self._open_id}&cursor={cursor}&count={count}"
        r = self._session.get(url, )
        return self.get_response_data(r)

    def video_data(self, ids, use_item_ids=True):
        """
        该接口用于查询用户特定视频的数据，如点赞数、播放数等，返回的数据是实时的。该接口适用于抖音

        可以使用 item_id 或 video_id 列表，仅能查询 access_token 对应用户上传的视频（与 video_ids 字段二选一，平台优先处理 item_ids）

        注意事项
        抖音的 OAuth API 以https://open.douyin.com/ 开头。
        可以通过videoid转换itemid，获取 item_id（抖音视频 id），也可以通过"查询视频发布结果"获取 item_id（抖音视频 id）
        只返回用户公开的视频数据，未公开的视频数据不会返回。
        如果视频设置为了隐私，则返回创建时间为 0 的记录。

        Scope: video.data.bind
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/search-video/video-data
        查询视频发布结果: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/search-video/video-share-result
        """
        self.need_access_token()
        if use_item_ids:
            data = {"item_ids": ids, }
        else:
            data = {"video_ids": ids, }

        url = f"{self.base_url}/api/douyin/v1/video/video_data/?open_id={self._open_id}"
        r = self._session.post(url, json=data)
        return self.get_response_data(r)
