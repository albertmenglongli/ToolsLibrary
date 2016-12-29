# -*- coding:utf-8 -*-


from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from urllib import quote_plus
from string import Template
import datetime
import operator
import base64
import time
import json

__author__ = "Menglong.li"


class AliPay:
    def __init__(self, based64_encoded_rsa_private_key_pkcs8, alipay_verification_public_key):
        self.based64_encoded_rsa_private_key_pkcs8 = based64_encoded_rsa_private_key_pkcs8
        self.alipay_verification_public_key = alipay_verification_public_key

    def generate_order_string(self, app_id_for_alipay, subject, out_trade_no, total_amount, notify_url):
        def _sign_string(message):
            _key = RSA.importKey(base64.decodestring(self.based64_encoded_rsa_private_key_pkcs8))
            _signer = PKCS1_v1_5.new(_key)
            _signature = _signer.sign(SHA.new(message.encode('utf8')))
            return base64.encodestring(_signature).decode('utf8').replace('\n', '')

        _order_string = ''
        try:
            _params = {
                'app_id': str(app_id_for_alipay),
                'method': 'alipay.trade.app.pay',
                'charset': 'utf-8',
                'sign_type': 'RSA',
                'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'version': '1.0',
                'notify_url': notify_url,
                'biz_content': {
                    'out_trade_no': str(out_trade_no),
                    'product_code': 'QUICK_MSECURITY_PAY',
                    'subject': subject,
                    'total_amount': "%.2f" % float(total_amount),
                }
            }

            # Replace value, which is a dict, with its dumps json string value
            # PS: For AliPay, keys inside of biz_content don't have to be sorted.
            [operator.setitem(_params, key, json.dumps(value, separators=(',', ':'), sort_keys=True)) for key, value in _params.items() if type(value) is dict]

            _unsigned_string = '&'.join('{}={}'.format(key, str(value)) for (key, value) in sorted(_params.iteritems()))
            _order_string_prefix = '&'.join('{}={}'.format(key, quote_plus(str(value))) for (key, value) in sorted(_params.iteritems()))
            _order_string = ''.join([_order_string_prefix, '&sign=', quote_plus(_sign_string(_unsigned_string))])
        except Exception as e:
            # handle all the exceptions when generate the order string, and just return order_string = ''
            pass
        return _order_string

    def verify_signature(self, data_dict):
        def _verify_signature(message, signature, sign_type):
            # Only 'RSA' Type Supported
            if sign_type.upper() == 'RSA':
                h = SHA.new(message.encode('utf-8'))
                verifier = PKCS1_v1_5.new(RSA.importKey(base64.decodestring(self.alipay_verification_public_key)))
                return verifier.verify(h, base64.decodestring(signature.encode('utf-8')))
            else:
                raise Exception(Template('Sign type $sign_type not supported').substitute(sign_type=sign_type))

        _sign = data_dict.get('sign', '')
        _sign_type = data_dict.get('sign_type', '')

        # Filter out the sign, sign_type field, and join other key value in format k1=v1&k2=v2 (keys in order)
        _string_to_verify = "&".join(['{}={}'.format(key, str(value)) for (key, value) in sorted(data_dict.items()) if key not in {'sign', 'sign_type'}])
        return _verify_signature(message=_string_to_verify, signature=_sign, sign_type=_sign_type)
