import inspect
from typing import List
import os
import json
import re
import sys
import logging
import subprocess


# 获取inspect的堆栈字符串
def get_call_stack(stack: List[inspect.FrameInfo]) -> str:
    res_str = ""
    for item in stack:
        res_str += f"\n\tfile:{item.filename} line:{item.lineno}"
    return res_str


def connect_window_share(share_path, username, password):
    valid_flag = os.path.isdir(share_path)
    if valid_flag:
        print(f"{share_path} is connected")
    else:
        print(f"{share_path} is not connected")
        mount_command = f"net use /user:{username} {share_path} {password}"
        # print(mount_command.encode('utf-8'))
        os.system(mount_command.encode("utf-8"))
        valid_flag = os.path.isdir(share_path)
        if valid_flag:
            print("Connection success.")
        else:
            raise Exception("Failed to find storage directory.")


# 替换key=value
def replace_code(file_path, key, value):
    fp = open(file_path, "r+", encoding="UTF-8")
    text = fp.read()
    re_key = re.sub(r"\.", "\\.", key, 0)
    search_text = f""" *%s {re_key}=.*"""
    match_obj = re.search(search_text, text, flags=0)
    if match_obj:
        replace = "%s=%s" % (key, value)
        text = re.sub(search_text, replace, text)
        fp.seek(0)
        fp.write(text)
        fp.truncate()
        fp.close()
        print("%s change ok" % file_path)
    else:
        print(f"{file_path} have not {key} {value}")


# def valid_json(json_path, schema_path=None):
#     json_data = None
#     schema_data = None
#     try:
#         with open(json_path, 'r', encoding='UTF-8') as f:
#             json_data = json.load(f)
#             if schema_path is None:
#                 curpath = os.path.abspath(os.path.dirname(json_path))
#                 schema_path = os.path.join(curpath, json_data["$schema"])
#             with open(os.path.join(schema_path), 'r', encoding='UTF-8') as f:
#                 schema_data = json.load(f)
#             print(f'检查json:{json_path}  规则:{schema_path}', end='  ')
#             validate(instance=json_data, schema=schema_data)
#     except Exception as e:
#         print(f'{json_path} 不合法,原因如下:\n{e}')
#         return False
#     print("合法")
#     return json_data, schema_data


def init_log(logpath: str = None,level=logging.INFO):
    root = logging.getLogger()
    if logpath:
        logfile = open(logpath, encoding="utf-8", mode="a")  # 防止中文乱码
        logging.basicConfig(
            level=level,
            stream=logfile,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        printhandle = logging.StreamHandler(sys.stdout)
        printhandle.setLevel(logging.INFO)
        root.addHandler(printhandle)
    else:
        logging.basicConfig(
            level=level,
            stream=sys.stdout,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )


def run_cmd_popen(cmd, encoding="utf-8") -> str:
    pipe = subprocess.PIPE
    proc = subprocess.Popen(
        cmd, stdout=pipe, stderr=pipe, universal_newlines=True, encoding=encoding
    )
    out, err = proc.communicate()
    if err:
        raise Exception(err)
    return out


def get_cmd_output(cmd: str) -> str:
    cmd_arr = re.split(r"\s+", cmd)
    cmd_arr = list(x for x in cmd_arr if len(x.strip()) > 0)
    return get_cmdarr_output(cmd_arr)


def _decode_bytes(byte_text: bytes):
    try:
        res_text = byte_text.decode("utf-8")
    except UnicodeDecodeError:
        res_text = byte_text.decode("gbk")
    return res_text


def get_cmdarr_output(cmdarr: List[str]) -> str:
    try:
        output = subprocess.check_output(cmdarr, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        err_output = _decode_bytes(err.output)
        raise Exception(f"run cmd {cmdarr} err:{err_output}")
    return _decode_bytes(output)
