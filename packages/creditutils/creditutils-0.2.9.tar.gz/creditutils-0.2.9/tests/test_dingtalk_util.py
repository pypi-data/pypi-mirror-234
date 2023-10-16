import creditutils.dingtalk_util as dingtalk_util


def test_send_data():
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=****************************************************************'
    secret = '*******************************************************************'
    data_m = {
            "msgtype": "markdown",
            "markdown": {
                "title": "首屏会话透出的展示内容",
                "text": "# 这是支持markdown的文本 \n## 标题2  \n* 列表1 \n ![alt 啊](https://gw.alipayobjects.com/zos/skylark-tools/public/files/b424a1af2f0766f39d4a7df52ebe0083.png)"
            }
        }
    data_t = {
        "msgtype": "text", 
        "text": {
            "content": "天下信用 5.2.0相关的渠道包已经上传到阿里云，请配置天下信用的升级，apk包下载链接如下：http://apk.tianxiaxinyong.com/pycredit.apk"
        }, 
        "at": {
            "atMobiles": [
                "15870679047", 
                "18665922663"
            ], 
            "isAtAll": False
        }
    }
    rtn = dingtalk_util.send_map_data(webhook, secret, data_t)
    print(rtn.text)


def test_main():
    test_send_data()


if __name__ == '__main__':
    test_main()
    print('to the end!')
