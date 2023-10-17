import inquirer

from autowork_cli.common.request.CybotronSyncClient import CybotronSyncClient
from autowork_cli.common.config.BaseURLConfig import BaseURLConfig
from autowork_cli.common.config.LoginConfig import LoginConfig
from rich import print

from autowork_cli.util.apikeyutil import ApiKeyUtil


class LoginCommand:
    def __init__(self):
        self.config = LoginConfig()

    def run_login(self):
        # 初始化函数
        print("登录 Autowork...")

        self.ask_env()
        self.ask_api_key()
        self.ask_dev_apps()

        self.hello()

    def ask_env(self):
        # tuple (label, value) list
        choices_list = [(a + ": " + BaseURLConfig.get_domain_url(a), a) for a in BaseURLConfig.get_env_list()]
        answer = inquirer.prompt([
            inquirer.List(
                "env",
                message="选择要登录的环境?",
                choices=choices_list,
                default=self.config.get_env()
            )
        ])
        self.config.set_env(answer["env"])
        self.config.save()

    def ask_api_key(self):
        safe_apikey = ApiKeyUtil.safe_display(self.config.get_api_key())
        answer = inquirer.prompt([
            inquirer.Text('api_key',
                          message="请输入您的API KEY",
                          default=safe_apikey),
        ])

        if safe_apikey != answer["api_key"]:
            self.config.set_api_key(answer["api_key"])
            self.config.save()

    def ask_dev_apps(self):
        answer = inquirer.prompt([
            inquirer.Text('dev_apps',
                          message="请输入您正要开发的应用编码，多个应用用逗号分隔",
                          default=self.config.get_dev_apps()),
        ])
        self.config.set_dev_apps(answer["dev_apps"])
        self.config.save()

    def hello(self):
        client = CybotronSyncClient()
        try:
            userinfo = client.get("usr/api/v1/getUserInfo").get("result")
            username = userinfo.get('name')
            print(f"[green]你好, {username}, Autowork {self.config.get_env()}环境连接成功！")
        except Exception :
            print(f"[red]连接失败: 请确认API KEY是否正确，或者确认连接的赛博坦环境是否启动")
