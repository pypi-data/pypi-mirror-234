'''
作者:J.Hu
日期:2022-07-01
内容:
# 功能描述：
 - 支持邮件发送
# 重要版本变更说明：
 - 更新附件的代码编写,使其支持正常的文字显示;
 - To/Cc/Bcc的列表拼接采用逗号的形式拼接，原因是原来采用多个To/Cc/Bcc会导致
   在某些邮件客户端上只显示一个To/Cc/Bcc内容.
   比如：Header里面内容如：
   To:=?utf-8?b?6IOh5YGl?= <huj@citytsm.com>
   To:=?utf-8?b?6IOh5YGl?= <huj@citytsm.com>
   这样只会显示一个huj，
   现在修改变成：
   To:=?utf-8?b?6IOh5YGl?= <huj@citytsm.com>,=?utf-8?b?6IOh5YGl?= <huj@citytsm.com>
   这样就可以显示出2个huj，huj了
'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formataddr
from email.header import Header
from smtplib import SMTP, SMTP_SSL
from pydantic import BaseModel
from typing import Optional

class MailKeyword(str):
    # 发送信关键字
    FROM = 'From'
    TO = 'To'
    CC = 'Cc'
    BCC = 'Bcc'
    TITLE = 'Subject'

    # 编码关键字
    ENCODE_UTF8 = 'utf-8'

    # 邮件类型关键字
    MAILTYPE_PLAIN = 'plain'
    MAILTYPE_HTML = 'html'
    MAILTYPE_BASE64 = 'base64'


class MailAttach(BaseModel):
    path: str
    name: Optional[str] = None

    def __init__(self, **kw):
        if kw.get('name') is None:
            kw['name'] = kw['path'].split('/')[-1]
        super().__init__(**kw)


class MailUser(BaseModel):
    addr: str
    name: Optional[str] = None

    def __init__(self, **kw):
        if kw.get('name') is None:
            kw['name'] = kw['addr']
        super().__init__(**kw)


class Mail:
    def __init__(self,
                 host: str,
                 port: int = 465,
                 ssl: bool = True,
                 timeout: int = 7,
                 encode: MailKeyword = MailKeyword.ENCODE_UTF8,
                 mail_type: MailKeyword = MailKeyword.MAILTYPE_HTML,
                 attach_type: MailKeyword = MailKeyword.MAILTYPE_BASE64):
        """
        host:smtp服务器
        port:smtp服务器端口号
        ssl: true:使用ssl
        timeout:超时时间,单位:秒
        encode:编码类型,默认为utf-8
        mail_type: 正文类型, 默认为html
        attach_type: 附件类型,默认为base64
        """

        self._smtp = self.__connect(host, port, ssl, timeout)
        self._encode = encode
        self._mail_type = mail_type
        self._attach_type = attach_type

        # 初始化to,cc,bcc list
        self._receive_lst = {}
        self.__receive_type_lst = [
            MailKeyword.TO, MailKeyword.CC, MailKeyword.BCC]

    @property
    def smtp(self):
        return self._smtp

    @property
    def encode(self):
        return self._encode

    @property
    def mail_type(self):
        return self._mail_type

    @property
    def attach_type(self):
        return self._attach_type

    @property
    def sender(self):
        return self._sender

    @property
    def receive_to(self):
        return self.__get_receive_lst(MailKeyword.TO)

    @property
    def receive_cc(self):
        return self.__get_receive_lst(MailKeyword.CC)

    @property
    def receive_bcc(self):
        return self.__get_receive_lst(MailKeyword.BCC)

    def __get_receive_lst(self, type: MailKeyword):
        return self._receive_lst.get(type, [])

    def __set_receiver_lst(self, type: MailKeyword, addr, name=None):
        u = MailUser(addr=addr, name=name)
        type_list = self.__get_receive_lst(type)
        if type_list == []:
            self._receive_lst[type] = [u]
        else:
            self._receive_lst[type].append(u)

    def __connect(self, host, port, ssl, timeout):
        smtpfunc = SMTP_SSL if ssl else SMTP
        return smtpfunc(host, port, timeout=timeout)

    def __mime_attach(self, mime, att, attid):
        li = MailAttach(path=att)
        att = MIMEText(open(li.path, 'rb').read(),
                       MailKeyword.MAILTYPE_BASE64, self.encode)
        att.add_header('Content-ID', str(attid))
        att.add_header('Content-Type', 'application/octet-stream')
        att.add_header("Content-Disposition", 'attachment',
                       filename=(MailKeyword.ENCODE_UTF8, '', li.name))
        mime.attach(att)

    def set_sender(self, addr, name=None):
        self._sender = MailUser(addr=addr, name=name)

    def add_receiver_to(self, addr, name=None):
        self.__set_receiver_lst(MailKeyword.TO, addr, name)

    def add_receiver_cc(self, addr, name=None):
        self.__set_receiver_lst(MailKeyword.CC, addr, name)

    def add_receiver_bcc(self, addr, name=None):
        self.__set_receiver_lst(MailKeyword.BCC, addr, name)

    def clear_receiver_lst(self):
        """
        清空收件人列表包含to,cc,bcc
        """
        self._receive_lst = {}

    def login(self, user: str, passwd: str, nickname: str = None):
        """
        user:登录用户名
        passwd:登录密码
        """
        self.smtp.login(user, passwd)
        self.set_sender(user, nickname)

    def send(self, title: str, content: str, attach_lst=None):
        """
        title:邮件标题
        content:邮件正文
        attach:邮件附件,默认为空
        """
        mime = MIMEMultipart()

        # 设置邮件标题,发件人
        mime[MailKeyword.TITLE] = Header(title, self.encode)
        mime[MailKeyword.FROM] = formataddr(
            [self.sender.name, self.sender.addr])

        # 设置收件人信息 to,cc,bcc
        receive_lst = []
        for val in self.__receive_type_lst:
            val_lst = self.__get_receive_lst(val)
            receive_lst.extend([mail.addr for mail in val_lst])
            mime[val] = ','.join(
                [formataddr([mail.name, mail.addr]) for mail in val_lst])

        # 正文内容设置
        mime.attach(MIMEText(content, self.mail_type, self.encode))

        # 附件内容设置
        for idx, val in enumerate(attach_lst):
            self.__mime_attach(mime, val, idx)

        # 发送邮件
        self.smtp.sendmail(self.sender.addr, receive_lst, mime.as_string())

    def disconnect(self):
        """
        关闭链接
        """
        self.smtp.close()
