from argparse import ArgumentParser
from getpass import getpass
import requests as rq
import socket
import textwrap
from re import match
import json


class CLICommand:
    """苏大校园网登录脚本
    """

    @staticmethod
    def add_argments(parser: ArgumentParser):
        pass

    @staticmethod
    def run(args, parser):
        print("--苏大校园网登录脚本--")
        sid = input("请输入学号:")
        pswd = getpass("请输入密码:")
        login(sid, pswd)


def login(sid, pswd):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    mac = 000000000000
    url = f"http://10.9.1.3:801/eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2Cb%2C{sid}" \
          f"&user_password={pswd}&wlan_user_ip={ip}&wlan_user_ipv6=&wlan_user_mac={mac}&wlan_ac_ip=" \
          f"&wlan_ac_name=&jsVersion=3.3.3&v=8918"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    }
    response = rq.get(url, headers=headers)
    print(parse(response.text))
    response.close()


def parse(s):
    rt = match(r".*?\((\{.*?})\)", s)
    data = rt.group(1)
    data = json.loads(data)
    return textwrap.dedent(f"""
    ------------------------
    msg: {data["msg"]}
    code: {data["result"]}
    ------------------------
    """).strip()
