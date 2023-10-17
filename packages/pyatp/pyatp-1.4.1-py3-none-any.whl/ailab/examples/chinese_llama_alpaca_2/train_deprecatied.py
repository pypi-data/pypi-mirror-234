import os
from ailab.utils.other import install_requiremet
from ailab.log import logger
import subprocess

def upgrade_atp():
    cmds = [
        "pip config set global.index-url https://repo.model.xfyun.cn/api/packages/administrator/pypi/simple  &&  pip config set global.extra-index-url https://pypi.mirrors.ustc.edu.cn/simple/",

        'pip install pyatp --upgrade']

    for cm in cmds:
        subprocess.call(cm, shell=True)


def install_req():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    install_requiremet(dir_path)

def chinese_alpaca_test():
    import subprocess
    # 启动 shell 脚本
    dir_path = os.path.dirname(os.path.realpath(__file__))
    shell_path = os.path.join(dir_path,"train.sh")
    ret = subprocess.call("sh " + shell_path, shell=True)
    if ret != 0:
        logger.info("训练失败: Check")
    return ret

if __name__ == '__main__':
    install_req()
    upgrade_atp()
    exit(chinese_alpaca_test())
