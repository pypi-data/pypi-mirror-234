"""junoplatform.tools.cmd.py: junocli cmd implementation"""
from decouple import config as dcfg
import collections
from typing import Optional, Mapping
from junoplatform.meta.decorators import auth
import junoplatform
from junoplatform.io.utils import junoconfig, get_package_path
import zipfile
from typing import List
from pylint.reporters.text import TextReporter
from pylint.lint import Run
from io import StringIO
import json
import uuid
import traceback
import shutil
import requests
import logging
import yaml
import os
import click
__author__ = "Bruce.Lu"
__email__ = "lzbgt@icloud.com"
__time__ = "2023/07/20"


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')


class CMDBase(object):
    def __init__(self):
        self.juno_dir = os.path.expanduser('~') + '/.juno'
        os.makedirs(self.juno_dir, exist_ok=True)
        self.juno_file = self.juno_dir + '/config.yaml'
        self.juno_cfg = {}
        try:
            with open(self.juno_file, 'r', encoding='utf-8') as f:
                self.juno_cfg = yaml.safe_load(f)
                logging.debug(
                    f"self.juno_cfg: {self.juno_cfg}, type: {type(self.juno_cfg)}")
        except:
            pass


class OrderedGroup(click.Group):
    def __init__(self, name: Optional[str] = None, commands: Optional[Mapping[str, click.Command]] = None, **kwargs):
        super(OrderedGroup, self).__init__(name, commands, **kwargs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx: click.Context) -> Mapping[str, click.Command]:
        return self.commands


@click.group(cls=OrderedGroup)
@click.pass_context
def main(ctx, ):
    ctx.obj = CMDBase()


pass_base = click.make_pass_decorator(CMDBase)


@main.command()
@click.argument("api")
@click.option("-u", "--username", prompt=True)
@click.option("-p", "--password", prompt=True, hide_input=True,
              )
