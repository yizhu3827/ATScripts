import os
# 导入删除文件夹/文件模块：
import shutil
# 导入压缩模块：
import zipfile
# 导入日期模块：
import datetime
# 导入发邮件模块：
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
# 导入配置文件：
from conf import settings
from util.LogHandler import logger
class SendMailHandler(object):
    # 将测试报告压缩并发送邮件
    def _check_zip_file(self):
        # 将测试报告压缩：
        base_dir = settings.ALLURE_REPORT_DIR_PATH
        # 压缩包路径：
        zip_file_path = settings.ZIP_FILE_PATH
        f = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_name, file_names in os.walk(base_dir):
            # 要是不replace，就从根目录开始复制：
            file_path = dir_path.replace(base_dir, '')
            # 实现当前文件夹以及包含的所有文件：
            file_path = file_path and file_path + os.sep or ''
            for file_name in file_names:
                f.write(os.path.join(dir_path, file_name), file_path + file_name)
        f.close()
    def send_mail_msg(self):
        # 调用压缩功能：
        self._check_zip_file()
        # 调用发邮件操作：
        self._send_mail()
        # 调用删除临时文件：
        self._del_temp_file()
    def _send_mail(self):
        # 发邮件操作：
        # 第三方 SMTP 服务：
        mail_host = settings.MAIL_HOST
        # 下面两个，可修改：
        mail_user = settings.MAIL_USERNAME
        mail_pass = settings.MAIL_TOKEN
        # 可修改：设置收件人和发件人：
        sender = settings.SENDER
        # 收件人，收件人可以有多个，以列表形式存放：
        receivers = settings.RECEIVERS
        # 创建一个带附件的实例对象：
        message = MIMEMultipart()
        # 可修改邮件主题、收件人、发件人：
        subject = settings.MAIL_SUBJECT
        # 下面三行不用修改：
        message['Subject'] = Header(subject, 'utf-8')
        # 发件人：
        message['From'] = Header("{}".format(sender), 'utf-8')
        # 收件人：
        message['To'] = Header("{}".format(';'.join(receivers)), 'utf-8')
        # 邮件正文内容 html 形式邮件：相当于是一个报告预览：
        # 可修改：send_content
        content = settings.MAIN_CONTENT
        # 第一个参数为邮件正文内容：
        html = MIMEText(_text=content, _subtype='plain', _charset='utf-8')
        # 构造附件：
        send_content = open(settings.ZIP_FILE_PATH, 'rb').read()
        # 只允许修改第一个参数，后面两个保持默认：
        att = MIMEText(_text=send_content, _subtype='base64', _charset='utf-8')
        # 不要改：
        att["Content-Type"] = 'application/octet-stream'
        # 页面中，附件位置展示的附件名称：
        file_name = 'report.zip'
        # 下面3行不要改、filename 为邮件附件中显示什么名字：
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(file_name)
        message.attach(html)
        message.attach(att)
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(mail_host, 25)
            smtp_obj.login(mail_user, mail_pass)
            smtp_obj.sendmail(sender, receivers, message.as_string())
            smtp_obj.quit()
            logger().info("邮件发送成功")
        except smtplib.SMTPException as e:
            logger().error("Error: 邮件发送失败，详情:{}".format(e))
    def _del_temp_file(self):
        # 清空report目录：
        logger().info('删除临时目录')
        # shutil.rmtree(settings.REPORT_PATH)
        logger().info('删除临时目录成功')
if __name__ == '__main__':
    # 在当前py文件测试：
    SendMailHandler().send_mail_msg()