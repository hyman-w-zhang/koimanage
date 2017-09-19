import requests
import datetime
import pytz
import time
from collections import OrderedDict
from urllib.parse import quote
from hashlib import sha1
import base64
import hmac


ali_cdn_api = 'http://cdn.aliyuncs.com/'

time_zone_utc = pytz.timezone('UTC')

ali_cdn_api_format = 'JSON'
ali_cdn_api_version = '2014-11-11'

access_key_id = 'WQJC0JqAfgIe3Msh'
access_key_secret = 'ucUzDnwidx1Q3lqXCAlbFKxluQMIWf' + '&'

signature_method = 'HMAC-SHA1'
signature_version = '1.0'

http_method = 'GET'


def custom_quote(uri):
    return quote(string=uri, safe='-_.~', encoding='utf-8')


def refresh_cdn_cache(url):
    time_stamp = datetime.datetime.now(tz=time_zone_utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    signature_nonce = str(int(time.time() * 10000000))
    params = {
        'SignatureVersion': signature_version,
        'Format': ali_cdn_api_format,
        'Timestamp': time_stamp,
        'AccessKeyId': access_key_id,
        'SignatureMethod': signature_method,
        'Version': ali_cdn_api_version,
        # 'Action': 'RefreshObjectCaches',
        'Action': 'DescribeRefreshQuota',
        'SignatureNonce': signature_nonce,
        # 'ObjectPath': url,
        # 'ObjectType': 'File',
    }
    canonicalized_query_string = OrderedDict(sorted(params.items()))
    string_to_sign = http_method + '&%2F'
    for k, v in canonicalized_query_string.items():
        string_to_sign += ('&' + custom_quote(k + '=' + v))
    print(string_to_sign)
    key = bytes(access_key_secret, encoding='utf-8')
    msg = bytes(string_to_sign, encoding='utf-8')
    hmac_content = hmac.new(key=key, msg=msg, digestmod=sha1)
    signature = base64.b64encode(hmac_content.digest())
    print(signature)
    params['Signature'] = quote(str(signature, encoding='utf-8'), safe='')
    '''
    resp = requests.get(url=ali_cdn_api, params=params)
    print(resp.status_code)
    print(resp.content.decode())
    '''
    query_string = ''
    for k, v in params.items():
        query_string += (k + '=' + custom_quote(v) + '&')

    print(ali_cdn_api + '?' + query_string.strip('&'))

def _test_calc_hmac():
    string_to_sign = 'GET&%2F&AccessKeyId%3Dtestid&Action%3DDescribeCdnService&Format%3DJSON&SignatureMethod%3DHMAC-SHA1&SignatureNonce%3D9b7a44b0-3be1-11e5-8c73-08002700c460&SignatureVersion%3D1.0&Timestamp%3D2015-08-06T02%253A19%253A46Z&Version%3D2014-11-11'
    print(string_to_sign)
    key = bytes('testsecret&', encoding='utf-8')
    msg = bytes(string_to_sign, encoding='utf-8')
    hmac_content = hmac.new(key=key, msg=msg, digestmod=sha1)
    signature = str(base64.b64encode(hmac_content.digest()), encoding='utf-8')
    print(signature)

if __name__ == '__main__':
    # refresh_cdn_cache('static.wcbp.leomaster.com.cn/html/images/kvbanner_02.png')
    _test_calc_hmac()