@pass_base
def login(base: CMDBase, api, username, password):
    '''must login success before all other commands
    '''
    auth = {"username": username, "password": password}
    logging.info(f"login at {api}")
    r = requests.post(f'{api}/login', data=auth,
                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if r.status_code != 200:
        if 'detail' in r.json():
            detail = r.json()['detail']
            logging.error(f"login error: {detail}")
            return
        else:
            logging.error(f"login error: {r.status_code}")
    token = r.json()['access_token']
    data = {"auth": auth, "token": token, "api": api}

    with open(base.juno_file, 'w', encoding='utf-8') as f:
        f.write(yaml.dump(data))
    logging.info("successfully logged in")


@main.command()
@click.argument('name')
@click.argument('plant')
@click.argument('module')
@pass_base
@auth
def create(base: CMDBase, name, plant: str, module: str):
    '''create an algo module with project NAME for PLANT-MODULE
    '''
    home = os.path.dirname(junoplatform.__file__)
    src = f"{home}/templates/main.py"
    if module.find("-") >= 0:
        logging.error(
            "MODULE name can't contain hyphen('-'), should use underscore('_') instead")
        exit(1)

    try:
        os.makedirs(name, exist_ok=False)
        shutil.copy2(src, name)
        doc = {"name": name, "version": "0.0.0", "author": os.getlogin(), "package_id": "int_temporary",
               "description": "template algo project", "plant": plant, "module": module}
        with open(f"{name}/project.yml", "w", encoding='utf-8') as f:
            yaml.dump(doc, f, sort_keys=False)
        input = {
            "tags": [
                "AI-T20502_DIS",
                "AI-T20501_DIS"
            ],
            "items": 1440,
            "sched_interval": 90
        }

        if plant == 'yudai':
            input["tags"] = ['AI_AT-P10503-DISP', 'COD2']

        if plant == 'yulin':
            input['tags'] = ['通道 1.设备 1.opc.group.3004FV00306_AI.PV',
                             '通道 1.设备 1.opc.group.3007LIT00202_AI.PV']

        with open(f"{name}/input.json", "w", encoding='utf-8') as f:
            json.dump(input, f, sort_keys=False)

        shutil.copy2(f"{home}/templates/config.json", name)

    except Exception as e:
        msg = traceback.format_exc()
        logging.error(f"failed to create project {name}: {e}")


@main.command()
@pass_base
@auth
def run(base):
    '''run a package locally for testing
    '''
    os.system("python main.py junocli")


@main.group(cls=OrderedGroup)
@click.pass_context
def package(ctx):
    pass


@main.group(cls=OrderedGroup)
@click.pass_context
def deploy(ctx):
    pass


@main.group(cls=OrderedGroup)
@click.pass_context
def plant(ctx):
    pass


@package.command()
@click.argument('conf_file', default="config.json")
@click.option('-t', '--tag', type=click.Choice(['algo', 'config', 'ac', 'other']), required=True)
@click.option('-m', '--message', required=True)
@click.option('-i', '--input', help="the path of input spec file", default="input.json")
@pass_base
@auth
def new(base: CMDBase, conf_file, tag, message, input):
    ''' make a new package
    '''
    try:
        lint = StringIO()  # Custom open stream
        reporter = TextReporter(lint)
        Run(["main.py"], reporter=reporter, exit=False)
        errors = lint.getvalue().split("\n")
        for x in errors:
            if "failed" in x or "fatal" in x:
                logging.error(x)
                logging.info("fix the error above and redo package")
                exit(1)

        package_id = uuid.uuid4().hex
        junoconfig['package_id'] = package_id

        def parse_version(s: str) -> List[int] | None:
            v = s.split(".")
            if len(v) != 3:
                return None
            try:
                return [int(x) for x in v]
            except:
                return None

        def inc_version(v: str, t: type):
            v = parse_version(v)
            if tag == 'algo':
                v[0] += 1
                junoconfig['tag'] = 'algo'
            elif tag == 'config':
                v[1] += 1
                junoconfig['tag'] = 'config'
            elif tag == 'ac':
                v[0] += 1
                v[1] += 1
                junoconfig['tag'] = 'ac'
            else:
                v[2] += 1
            junoconfig["version"] = ".".join([str(x) for x in v])

        if "version" not in junoconfig:
            junoconfig["version"] = "0.0.0"
        try:
            inc_version(junoconfig["version"], tag)
        except:
            logging.error(f"invalid version: {junoconfig['version']}")
            exit(1)

        junoconfig["message"] = message

        if "algo_cfg" in junoconfig:
            junoconfig.pop("algo_cfg")
        if "input_cfg" in junoconfig:
            junoconfig.pop('input_cfg')
        if "cloud" in junoconfig and "auth" in junoconfig["cloud"]:
            junoconfig["cloud"].pop("auth")

        with open('project.yml', 'w', encoding='utf-8') as f:
            yaml.safe_dump(junoconfig.data, f, sort_keys=False)

        logging.info(f"create new package success (updated project.yml):\n\tplant: {junoconfig['plant']}, \
                     module: {junoconfig['module']}, conf: {conf_file}\n\t{tag}: {message}\
                     \n\tid: {package_id}\n\tversion: {junoconfig['version']}")

        # dist
        os.makedirs("dist", exist_ok=True)
        module = junoconfig['module']
        plant = junoconfig['plant']
        arch = f'dist/{plant}-{module}-{junoconfig["package_id"]}.zip'
        with zipfile.ZipFile(arch, 'w') as f:
            for root, dirs, files in os.walk('./'):
                if root[-4:] == 'dist':
                    continue
                for file in files:
                    p = os.path.join(root, file)
                    f.write(p)
                    logging.info(f"added: {p}")
        logging.info(f"package stored in: {arch}")

    except Exception as e:
        msg = traceback.format_exc()
        logging.error(f"{e}:\n{msg}")


@package.command()
@click.argument('package_id', default="", required=False)
@pass_base
@auth
def pub(base: CMDBase, package_id):
    '''publish a package only (no deploy action)
    '''
    if not package_id:
        try:
            package_id = junoconfig["package_id"]
        except:
            logging.error(
                "must under project dir to run this command when no package_id provided(using project default)")
            exit(1)

    api = f'{base.juno_cfg["api"]}/package'
    logging.info(f"build package {package_id} to {api}")
    papath = get_package_path(junoconfig, package_id)

    logging.info(base.juno_cfg['token'])
    with open(papath, 'rb') as f:
        r = requests.post(api, files={'file': (f'{package_id}.zip', f, 'application/zip')},
                          headers={"Authorization": f"Bearer {base.juno_cfg['token']}"})
        if r.status_code != 200:
            msg = f"faild upload package {package_id} "
            if "detail" in r.json():
                msg += r.json()["detail"]
            logging.error(msg)
            logging.info(
                f"use below cmd to check package info:\n\tjunocli package info {package_id}")
        else:
            logging.info(f"successfully upload package {package_id}")
            logging.info(
                f"use cmd below to check build status ok (status == 1):\njunocli package info {package_id}")


@package.command()
@click.argument('package_id', required=False)
@pass_base
@auth
def repub(base: CMDBase, package_id):
    if not package_id:
        try:
            package_id = junoconfig["package_id"]
        except:
            logging.error(
                "must under project dir to run this command when no package_id provided(using project default)")
            exit(1)
    api = f'{base.juno_cfg["api"]}/package'
    params = {"package_id": package_id}
    r = requests.patch(api, params=params, headers={
                       "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild rebuild package in cloud:  {package_id} "
        if "detail" in r.json():
            msg += r.json()["detail"]
        logging.error(msg)
    else:
        logging.info(
            f"successfully summit recompile package request: {package_id}")


statusmap = {
    0: "building",
    1: "ready",
    2: "failed"
}


def info_package(base: CMDBase, package_id: str):
    '''info packages
    '''
    api = f'{base.juno_cfg["api"]}/package/info'
    params = {}
    params["package_id"] = package_id
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages"
        if "detail" in r.json():
            msg += ". detail: " + r.json()["detail"]
        return msg
    else:
        data = r.json()
        # data["config"] = json.loads(data["config"])
        # data["status"] = statusmap.get(data["status"])
        return data


@package.command()
@click.argument('package_id', required=False)
@pass_base
@auth
def info(base: CMDBase, package_id):
    '''info packages
    '''
    if not package_id:
        try:
            package_id = junoconfig["package_id"]
        except:
            logging.error(
                "must under project dir to run this command when no package_id provided(using project default)")
            exit(1)

    res = info_package(base, package_id)
    if isinstance(res, str):
        logging.error(res)
    else:
        logging.info(json.dumps(res, indent=2, ensure_ascii=False))


@package.command()
@click.argument('package_id', required=True)
@pass_base
@auth
def clone(base: CMDBase, package_id):
    '''clone package
    '''
    if not dcfg("ENABLE_DL", 0, cast=int):
        logging.error("package download is not enabled")

    api = f"{base.juno_cfg['api']}/package"
    params = {}
    params["package_id"] = package_id
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        logging.error(msg)
    else:
        with open(f"{package_id}.zip", "wb") as f:
            for c in r.iter_content(chunk_size=2048):
                if c:
                    f.write(c)


def list_packages(base: CMDBase, plant, module):
    '''list packages
    '''
    api = f"{base.juno_cfg['api']}/packages"
    params = {}
    if plant:
        params["plant"] = plant
    if module:
        params["module"] = module
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return msg
    else:
        res = []
        for x in r.json():
            # x["config"] = json.loads(x["config"])
            # x["status"] = statusmap.get(x["status"])
            res.append(x)
        res.reverse()
        return res


@package.command()
@click.option("-p", "--plant", default="")
@click.option("-m", "--module", default="")
@pass_base
@auth
def ls(base, plant, module):
    '''list packages
    '''
    res = list_packages(base, plant, module)
    if isinstance(res, str):
        logging.error(res)
    else:
        logging.info(
            f"results:\n{json.dumps(res, indent=2, ensure_ascii=False)}")


def deploy_package(base: CMDBase, package_id: str, kind: int, keep_field_spec: int):
    api = f"{base.juno_cfg['api']}/deploy"
    params = {}
    params["package_id"] = package_id
    params["kind"] = kind
    params["keep_spec_cfg"] = keep_field_spec
    r = requests.post(api, params=params, headers={
                      "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild deploy packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return Exception(msg)
    else:
        return r.json()


@deploy.command()
@click.argument('package_id', required=False)
@click.option("-k", "--keep", help="keep field configuration of UI", default=True, show_default=True)
@pass_base
@auth
def new(base, package_id, keep):
    '''deploy package
    '''
    if not package_id:
        try:
            package_id = junoconfig["package_id"]
        except:
            logging.error(
                "must under project dir to run this command when no package_id provided(using project default)")
            exit(1)
    keep_spec = 1
    if not keep:
        keep_spec = 0

    s = deploy_package(base, package_id, kind=0, keep_field_spec=keep_spec)
    if isinstance(s, Exception):
        logging.error(str(s))
    else:
        logging.debug(s)
        logging.info(
            f"deploy of package: {package_id} submitted.\nstatus can be viewed by run:\n\tjunocli deploy status")


@deploy.command()
@click.argument('package_id', required=False)
@pass_base
@auth
def rollback(base, package_id):
    '''rollback a package to previous version or specific id[optional]
    '''
    token = base.juno_cfg['token']
    if not package_id:
        try:
            package_id = junoconfig["package_id"]
        except:
            logging.error(
                "must under project dir to run this command when no package_id provided(using project default)")
            exit(1)
    res = info_package(base, package_id=package_id)
    if isinstance(res, str):
        logging.error(res)
        exit(1)

    row = list_current_deployed(base, plant=res["plant"], module=res["module"])
    if isinstance(row, str):
        logging.error(row)
        exit(1)

    row = {x["package_id"]: 1 for x in row}

    if package_id not in row:
        logging.error(
            f"package {package_id} is not currently deployed, no rollback allowed")
        exit(1)

    res = list_packages(base, plant=res["plant"], module=res["module"])
    if isinstance(res, str):
        logging.error(str)
    else:
        res.reverse()
        target_idx = -1
        for idx, x in enumerate(res):
            if x["package_id"] == package_id:
                target_idx = idx + 1

        if target_idx < len(res):
            while res[target_idx]["status"] != 1:
                target_idx += 1
                if target_idx >= len(res):
                    break

            if target_idx < len(res):
                new_id = res[target_idx]["package_id"]
                res = deploy_package(base, new_id, 1, 1)
                if not isinstance(res, Exception):
                    logging.info(
                        f"rollback from {package_id} to {new_id} submitted")
                else:
                    logging.error(res)
                return

        logging.error(
            f"no available package to rollback for {package_id}")


def list_deployments(base: CMDBase, plant, module, user, package_id):
    ''' list deoployments
    '''
    api = f"{base.juno_cfg['api']}/deploys"
    params = {}
    params["package_id"] = package_id
    params["plant"] = plant
    params["module"] = module

    if user == "me":
        params["username"] = params["username"] = os.getlogin()
    else:
        params["username"] = user
    logging.info(f"lsit deployments with params:\n{params}")

    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        logging.error(r.text)
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return msg
    else:
        data = r.json()
        data.reverse()
        return data


def list_current_deployed(base: CMDBase, plant: str, module=str):
    api = f"{base.juno_cfg['api']}/deploys/current"
    params = {}
    params["plant"] = plant
    params["module"] = module

    logging.info(f"list current deployments with params:\n{params}")
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return msg
    else:
        r.encoding = "utf-8"
        data = r.json()
        data.reverse()
        return data


@deploy.command()
@click.option("-p", "--plant", default="")
@click.option("-m", "--module", default="")
@click.option("-i", "--package_id", default="")
@click.option("-u", "--user", default="")
@pass_base
@auth
def ls(base, plant, module, user, package_id):
    ''' list deoployments
    '''
    res = list_deployments(base, plant, module, user, package_id)
    if isinstance(res, str):
        logging.error(res)
    else:
        logging.info(
            f"results:\n{json.dumps(res, indent=2,ensure_ascii=False)}")


@deploy.command()
@click.option("-p", "--plant", default="")
@click.option("-m", "--module", default="")
@pass_base
@auth
def status(base, plant, module):
    ''' check current deployments status
    '''
    res = list_current_deployed(base, plant=plant, module=module)
    if isinstance(res, str):
        logging.error(res)
    else:
        logging.info(
            f"results:\n{json.dumps(res, indent=2, ensure_ascii=False)}")


def list_pant(base: CMDBase, name: str):
    api = f"{base.juno_cfg['api']}/plants"
    params = {}
    params["name"] = name

    logging.info(f"list plants with params:\n{params}")

    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return msg
    else:
        data = r.json()
        data.reverse()
        return data


@plant.command()
@click.argument('name', required=False, default="")
@pass_base
@auth
def ls(base, name):
    ''' list plant(s)
    '''
    res = list_pant(base, name)
    if isinstance(res, str):
        logging.error(res)
    else:
        logging.info(
            f"results:\n{json.dumps(res, indent=2,ensure_ascii=False)}")


def add_plant(base: CMDBase, name, location, description):
    api = f"{base.juno_cfg['api']}/plant"
    plant = {}
    plant["id"] = 0
    plant["name"] = name
    plant["location"] = location
    plant["description"] = description

    data = {
        "plant": plant
    }

    logging.info(f"add plant with data:\n{data}")

    r = requests.post(api, json=data, headers={
                      "Authorization": f"Bearer {base.juno_cfg['token']}"})
    if r.status_code != 200:
        msg = f"faild add plant "
        if "detail" in r.json():
            msg += f'{r.json()["detail"]}'
        return msg
    else:
        None


@plant.command()
@click.argument('name', required=True)
@click.option('-l', '--location', required=True)
@click.option('-d', '--description', required=True)
@pass_base
@auth
def add(base, name, location, description):
    ''' add plant
    '''
    res = add_plant(base, name, location, description)
    if isinstance(res, str):
        logging.error(res)
