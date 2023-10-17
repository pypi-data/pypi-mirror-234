import os.path
import pathlib
import shutil
from typing import Any
import logging
from jinja2 import Environment
from plumbum import cli
from plumbum.cmd import rm  # type: ignore
import subprocess
from pyatp_buildkit.config import *
from ailab.inference_wrapper.huggingface import transformers
import datetime

log = logging.getLogger()
pwd = os.path.abspath(__file__)
dockerfile_dir = ''
import subprocess


class Manager(cli.Application):
    """aialb CI Manager"""

    PROGNAME: str = "build.py"
    VERSION: str = "0.0.1"

    manifest = {}
    ci = None

    def main(self):
        if not self.nested_command:  # will be ``None`` if no sub-command follows
            log.fatal("No subcommand given!")
            print()
            self.help()
            return 1
        elif len(self.nested_command[1]) < 2 and any(
                "generate" in arg for arg in self.nested_command[1]
        ):
            log.error(
                "Subcommand 'generate' missing  required arguments! use 'generate --help'"
            )
            return 1


@Manager.subcommand("generate")  # type: ignore
class ManagerGenerate(Manager):
    DESCRIPTION = "Generate Dockerfiles from templates."

    parent: Manager

    vars = {}

    matrix = []
    template_env: Any = Environment(
        extensions=["jinja2.ext.do", "jinja2.ext.loopcontrols"],
        trim_blocks=True,
        lstrip_blocks=True,
    )
    cache: Any = cli.Flag(
        ["-c", "--cache"], default=True, help="Enable cache mode"
    )
    template: Any
    action: Any = cli.SwitchAttr(
        "--action",
        str,
        group="Targeted",

        excludes=["--all", ],
        default='build',
    )

    build_name: Any = cli.SwitchAttr(
        "--build_name",
        str,
        group="Targeted",

        excludes=["--all", ],
        default='test_aiservice',
    )
    dockerfile: Any = cli.SwitchAttr(
        "--dockerfile",
        str,
        group="Targeted",
        excludes=["--all", ],
        default='',
    )
    generate_all: Any = cli.Flag(
        ["--all"],
        help="Generate all of the templates.",
    )

    distro: Any = cli.SwitchAttr(
        "--model",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="The distro to use.",
        default=None,
    )
    pretrained_model: Any = cli.SwitchAttr(
        "--pretrained_model",
        str,
        group="Targeted",
        excludes=["--all"],
        help="The distro version",
    )

    model_name: Any = cli.SwitchAttr(
        "--model_name",
        str,
        group="Targeted",
        excludes=["--all"],
        help="The distro version",
    )

    model_path: Any = cli.SwitchAttr(
        "--model_path",
        str,
        group="Targeted",
        excludes=["--all"],
        help="The distro version",
        default='',
    )
    is_transformers: Any = cli.Flag(
        ["--is_transformers"],
        help="If Using Github Actions",
        default=True,
    )

    inference_task: Any = cli.SwitchAttr(
        "--inference_task",
        str,
        excludes=["--all"],
        group="Targeted",
        help="The cuda version to use. Example: '11.2'",
        default=None,
    )

    inference_script_path: Any = cli.SwitchAttr(
        "--inference_script_path",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="inference_script_path",
        default='',
    )

    project_id: Any = cli.SwitchAttr(
        "--project_id",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="git tag ",
        default=None,
    )
    base_image: Any = cli.SwitchAttr(
        "--base_image",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="base_image tag ",
        default="artifacts.iflytek.com/docker-private/atp/atp_general_image:v1.0.9",
    )
    docker_repo: Any = cli.SwitchAttr(
        "--docker_repo",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="",
        default="artifacts.iflytek.com/docker-private/atp/train",
    )
    maintainer: Any = cli.SwitchAttr(
        "--maintainer",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="image entrypoint ",
        default="ybyang7@iflytek.com",
    )
    image_tag: Any = cli.SwitchAttr(
        "--tag",
        str,
        group="Targeted",
        excludes=["--all", ],
        default="latest",
    )
    entrypoint: Any = cli.SwitchAttr(
        "--entrypoint",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="image entrypoint ",
        default=None,
    )

    cmd: Any = cli.SwitchAttr(
        "--cmd",
        str,
        group="Targeted",
        excludes=["--all", ],
        help="iamge cmd ",
        default=None,
    )

    extra_pip_packages: Any = cli.SwitchAttr(
        '--extra_pip_packages',
        str,
        group="Targeted",
        excludes=["--all", ],
        default="aiges pyatp",
    )
    auto_run: Any = cli.Flag(
        ["--auto_run"],
        help="If Using Github Actions",
        default=True,
    )

    # extracts arbitrary keys and inserts them into the templating context
    def extract_keys(self, val, arch=None):
        pass

    # For cudnn templates, we need a custom template context
    def output_cudnn_template(self, cudnn_version_name, input_template, output_path):
        pass

    def prepare_context(self):

        # The templating context. This data structure is used to fill the templates.
        self.vars = {
            "registry": self.get_regsitry(),
            "tag": self.generate_matrix_tags(),
        }

    def prepare_packages_txt(self) -> str:
        packages_txt = ""
        return packages_txt

    def prepare_model(self):
        model = self.model_name
        self.vars['model'] = model
        model_path = self.model_path

        if os.path.exists(model_path):
            self.vars['model_path'] = model_path

    def check_inference_path(self, p):
        # todo 校验真实p地址
        if not os.path.exists(p):
            log.error("not exists this inference dir %s" % p)
            return False
        if not os.path.isdir(p):
            log.error("not a  dir")
            return False

        else:
            files = os.listdir(p)
            if 'wrapper' not in files:
                log.error("please specify a dir which contains a wrapper.py")
                return False
            else:
                _path = os.path.join(p, 'wrapper')
                if not os.path.isdir(_path):
                    return False
                files2 = os.listdir(_path)
                if "wrapper.py" not in files2:
                    return False

        return True

    def prepare_inference_task_and_module(self):
        python_path = ''
        global dockerfile_dir
        # todo 拷贝推理文件以及目录
        if self.inference_script_path:
            valid = self.check_inference_path(self.inference_script_path)
            if valid:
                log.info("copy files to workspace")
                files = os.listdir(self.inference_script_path)
                target_dir = os.path.join(dockerfile_dir, 'wrapper')
                #                if not os.path.exists(target_dir):
                #                    os.makedirs(target_dir)
                for f in files:
                    if os.path.isdir(os.path.join(self.inference_script_path, f)):
                        shutil.copytree(os.path.join(self.inference_script_path, f), target_dir, dirs_exist_ok=True)
                    else:
                        shutil.copy(os.path.join(self.inference_script_path, f), os.path.join(dockerfile_dir, f))

                if 'requirements.txt' in files:
                    log.info("finding. requirements.txt")
                    self.vars['requirements_txt'] = "requirements.txt"
                if 'packages.txt' in files:
                    log.info("finding. packages.txt")
                    self.vars['packages_txt'] = "packages.txt"

            elif self.pretrained_model:
                # 使用pretrained_model 预制
                if not self.pretrained_model in SUPPORTED_TRAIN_TASKS:
                    raise ModuleNotFoundError("Not support this pretrained_model")
                log.info("copy pretrained innternal files to workspace")
                self.inference_script_path = SUPPORTED_TRAIN_TASKS_WRAPPER_MAP[self.pretrained_model]
                files = os.listdir(self.inference_script_path)

                target_dir = os.path.join(dockerfile_dir, 'wrapper')
                #                if not os.path.exists(target_dir):
                #                    os.makedirs(target_dir)
                for f in files:
                    if os.path.isdir(os.path.join(self.inference_script_path, f)):
                        shutil.copytree(os.path.join(self.inference_script_path, f), target_dir)
                    else:
                        shutil.copy(os.path.join(self.inference_script_path, f), os.path.join(dockerfile_dir, f))

                if 'requirements.txt' in files:
                    log.info("finding. requirements.txt")
                    self.vars['requirements_txt'] = "requirements.txt"
                if 'packages.txt' in files:
                    log.info("finding. packages.txt")
                    self.vars['packages_txt'] = "packages.txt"

            else:
                raise FileNotFoundError(self.inference_script_path)
        # transformer 内置
        elif self.is_transformers and self.inference_task:
            valid, m_path_dict = self.check_inference_task(self.inference_task)
            if valid:
                self.vars['inference_wrapper_path'] = m_path_dict[self.inference_task]
                log.info("is transformer.. using internal module: %s" % m_path_dict[self.inference_task])

            else:
                log.info("not valid %s" % self.inference_task)

                self.vars['inference_wrapper_path'] = "."
        else:
            self.vars['inference_wrapper_path'] = python_path

    def check_inference_task(self, task):
        transformers_dir = os.path.dirname(transformers.__file__)
        SUPPORTED_TASK = {}
        path_dict = {}
        fs = os.listdir(transformers_dir)
        for d in fs:
            if os.path.isdir(os.path.join(transformers_dir, d)):
                if d == "__pycache__":
                    continue
                if d not in SUPPORTED_TASK:
                    SUPPORTED_TASK[d] = []
                tasks = os.listdir(os.path.join(transformers_dir, d))
                for task in tasks:
                    p = os.path.join(transformers_dir, d, task)
                    if os.path.isdir(p):
                        SUPPORTED_TASK[d].append(task)
                        path_dict[task] = p
        valid = False
        for k in SUPPORTED_TASK.values():
            if task in k:
                valid = True
        return valid, path_dict

    def prepare_requirements_txt(self) -> str:
        requirements_txt = ""
        return requirements_txt

    def generate_dockerfile(self):
        if os.path.exists(TEMP_GEN_DIR):
            shutil.rmtree(TEMP_GEN_DIR)

        if not os.path.exists(TEMP_GEN_DIR):
            os.makedirs(TEMP_GEN_DIR)
        dockerfile_content = ''
        if os.path.exists(self.dockerfile):
            dockerfile_content = open(self.dockerfile).read()

        self.vars["base_image"] = self.base_image
        self.vars['maintainer'] = self.maintainer
        self.vars['pip_source'] = 'https://pypi.mirrors.ustc.edu.cn/simple/'

        if dockerfile_content:
            self.vars['dockerfile'] = dockerfile_content
        global dockerfile_dir
        dockerfile_dir = os.path.join(TEMP_GEN_DIR, 'run')
        if not os.path.exists(dockerfile_dir):
            os.makedirs(dockerfile_dir)

        self.prepare_inference_task_and_module()
        # extra pip packages
        if self.extra_pip_packages:
            self.vars['extra_pip_packages'] = self.extra_pip_packages

        # for render
        render_vars = {
            "vars": self.vars
        }
        st = self.render(render_vars)
        log.info("Generated Dockerfile %s " % st)
        with open(os.path.join(dockerfile_dir, Dockerfile), 'w') as dockerfile:
            dockerfile.write(st)
            dockerfile.close()
            log.info("write %s success" % os.path.abspath(os.path.join(dockerfile_dir, Dockerfile)))

        if self.auto_run:
            self.buildx()

    def mock_buildx(self):
        global dockerfile_dir
        log.info("buildx dockerfile in %s" % dockerfile_dir)
        log.info("building: ")
        with open(os.path.abspath(os.path.join(dockerfile_dir, Dockerfile)), 'r') as f:
            log.info(f.read())
        f.close()
        if not self.image_tag:
            image_tag = "latest"
        cache = " --no-cache "
        if self.cache:
            cache = ""

        cmd = f"docker buildx build . -t {self.docker_repo}/{self.build_name}:{self.image_tag} {cache} --push"
        log.info(cmd)

    def buildx(self):
        # 1. check buildx command
        global dockerfile_dir
        mock = True
        docker_bin = "/usr/local/bin/docker"
        if os.path.exists(docker_bin):
            mock = False

        if mock:
            self.mock_buildx()
            return
        pwd = os.getcwd()
        cache = " --no-cache "
        if self.cache:
            cache = ""
        cmd = f"docker buildx build . -t {self.docker_repo}/{self.build_name}:{self.image_tag} {cache} --push"

        log.info(cmd)
        os.chdir(dockerfile_dir)
        subprocess.call(cmd, shell=True)
        os.chdir(pwd)

    def render(self, render_vars):
        s = self.template.render(**render_vars)
        return s

    def get_regsitry(self):
        if self.use_github:
            return ECR_REPO
        return INNER_REPO

    def _load_template(self):
        tpl = os.path.join(os.path.dirname(pwd), "templates/Dockerfile.j2")
        if not os.path.exists(tpl):
            raise FileNotFoundError("not found %s" % tpl)
        log.info("load success j2 file.")
        self.template = self.template_env.from_string(open(tpl, "r").read())

    def _load_release_note(self):
        tpl = "./docker/templates/release-note/Note.md.j2"
        if not os.path.exists(tpl):
            raise FileNotFoundError("not found %s" % tpl)
        log.info("load success Note.md j2 file.")
        self.release_note = self.template_env.from_string(open(tpl, "r").read())

    def find_latest_gz(self):
        # 列出目录下所有的文件
        testdir = "."
        list = os.listdir(".")
        gzs = [x for x in list if x.startswith("pyatp") and x.endswith(".tar.gz")]
        # 对文件修改时间进行升序排列
        gzs.sort(key=lambda fn: os.path.getmtime(os.path.join(testdir, fn)))
        # 获取最新修改时间的文件
        filetime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(testdir, gzs[-1])))
        # 获取文件所在目录
        filepath = os.path.join(testdir, gzs[-1])
        print("find latest %s" % filepath)
        return filepath

    def upgrade_ailab_dir(self):
        print(".. Upgrading bulletin ailab build sdk!")

        cmd = " pip download  pyatp --no-deps --no-binary=:all:"
        subprocess.call(cmd, shell=True)

        latest_gz = self.find_latest_gz()

        cmds = [
            "pip config set global.index-url https://repo.model.xfyun.cn/api/packages/administrator/pypi/simple  &&  pip config set global.extra-index-url https://pypi.mirrors.ustc.edu.cn/simple/",
            'pip install  cchardet ',
        ]
        if latest_gz and os.path.exists(latest_gz):
            print("upgrading ailab dir: %s" % latest_gz)
            mkdir = "mkdir -p /home/ailab"
            unpress = "tar zxvf %s --strip-components 2 -C /home/ailab" % latest_gz
            cmds.append(mkdir)
            cmds.append(unpress)

        for cm in cmds:
            subprocess.call(cm, shell=True)

    def targeted(self):
        try:
            self.upgrade_ailab_dir()
        except Exception as e:
            print(e)

        if self.action == "build":
            log.info("building generating")
            self._load_template()
            self.generate_dockerfile()

        elif self.action == "release":
            log.info("releasing generating...")
        else:
            log.error("wrong action %s" % self.action)

    def release(self):
        pass

    def main(self):
        self.targeted()
        log.info("Done")


if __name__ == "__main__":
    Manager.run()
