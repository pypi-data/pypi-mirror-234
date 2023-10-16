from junoplatform.io.utils import junoconfig
import yaml
import os
import logging
import requests
import json


def info_package(package_id: str = ""):
    '''info packages
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - dict; otherwise - errmsg(str)
    '''
    api = f'{junoconfig["cloud"]["api"]}/package/info'
    params = {}
    if not package_id:
        package_id = junoconfig["package_id"]

    params["package_id"] = package_id
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {junoconfig['cloud']['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages"
        if "detail" in r.json():
            msg += ". detail: " + r.json()["detail"]
        return 1, msg
    else:
        data = r.json()
        data["config"] = json.loads(data["config"])
        # data["status"] = statusmap.get(data["status"])
        return 0, data


def list_packages(plant, module):
    '''list packages
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - list[dict]; otherwise - errmsg(str)
    '''
    api = f"{junoconfig['cloud']['api']}/packages"
    params = {}
    if plant:
        params["plant"] = plant
    if module:
        params["module"] = module

    logging.info(f"list packages with params:\n{params}")
    r = requests.get(api, params=params, headers={
                     "Authorization": f"Bearer {junoconfig['cloud']['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return 1, msg
    else:
        res = []
        for x in r.json():
            x["config"] = json.loads(x["config"])
            # x["status"] = statusmap.get(x["status"])
            res.append(x)
        res.reverse()
        return 0, res


def deploy_package(package_id: str, kind: int, keep_field_cfg: int):
    '''deploy a package
    kind: int, # 0: deploy , 1 rollback, 2: reconfig, 3: cloud api rollback
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - None; otherwise - errmsg(str)
    '''
    api = f"{junoconfig['cloud']['api']}/deploy"
    params = {}
    params["package_id"] = package_id
    params["kind"] = kind
    params["keep_spec_cfg"] = keep_field_cfg
    r = requests.post(api, params=params, headers={
                      "Authorization": f"Bearer {junoconfig['cloud']['token']}"})
    if r.status_code != 200:
        msg = f"faild fetch packages "
        if "detail" in r.json():
            msg += r.json()["detail"]
        return 1, msg
    else:
        return 0, None


def rollback(package_id: str = ""):
    '''rollback a package to previous version or specific id[optional]
    returns: 
        tuple(code, data)
            code: 0 - success; otherwise - failure
            data: when(code==0) - new package_id(str); otherwise - errmsg(str)
    '''
    token = junoconfig['cloud']['token']
    if not package_id:
        try:
            package_id = junoconfig["package_id"]
        except:
            logging.error("no package id")
            exit(1)
    code, res = info_package(package_id=package_id)
    if code:
        logging.error(f"failed to get package info: {str}")
        return 1, res
    else:
        code, res = list_packages(res["plant"], res["module"])
        if code:
            logging.error(res)
            return 2, res
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
                    code, res = deploy_package(new_id, 3, 1)
                    if not code:
                        logging.info(
                            f"rollback from {package_id} to {new_id} submitted")
                        return 0, {new_id}
                    else:
                        logging.error(res)
                        return 3, res

            msg = f"no available package to rollback for {package_id}"
            logging.error(msg)
            return 4, msg
