from urllib.parse import quote_plus
from enum import Enum
from requests import post, get


class DingURL(str, Enum):
    LOGIN = 'https://login.dingtalk.com/oauth2/challenge.htm'
    ACCESS_TOKEN = 'https://api.dingtalk.com/v1.0/oauth2/userAccessToken'
    USER_INFO = 'https://api.dingtalk.com/v1.0/contact/users/me'


class DingQR:
    def __init__(self, ak: str, sk: str) -> None:
        """钉钉扫码登录初始化

        Parameters:
        ------------
        ak:钉钉应用的appkey
        sk:钉钉应用的secretkey
        """
        self.ak = ak
        self.sk = sk

    def login_url_generate(self, redirect_url: str, ding_login_url: str = DingURL.LOGIN.value) -> str:
        """生成钉钉扫码登录的url地址

        Parameters:
        -----------
        redirect_url: 扫码通过后,回调的地址
        ding_login_url: 构建登录url的前缀地址,默认无需变动

        Return:
        -------
        url:钉钉扫码登录的url地址
        """
        data = dict(
            redirect_uri=quote_plus(redirect_url),
            client_id=self.ak,
            response_type='code', scope='openid', state='dddd', prompt='consent'
        )
        query_params = '&'.join([f'{k}={data[k]}' for k in data])
        url = ding_login_url+'?'+query_params
        return url

    def user_info_get(self, auth_code: str, access_token_url: str = DingURL.ACCESS_TOKEN.value, user_info_url: str = DingURL.USER_INFO.value) -> dict:
        """获取钉钉扫码得到的用户信息

        Parameters:
        ------------
        auth_code:钉钉登录连接返回的auth_code
        access_token_url: 获取access_token的api请求地址
        user_info_url: 获取用户信息的api请求地址

        Return:
        --------
        results:用户信息
        """

        # 获取Access_token
        data = dict(clientId=self.ak, clientSecret=self.sk,
                    code=auth_code, grantType='authorization_code')
        with post(access_token_url, json=data) as rsp:
            rsp.encoding = rsp.apparent_encoding
            access_token = rsp.json().get('accessToken', '')

        # 获取UserInfo
        headers = {'x-acs-dingtalk-access-token': f'{access_token}'}
        with get(user_info_url, headers=headers) as rsp:
            rsp.encoding = rsp.apparent_encoding
            results = rsp.json()
        return results
