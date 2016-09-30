# alipay_python_sdk

## 说明

关于支付宝接口的完全使用方式,请参考阿里官方文档 [文档目录](https://doc.open.alipay.com/) [API目录](https://doc.open.alipay.com/doc2/apiList?docType=4)

本项目仅抽象调用过程,方便py开发者与alipay对接

## 安装依赖

```bash
git clone https://github.com/lioncui/alipay_python_sdk
cd alipay_python_sdk
pip install pycrypto
```

## 请求示例

```py
Python 2.7.10 (default, Oct 23 2015, 19:19:21) 
[GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.59.5)] on darwin
Type "help", "copyright", "credits" or "license" for more information
>>> from alipay_python_sdk import AliPayClient
>>> ali = AliPayClient()
>>> ali.gateway = "https://openapi.alipay.com/gateway.do"
>>> ali.app_id = "2016081612345678"
>>> ali.private_key_path = "/secret/private.pem"
>>> ali.method = "monitor.heartbeat.syn"
>>> ali.biz_content = "{}"
>>> ali.request()
{u'monitor_heartbeat_syn_response': {u'msg': u'Success', u'code': u'10000', u'pid': u'2016081612345678'}, u'sign': u'ndNbTnj62ZSW3YV2TkMher96IUP37kYrZvEsiqd1ce8I6iAH8GLgiYAyojJ6+xXrWk3enTOvWRPRBOIqwS+TZEiKPdDbllz9BZMn2KkZSHy7XllzlBw0LfSyfTmO/O5qZycNMC4a5ZkLF4gaaBasyrM4SRskg4eaPzzFiC5EDvM='}
```