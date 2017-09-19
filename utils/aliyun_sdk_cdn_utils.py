from aliyunsdkcore.client import AcsClient

from aliyunsdkcdn.request.v20141111 import RefreshObjectCachesRequest
from aliyunsdkcdn.request.v20141111 import PushObjectCacheRequest

client = AcsClient(
    "WQJC0JqAfgIe3Msh",
    "ucUzDnwidx1Q3lqXCAlbFKxluQMIWf",
    "cn-shenzhen"
)


def refresh_cdn(url):
    request = RefreshObjectCachesRequest.RefreshObjectCachesRequest()
    request.set_accept_format('JSON')
    request.set_ObjectType('File')
    request.set_ObjectPath(url)

    client.do_action_with_exception(request)


def push_file_to_cdn(url):
    request = PushObjectCacheRequest.PushObjectCacheRequest()
    request.set_accept_format('JSON')
    request.set_ObjectPath(url)
    client.do_action_with_exception(request)


if __name__ == '__main__':
    refresh_cdn('static.wcbp.leomaster.com.cn/html/images/kvbanner_02.png')
    push_file_to_cdn('static.wcbp.leomaster.com.cn/html/images/kvbanner_02.png')
