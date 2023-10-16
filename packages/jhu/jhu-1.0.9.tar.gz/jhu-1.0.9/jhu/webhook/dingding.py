"""
作者:J.Hu
日期:2023-10-08
内容:
- 钉钉的Webhook功能,支持发送text类型和link类型
"""
from time import time
from base64 import b64encode
from hashlib import sha256
from hmac import new as hmac_new
from urllib.parse import quote_plus
from requests import session


class AtContent(dict):
    def __init__(self, atMobiles: list[str] = None, atUserIds: list[str] = None, isAtAll: bool = False) -> None:
        super().__init__(atMobiles=atMobiles, atUserIds=atUserIds, isAtAll=isAtAll)


class TextData(dict):
    def __init__(self, content: str, at: AtContent = None) -> None:
        super().__init__(msgtype='text', at=at, text=dict(content=content))


class LinkData(dict):
    """link的类型不支持@功能
    """

    def __init__(self, title: str, text: str, messageUrl: str, picUrl: str = None) -> None:
        super().__init__(msgtype='link', link=dict(title=title,
                                                   text=text, messageUrl=messageUrl, picUrl=picUrl))


class DingHook:
    def __init__(self, url: str, sk: str = None) -> None:
        self.url = url
        self.sk = sk

    def send(self, data) -> None:
        """发送消息
        """
        # 设置了加签的情况
        sk = self.sk

        if sk:
            sk_enc = sk.encode('utf-8')
            timestamp = str(round(time()*1000))
            sign_str = f'{timestamp}\n{sk}'
            sign_str_enc = sign_str.encode('utf-8')
            hmac_code = hmac_new(sk_enc, sign_str_enc,
                                 digestmod=sha256).digest()
            sign = quote_plus(b64encode(hmac_code))
            url = f'{self.url}&timestamp={timestamp}&sign={sign}'
        else:
            url = self.url

        # 发送消息
        with session() as s:
            rsp = s.post(url, json=data)

        result = rsp.json()
        if result['errcode'] != 0:
            raise Exception(result['errmsg'])


if __name__ == "__main__":
    url = 'https://oapi.dingtalk.com/robot/send?access_token=**********'
    sk = '***********'
    ding = DingHook(url, sk)
    at = AtContent(isAtAll=True)
    # text类型
    data = TextData(content='吕布来袭,请注意', at=at)
    # link类型
    data = LinkData(title='新的挑战', text='恭喜你的球队升入英超联赛,现在你将面临更大的挑战了,这里的竞争将更加的激烈', messageUrl='https://www.baidu.com',
                    picUrl='')
    try:
        rsp = ding.send(data)
    except Exception as e:
        print(e)
