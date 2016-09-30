# -*- coding: utf-8 -*-
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PK
from Crypto.Hash import SHA
import json
from datetime import datetime
try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode
try:
    import urllib2
except:
    from urllib import request as urllib2


class AliPayClient(object):

    def __init__(self):
        self.gateway = "https://openapi.alipay.com/gateway.do"
        self.app_id = ""
        self.format = "JSON"
        self.method = ""
        self.charset = "utf-8"
        self.sign_type = "RSA"
        self.timestamp = ""
        self.version = "1.0"
        self.notify_url = ""
        self.app_auth_token = ""
        self.biz_content = ""

    def _sys_params(self):
        data = {
            "app_id": self.app_id,
            "format": self.format,
            "method": self.method,
            "charset": self.charset,
            "sign_type": self.sign_type,
            "timestamp":
                datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            "version": self.version,
            "app_auth_token": self.app_auth_token,
            "notify_url": self.notify_url,
        }
        self.sys_params = data
        return self.sys_params

    def _api_params(self):
        data = {
            "biz_content": self.biz_content,
        }
        self.api_params = data
        return self.api_params

    def _check_empty(self, key, **params):
        return params.get(key) != "" and not None

    def _get_sign_content(self, **params):
        redata = []
        sorted_params = sorted(params)
        for k in sorted_params:
            if self._check_empty(k, **params):
                element = "{0}={1}".format(k, params[k])
                redata.append(element)
        sign_content = "&".join(redata)
        return sign_content

    def _get_verify_content(self, **params):
        redata = []
        sorted_params = sorted(params)
        for k in sorted_params:
            if self._check_empty(k, **params):
                element = '\"{0}\":\"{1}\"'.format(k, params[k])
                redata.append(element)
        sign_content = ",".join(redata)
        return "{%s}" % sign_content

    def _get_sign_with_sha1(self, private_key, content):
        key = RSA.importKey(private_key)
        h = SHA.new(content.encode("utf-8"))
        signer = PK.new(key)
        sign = signer.sign(h)
        return base64.b64encode(sign).decode("utf-8")

    def request(self):
        totalParams = self._sys_params().copy()
        totalParams.update(self._api_params())
        signcontent = self._get_sign_content(**totalParams)
        with open(self.private_key_path) as f:
            private_key = f.read()
        sign = self._get_sign_with_sha1(private_key, signcontent)
        self.sys_params["sign"] = sign
        querys = urlencode(self.sys_params)
        post_data = urlencode(self.api_params)
        url = "{0}?{1}".format(self.gateway, querys)
        response = urllib2.urlopen(url, post_data).read().decode("utf-8")
        print response
        self._response = json.loads(response)
        return self._response

    def verify(self):
        with open(self.alipay_public_key_path) as f:
            alipay_public_key = f.read()
        pub_key = RSA.importKey(alipay_public_key)
        verifier = PK.new(pub_key)
        sign = self._response.get('sign', "")
        params = self._response["_".join(self.method.split(".")) + "_response"]
        content = self._get_verify_content(**params)
        data = SHA.new(content.encode(self.charset))
        return verifier.verify(data, base64.b64decode(sign))
