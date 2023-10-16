#!/usr/bin/env python3

"""
作者:J.Hu
日期:2023-09-12
内容:
> 追加了针对115版本以上chrome的驱动下载,请确保网络能够访问 https://googlechromelabs.github.io/chrome-for-testing/
> 追加了experimental_option的初始化设定,运行自定义参数,默认加入不会自动关闭浏览器操作.
> 针对新版本selenum4.X进行了部分方法的更新,支持By多类型的ActionInfo
> 自动分析系统并下载匹配最新的驱动,免除了手动下载匹配驱动
> 抽象化部分操作,通过简单的结构化配置即可实现脚本运行
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from requests import session
from typing import List
import json
import zipfile
import os
import platform


# 环境变量设定
DRIVER_NAME = 'chromedriver'
DRIVER_PATH = './' + DRIVER_NAME

# 淘宝镜像谷歌浏览器驱动下载地址
DRIVER_URL = 'https://registry.npmmirror.com/-/binary/chromedriver/'
# 115版本及以后用此链接进行下载
DRIVER_URL_155 = 'https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/'
DRIVER_URL_JSON = 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'


def get_chromedriver_type() -> str:
    """根据系统类型获取下载驱动
    Returns
    -------
    'chromedriver_mac64.zip': Mac Intel驱动
    'chromedriver_mac64_m1.zip': Mac M系列驱动
    'chromedriver_linux64.zip': Linux驱动
    'chromedriver_win32.zip': Windows驱动
    """
    system_info = platform.system()
    if system_info == 'Darwin':
        # x86_64架构视为非M系列 M系列为ARM架构
        return 'chromedriver_mac64.zip' if platform.machine() == 'x86_64' else 'chromedriver_mac64_m1.zip'
    elif system_info == 'Linux':
        return 'chromedriver_linux64.zip'
    else:
        return 'chromedriver_win32.zip'


def get_chromedriver_type_115() -> str:
    """根据系统类型获取下载驱动
    """
    system_info = platform.system()
    if system_info == 'Darwin':
        # x86_64架构视为非M系列 M系列为ARM架构
        return 'mac-x64/chromedriver-mac-x64.zip' if platform.machine() == 'x86_64' else 'mac-arm64/chromedriver-mac-arm64.zip'
    elif system_info == 'Linux':
        return 'linux64/chromedriver-linux64.zip'
    else:
        bits = platform.architecture()[0]
        if bits == '32bit':
            return 'win32/chromedriver-win32.zip'
        else:
            return 'win64/chromedriver-win64.zip'


def get_chromedriver_list(url: str = DRIVER_URL) -> list:
    """获取可供下载的驱动版本
    Parameters
    ----------
    url:镜像驱动下载地址
    Returns
    -------
    {
        name:下载的驱动版本号
    }
    """
    with session() as conn:
        rsp = conn.get(url)
        chrome_list = json.loads(rsp.text)
    # 获取到的版本号为最后有一个/,舍弃掉,并且分割出版本数字,版本号中含有非数字的全都作为非版本数据处理掉,为后续版本比较处理,全部int化掉
    return [[int(i) for i in val['name'][:-1].split('.')] for val in chrome_list if val['name'][0].isdigit()]


def get_chromedriver_list_115(url: str = DRIVER_URL_JSON) -> list:
    with session() as conn:
        rsp = conn.get(url)
        chrome_list = json.loads(rsp.text)
    # 获取到的版本号为最后有一个/,舍弃掉,并且分割出版本数字,版本号中含有非数字的全都作为非版本数据处理掉,为后续版本比较处理,全部int化掉

    rsp = []
    for d in chrome_list['versions']:
        rsp.append(list(map(int, d['version'].split('.'))))
    return rsp


def download_chrome_driver(url: str) -> None:
    """下载驱动文件并解压缩和设置权限
    Paramters
    ---------
    url:下载驱动的地址
    """
    driver_name = DRIVER_NAME
    zip_driver_name = driver_name + '.zip'
    with session() as conn:
        rsp = conn.get(url, stream=True)
    with open(zip_driver_name, 'wb') as f:
        for chunk in rsp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
            else:
                break

    with zipfile.ZipFile(zip_driver_name) as zf:
        # 获取ZIP文件中的所有文件和文件夹列表
        file_list = zf.namelist()

        # 逐个解压文件
        for file in file_list:
            # 从文件路径中提取文件名
            file_name = os.path.basename(file)
            # 将文件解压到目标路径
            if file_name == driver_name:
                zf.extract(file, './')

                # 判断是否是设定的标准路径,如果不是,则移动到标准路径
                if (file != driver_name):
                    os.rename(file, driver_name)

    os.chmod(driver_name, 766)


def get_chrome_version(message: str) -> str:
    """从错误信息中寻找浏览器的版本信息
    Parameters
    ----------
    message:出错信息
    Returns
    -------
    返回版本号信息,如果没有获取到版本号信息,返回空
    """
    start_msg = 'Current browser version is '
    end_msg = 'with binary path'

    end_idx = message.find(end_msg)
    start_idx = len(start_msg) + message.find(start_msg)
    if end_idx == -1:
        return ''
    return message[start_idx:end_idx].strip()


def fit_chrome_version(cur_version: str, check_list: list, prefix_url: str = DRIVER_URL) -> str:
    """根据当前的版本,匹配下载版本. 匹配的下载版本号不大于当前版本号,且是最接近的一个版本号
    Parameters
    ----------
    cur_version:当前版本信息
    check_list:可供下载的版本列表
    prefix_url:前置通用url
    Returns
    -------
    返回一个供下载的版本url
    """
    # 如果没有版本信息,返回一个默认值
    if cur_version == '':
        return prefix_url + '.'.join([str(val) for val in check_list[0]]) + '/'

    cur_list = [int(i) for i in cur_version.split('.')]
    cur_size = len(cur_list)
    version_info = ''
    for i in range(cur_size):
        ver_dif = min([cur_list[i] - val[i]
                       for val in check_list if cur_list[i] >= val[i]])
        check_list = [val for val in check_list if val[i]
                      == cur_list[i] - ver_dif]
        if i == 0:
            version_info = str(cur_list[i] - ver_dif)
        else:
            version_info = version_info + '.' + str(cur_list[i] - ver_dif)
    return prefix_url + version_info + '/'


def setup_dirver(cur_version: str, chrome_list: list):
    url = DRIVER_URL
    fn = get_chromedriver_type
    chrome_list_fn = get_chromedriver_list

    if cur_version != '':
        if [int(i) for i in cur_version.split('.')][0] > 114:
            url = DRIVER_URL_155
            fn = get_chromedriver_type_115
            chrome_list_fn = get_chromedriver_list_115

    # 重新获取一次,因为不同版本的下载地址是不一样的.
    chrome_list = chrome_list_fn()

    download_url = fit_chrome_version(
        cur_version, chrome_list, prefix_url=url) + fn()
    download_chrome_driver(download_url)
    return chrome_list


def init_chrome_options(experimental_option: dict = None):
    """初始化设定ChromeOptions
    """
    options = webdriver.ChromeOptions()

    # 忽略SSL验证
    options.add_argument('ignore-certificate-errors')

    # 伪装浏览器
    options.add_argument(
        'User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')

    # 屏蔽chrome正受到自动测试软件的控制
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    # 不自动关闭浏览器
    options.add_experimental_option('detach', True)

    # 自定义的追加相关experimental_option的设置
    if experimental_option:
        for k in experimental_option:
            options.add_experimental_option(k, experimental_option[k])

    return options


class ActionInfo:
    def __init__(self, by, by_val, func, val):
        self.by = by
        self.by_val = by_val
        self.func = func
        self.val = val


class WebdriveChrome:
    def __init__(self, driver_path=DRIVER_PATH, experimental_option: dict = None):
        """初始化Webdriver Chrome
        """
        # 初始化浏览器配置项
        options = init_chrome_options(experimental_option)

        # 默认等待时间(单位:秒)
        self._waittime = 5

        cur_version = ''
        chrome_list = []
        if not os.path.exists(driver_path):
            chrome_list = setup_dirver(cur_version, chrome_list)

        service = Service(executable_path=driver_path)

        # 默认尝试3次.
        for _ in range(3):
            try:
                driver = webdriver.Chrome(service=service, options=options)
                driver.implicitly_wait(self.waittime)  # 避免模拟器运行慢获取不到元素
                self._driver = driver
                break
            except Exception as e:
                cur_version = get_chrome_version(e.msg)
                chrome_list = setup_dirver(cur_version, chrome_list)

    @property
    def driver(self):
        return self._driver

    @property
    def waittime(self):
        return self._waittime

    def run(self, url: str, info: List[ActionInfo]):
        """运行Web动作
        Parameters
        ----------
        url:运行的url
        info: 运行动作对象列表
        """
        driver = self.driver
        driver.get(url)
        for t in info:
            obj = driver.find_element(t.by, t.by_val)
            t.func(obj) if t.val is None else t.func(obj, t.val)


if __name__ == '__main__':
    wb = WebdriveChrome()
