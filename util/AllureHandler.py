# 执行终端命令、subprocess要代替一些老旧的模块命令：
from subprocess import Popen, call
from conf import settings
from util.LogHandler import logger
class AllureHandler(object):
    # 读取json文件，生成allure报告：
    def execute_command(self):
        # Python执行终端命令：shell=True：将['allure', 'generate', '-o', 'xxxx']替换为'allure generate -o'
        try:
            call(settings.ALLURE_COMMAND, shell=True)
            logger().info('执行allure命令成功')
        except Exception as e:
            logger().error("执行allure命令失败,详情参考: {}".format(e))