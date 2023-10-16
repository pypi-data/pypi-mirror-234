import os
import smtplib
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import traceback
import argparse
import creditutils.trivial_util as trivial_util
import creditutils.file_util as file_util

class SenderLabel:
    NAME_FLAG = 'name'
    EMAIL_FLAG = 'email'
    PATH_FLAG = 'path'

class SenderProcess:
    def __init__(self, host, sender, passwd, port=465, name=None):
        # SMTP服务器及端口号
        self.host = host
        self.port = port
        # 发件人邮箱及姓名
        self.sender = sender
        self.name = name
        # 邮箱密码
        self.passwd = passwd

    def _format_addr(self, name, email):
        """规范地址格式处理, 支持多个收件人"""
        return formataddr((Header(name, 'utf-8').encode(), email))

    def send_mail(self, subject, content, receivers, ccs=None, images=None, files=None, subtype='plain'):
        mail_receivers = list()
        to_info_items = list()
        if receivers:
            for item in receivers:
                if item and SenderLabel.EMAIL_FLAG in item:
                    receiver_email = item[SenderLabel.EMAIL_FLAG]
                    mail_receivers.append(receiver_email)
                    receiver_name = receiver_email.split('@')[0]
                    if SenderLabel.NAME_FLAG in item and item[SenderLabel.NAME_FLAG]:
                        receiver_name = item[SenderLabel.NAME_FLAG]
                    info_item = self._format_addr(receiver_name, receiver_email)
                    to_info_items.append(info_item)

        cc_info_items = list()
        if ccs:
            for item in ccs:
                if item and SenderLabel.EMAIL_FLAG in item:
                    receiver_email = item[SenderLabel.EMAIL_FLAG]
                    mail_receivers.append(receiver_email)
                    receiver_name = receiver_email.split('@')[0]
                    if SenderLabel.NAME_FLAG in item and item[SenderLabel.NAME_FLAG]:
                        receiver_name = item[SenderLabel.NAME_FLAG]
                    info_item = self._format_addr(receiver_name, receiver_email)
                    cc_info_items.append(info_item)

        to_info = ','.join(to_info_items)
        cc_info = ','.join(cc_info_items)
        # print(f'mail_receivers: {mail_receivers}')
        # print(f'to_info: {to_info}')
        
        # mm = MIMEMultipart('related')
        mm = MIMEMultipart('mixed')

        # 邮件主题
        subject_content = subject
        # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
        sender_name = self.sender
        if self.name:
            sender_name = self.name
        mm["From"] = self._format_addr(sender_name, self.sender)
        # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
        mm["To"] = to_info
        mm["Cc"] = cc_info
        # 设置邮件主题
        mm["Subject"] = Header(subject_content,'utf-8')

        # 邮件正文内容
        body_content = content
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(body_content, subtype, "utf-8")
        # 向MIMEMultipart对象中添加文本对象
        mm.attach(message_text)

        # 二进制读取图片
        if images:
            for img in images:
                if img and SenderLabel.PATH_FLAG in img:
                    file_path = img[SenderLabel.PATH_FLAG]
                    file_name = os.path.basename(file_path)
                    if SenderLabel.NAME_FLAG in img and img[SenderLabel.NAME_FLAG]:
                        file_name = img[SenderLabel.NAME_FLAG]

                    image_data = open(file_path,'rb')
                    # 设置读取获取的二进制数据
                    msg_image = MIMEImage(image_data.read())
                    # msg_image.add_header('Content-ID', file_name)
                    msg_image.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file_name))
                    #关闭刚才打开的文件
                    image_data.close()
                    # 添加图片文件到邮件信息当中去
                    mm.attach(msg_image)

        # 构造附件
        if files:
            for item in files:
                if SenderLabel.PATH_FLAG in item:
                    file_path = item[SenderLabel.PATH_FLAG]
                else:
                    raise Exception('not exists file path!')

                file_name = os.path.basename(file_path)
                if SenderLabel.NAME_FLAG in item:
                    file_name = item[SenderLabel.NAME_FLAG]

                atta = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
                # 设置附件信息，中文信息需要特殊处理
                atta.add_header('Content-Disposition', 'attachment', filename=('gbk', '', file_name))
                # 添加附件到邮件信息当中去
                mm.attach(atta)

        try:
            # 创建SMTP对象
            stp = smtplib.SMTP_SSL(host=self.host)
            # 设置发件人邮箱的域名和端口
            stp.connect(host=self.host, port=self.port)  # 连接smtp服务器
            # 可以打印出和SMTP服务器交互的所有信息
            # stp.set_debuglevel(1)
            # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱密码
            stp.login(self.sender, self.passwd)  # 登录邮箱
            stp.sendmail(self.sender, mail_receivers, mm.as_string())  # 发送邮件
            print(f'send to {mail_receivers} success.')
            stp.quit()
        except Exception as e:
            print(f'send to {mail_receivers} failed, {str(e)}')
            print(traceback.format_exc())
