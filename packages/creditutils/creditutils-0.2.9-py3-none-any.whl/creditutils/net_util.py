import urllib
import urllib.request
import json
import traceback
import time
from creditutils.trivial_util import print_t


def get_proxy_ip(url):
    print_t('to get proxy ip.')
    
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        content = response.read()
        if (content):
            result = json.loads(content)
            if result['code'] == 0:
                return result['data']
            else:
                print_t(content)
                return None
        else:
            return None
    except:
        traceback.print_exc()
        return None


PROXY_TYPE_HTTP = 0
PROXY_TYPE_HTTPS = 1
PROXY_TYPE_SOCKS5 = 2

def get_one_proxy(url, to_wait=2, try_times=3, proxy_type=PROXY_TYPE_SOCKS5):
    cnt_butt = try_times
    cnt = 0
    while True:
        proxies = get_proxy_ip(url)
        cnt += 1
        if proxies:
            break
        else:
            # 至少要等待一段时间才能重新请求
            time.sleep(to_wait)

        if cnt >= cnt_butt:
            print_t(f'try {cnt} times, but still failed!')
            break

    if proxies:
        item = proxies[0]
        if proxy_type == PROXY_TYPE_HTTP:
            target = f'http://{item["ip"]}:{item["port"]}'
        elif proxy_type == PROXY_TYPE_HTTPS:
            target = f'https://{item["ip"]}:{item["port"]}'
        elif proxy_type == PROXY_TYPE_SOCKS5:
            target = f'SOCKS5://{item["ip"]}:{item["port"]}'
        else:
            raise Exception(f'invalid PROXY_TYPE {proxy_type}!')

        return target
    else:
        raise Exception('get proxy ip from network failed!')