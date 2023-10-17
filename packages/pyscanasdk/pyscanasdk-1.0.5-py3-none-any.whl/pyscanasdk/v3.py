# -*- coding: utf-8 -*-
import requests
import hashlib
import time
from urllib.parse import urlparse, parse_qsl, parse_qs


# https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-the-package-files
class ModerateClient(object):
    def __init__(self, app_id, secret_key, text_business_id='', img_business_id='', audio_business_id='',
                 video_business_id='', doc_business_id=''):
        """
        :param app_id: 获取来的appid
        :param secret_key: 获取到的和appid对应的secret_key
        :param text_business_id: 文本审核的业务id
        :return:
        """
        self.app_id = app_id
        self.secret_key = secret_key
        self.text_business_id = text_business_id
        self.img_business_id = img_business_id
        self.audio_business_id = audio_business_id
        self.video_business_id = video_business_id
        self.doc_business_id = doc_business_id

    def text(self, content, ac=False, extra="", timeout=10):
        """
        文本审核的接口
        :param content: 待审核的文本内容
        :param ac: False同步/True异步
        :param timeout: 超时时间，单位秒
        :param extra: 透传字段
        :return:
        """
        if not self.text_business_id:
            return {"msg": "文本business_id不能为空!"}
        url = "https://newkmsapi.qixincha.com/kms-open/v3/text/sync"
        async_url = "https://newkmsapi.qixincha.com/kms-open/v3/text/async"
        moderation_url = async_url if ac else url
        data = {
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "businessId": self.text_business_id,
            "text": content,
            "extra": extra
        }
        resp = requests.post(url=moderation_url, json=data, timeout=timeout)
        return resp.json()

    def image(self, content, ac=False, extra="", timeout=10):
        """
        图片审核的接口
        :param content: 待审核的图片
        :param ac: False同步/True异步
        :param timeout: 超时时间，单位秒
        :param extra: 透传字段
        :return:
        """
        if not self.img_business_id:
            return {"msg": "图片business_id不能为空!"}
        url = "https://newkmsapi.qixincha.com/kms-open/v3/image/sync"
        async_url = "https://newkmsapi.qixincha.com/kms-open/v3/image/async"
        moderation_url = async_url if ac else url
        data = {
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "businessId": self.img_business_id,
            "images": content,
            "extra": extra
        }
        resp = requests.post(url=moderation_url, json=data, timeout=timeout)
        return resp.json()

    def audio(self, content, extra="", timeout=10):
        """
        图片审核的接口
        :param content: 待审核的音频
        :param timeout: 超时时间，单位秒
        :param extra: 透传字段
        :return:
        """
        if not self.audio_business_id:
            return {"msg": "音频business_id不能为空!"}
        async_url = "https://newkmsapi.qixincha.com/kms-open/v3/audio/async"
        moderation_url = async_url
        data = {
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "businessId": self.audio_business_id,
            "url": content,
            "extra": extra
        }
        resp = requests.post(url=moderation_url, json=data, timeout=timeout)
        return resp.json()

    def video(self, content, extra="", timeout=10):
        """
        图片审核的接口
        :param content: 待审核的视频
        :param timeout: 超时时间，单位秒
        :param extra: 透传字段
        :return:
        """
        if not self.video_business_id:
            return {"msg": "视频business_id不能为空!"}
        async_url = "https://newkmsapi.qixincha.com/kms-open/v3/video/async"
        moderation_url = async_url
        data = {
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "businessId": self.video_business_id,
            "url": content,
            "extra": extra
        }
        resp = requests.post(url=moderation_url, json=data, timeout=timeout)
        return resp.json()

    def doc(self, content, extra="", timeout=10):
        """
        文档审核的接口
        :param content: 待审核的文档
        :param timeout: 超时时间，单位秒
        :param extra: 透传字段
        :return:
        """
        if not self.doc_business_id:
            return {"msg": "文档business_id不能为空!"}
        async_url = "https://newkmsapi.qixincha.com/kms-open/v3/doc/async"
        moderation_url = async_url
        data = {
            "appId": self.app_id,
            "secretKey": self.secret_key,
            "businessId": self.doc_business_id,
            "url": content,
            "extra": extra
        }
        resp = requests.post(url=moderation_url, json=data, timeout=timeout)
        return resp.json()

    def gen_signature(self, business_id, timestamp, nonce):
        """生成签名信息
        Args: business_id 业务id
        timestamp 时间戳
        nonce 随机数 不要取0
        Returns: 参数签名md5值
        """
        if not any([business_id, timestamp, nonce]):
            print('businessId,timestamp,nonce不能为空！')
            return ''
        params = {"nonce": nonce, "timestamp": timestamp, 'businessId': business_id}
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff.encode('utf8')).hexdigest()

    @staticmethod
    def check_empty(lst):
        return not any(not bool(item) for item in lst)

    def validate_signature_by_url(self, url):
        """生成签名信息
        Args: params url 回调地址
        Returns: 参数签名md5值
        """
        if not url.startswith('http'):
            url += 'https://www.baidu.com/?'
        query_dict = parse_qs(urlparse(url).query)
        business_id = query_dict.get('businessId', '[]')
        nonce = query_dict.get('nonce', [])
        timestamp = query_dict.get('timestamp', [])
        signature = query_dict.get('signature', [])
        if not self.check_empty([business_id, nonce, timestamp, signature]):
            print('请检查query是否完整，或nonce的值是否为0,signature是否为空')
            return False
        timestamp = timestamp[0]
        if int(time.time()) - int(timestamp) > 300:
            print('超时了')
            return False
        signature = signature[0]
        params = {}
        query_dict = parse_qsl(urlparse(url).query)
        [params.update({item[0]: item[1]}) for item in query_dict]
        del params['signature']
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        result = hashlib.md5(buff.encode('utf8')).hexdigest()
        return result == signature
