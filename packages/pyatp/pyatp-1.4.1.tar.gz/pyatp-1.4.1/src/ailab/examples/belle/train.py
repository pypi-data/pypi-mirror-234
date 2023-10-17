import os
import argparse

def belle_test(args):
    import subprocess
    # 启动 shell 脚本
    dir_path = os.path.dirname(os.path.realpath(__file__))
    shell_path = os.path.join(dir_path,"train.sh")
    subprocess_args = ["sh", shell_path]
    if args.distributed:
        subprocess_args.append("--distributed")
    ret = subprocess.call(' '.join(subprocess_args), shell=True)
    if ret != 0:
        print("训练失败: Check")
    return ret


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='An example script with command-line arguments.')
    parser.add_argument('--distributed', action='store_true', help='if use distributed')
    args = parser.parse_args()

    exit(belle_test(args))
