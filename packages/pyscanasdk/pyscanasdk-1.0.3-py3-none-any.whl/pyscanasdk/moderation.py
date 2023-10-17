# -*- coding: utf-8 -*-
import requests
import hashlib
import time


# https://packaging.python.org/en/latest/tutorials/packaging-projects/#creating-the-package-files
class ModerateClient(object):
    def __init__(self, app_id, secret_key, text_business_id):
        """
        :param app_id: 获取来的appid
        :param secret_key: 获取到的和appid对应的secret_key
        :param text_business_id: 文本审核的业务id
        :return:
        """
        self.app_id = app_id
        self.secret_key = secret_key
        self.text_business_id = text_business_id

    def text_moderation(self, content, timeout=10):
        """
        文本审核的接口
        :param content: 待审核的文本内容
        :param timeout: 超时时间，单位秒
        :return:
        """
        text_moderation_url = "https://newkmsapi.qixincha.com/kms-open/v2/openapi/synctextmoderation"
        suffix = self.essemble_signature()
        text_moderation_url += "?"
        text_moderation_url += suffix
        data = {
            "business_id": self.text_business_id,
            "text": content,
        }
        resp = requests.post(url=text_moderation_url, json=data, timeout=timeout).json()
        return resp

    def gen_signature(self, params):
        """生成签名信息
        Args: params (object) 请求参数
        Returns: 参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff.encode('utf8')).hexdigest()

    def essemble_signature(self):
        params = {
            "businessId": self.text_business_id,
            "nonce": 1,
            "appId": self.app_id,
            "timestamp": int(time.time())
        }
        signature = self.gen_signature(params=params)
        buff = ""
        for k in params.keys():
            buff += f"{str(k)}={params[k]}"
            buff += '&'
        buff += f"signature={signature}"
        return buff
