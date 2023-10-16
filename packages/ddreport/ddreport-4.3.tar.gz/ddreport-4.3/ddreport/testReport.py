#############################################
# File Name: ddreport
# Author: duanliangcong
# Mail: 137562703@qq.com
# Created Time:  2022-11-02 15:00:00
#############################################
from _pytest.python import Function
from _pytest.runner import runtestprotocol
from jsonpath import jsonpath
from collections.abc import Iterable
from ddreport.api import CustomQuery
from ddreport.db import PytestMysql
from ddreport.func import PytestFunctions
from ddreport.handle import Process
import requests
import pytest
import time
import json
import os, sys
import re
import ast
import traceback


requests.packages.urllib3.disable_warnings()

test_result = {
    "title": "",
    "desc": "",
    "tester": "",
    "start_time": "",
    "end_time": "",
    "failed": 0,
    "passed": 0,
    "skipped": 0,
    "error": 0,
    "cases": [],
}

dict_data = {
    'show_success': False
}

Result = {"nowResponse": {}}


class Gvalues(object):
    __slots__ = ('__value')

    def __init__(self):
        self.__value = dict()

    def set(self, key, value):
        self.__value.update({key: value})

    def get(self, key):
        return self.__value.get(key)

    def append(self, key, value):
        self.__value.get(key).append(value)

    def extend(self, key, value):
        self.__value.get(key).extend(value)

GG = Gvalues()

dd_paramet = dict()


def getEnvData(env_path, env_name):
    try:
        with open(env_path, 'r', encoding='utf-8')as f:
            envs = json.loads(f.read())
        return jsonpath(envs, f'$..[?(@.env_name=="{env_name}")]')[0]
    except Exception:
        return dict()


def node_handle(node, item, call):
    d = dict()
    # 模块
    d['model'] = item.module.__name__
    # 类
    d['classed'] = '' if item.parent.obj == item.module else item.parent.obj.__name__
    # 方法
    d['method'] = item.originalname
    # 描述
    d['doc'] = item.function.__doc__
    # 响应时间
    d['duration'] = call.duration
    # 结果
    d['status'] = node.outcome
    # 详细内容
    if node.sections:
        d["print"] = ''.join(node.sections[0][1:]).replace('<', '&lt;').replace('>', '&gt;')
    # 异常信息展示
    if call.excinfo:
        try:
            if d['status'] == 'skipped':
                d["skipped"] = call.excinfo.value.msg.replace('<', '&lt;').replace('>', '&gt;')
            else:
                d.update(call.excinfo.value.value.query_info)
                d.update(call.excinfo.value.value.error_info)
        except Exception:
            e1 = str(call.excinfo._excinfo[1]).replace('<', '&lt;').replace('>', '&gt;')
            e2 = str(call.excinfo._striptext).replace('<', '&lt;').replace('>', '&gt;')
            e3 = str(call.excinfo._traceback[0]).replace('<', '&lt;').replace('>', '&gt;')
            d.update(dict(msg_dict=f"{e1}\n{e2}\n{e3}"))
    # 打印正确请求
    if GG.get("@@ddreportQuery") and dict_data['show_success'] is True:
        queryData = GG.get("@@ddreportQuery")
        if queryData:
            Pro = Process()
            Pro.data_process(queryData, None)
            d.update(Pro.query_info)
    return d


def pytest_addoption(parser):
    """添加main的可调用参数"""
    group = parser.getgroup("testreport")
    group.addoption(
        "--ddreport",
        action="store",
        default=None,
        help="测试报告标识",
    )
    group.addoption(
        "--title",
        action="store",
        default=None,
        help="测试报告最顶部标题",
    )
    group.addoption(
        "--desc",
        action="store",
        default=None,
        help="当前测试报告的说明",
    )
    group.addoption(
        "--tester",
        action="store",
        default=None,
        help="测试人员",
    )
    group.addoption(
        "--env_path",
        action="store",
        default=None,
        help="环境配置路径",
    ),
    group.addoption(
        "--env_name",
        action="store",
        default=None,
        help="环境名称",
    ),
    group.addoption(
        "--receive",
        action="store",
        default=None,
        help="接收一个字典类型的参数",
    ),
    group.addoption(
        "--api_success",
        action="store",
        default=None,
        help="是否打印正确的api请求信息",
    ),


def pytest_sessionstart(session):
    test_result['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    test_result['title'] = session.config.getoption('--title') or ''
    test_result['tester'] = session.config.getoption('--tester') or ''
    test_result['desc'] = session.config.getoption('--desc') or ''
    # 是否展示正确的请求及响应信息
    success_show = session.config.getoption('--api_success')
    try:
        if success_show.upper() == "TRUE" or int(success_show) == 1:
            dict_data['show_success'] = True
        else:
            dict_data['show_success'] = False
    except Exception:
        dict_data['show_success'] = False
    # 记录命令传过来的参数
    receive_dict = session.config.getoption("--receive")
    if receive_dict:
        try:
            receive_dict = json.loads(receive_dict)
        except Exception:
            try:
                receive_dict = ast.literal_eval(receive_dict)
            except Exception:
                receive_dict = {}
        for k, v in receive_dict.items():
            GG.set(k, v)


def pytest_sessionfinish(session, exitstatus):
    def set_default(obj):
        if isinstance(obj, (list, dict)):
            return str(obj).replace('<', '&lt;').replace('>', '&gt;')
    test_result['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    ddreport = session.config.getoption('--ddreport')
    if ddreport:
        report_dirOrFile = ddreport.replace('\\', '/').strip()
        if not report_dirOrFile.endswith('.html'):
            report_dir, report_name = report_dirOrFile, f'testReport {time.strftime("%Y-%m-%d_%H%M%S")}.html'
        else:
            report_dir, report_name = '/'.join(report_dirOrFile.split('/')[:-1]), report_dirOrFile.split('/')[-1]
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        report_save_path = os.path.join(report_dir, report_name)
        # 读取测试报告文件
        template_path = os.path.join(os.path.dirname(__file__), './template')
        with open(f'{template_path}/index.html', 'r', encoding='utf-8')as f:
            template = f.read()
        report_template = template.replace('templateData', json.dumps(test_result))
        with open(report_save_path, 'w', encoding='utf-8') as f:
            f.write(report_template)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    call.duration = '%.2f' % call.duration          # 科学计数转普通格式
    info = {}
    if report.when == 'call':
        # 过滤不需要的funcargs
        dd_paramet.clear()
        params_keys = [om.args[0] for om in item.own_markers if om.args]
        for k in item.fixturenames:
            if k in ["_session_faker", "request"]:
                continue
            elif k.startswith("dd__"):
                continue
            elif params_keys and k in params_keys:
                continue
            else:
                dd_paramet[k] = item.funcargs[k]
        test_result[report.outcome] += 1
        info = node_handle(report, item, call)
    elif report.outcome == 'failed':
        report.outcome = 'error'
        test_result['error'] += 1
        info = node_handle(report, item, call)
    elif report.outcome == 'skipped':
        test_result[report.outcome] += 1
        info = node_handle(report, item, call)
    if report.when == 'teardown':
        # 是否有图片信息
        if GG.get("@ddImage"):
            Result["nowResponse"].update(dict(img=GG.get("@ddImage")))
        test_result["cases"].append(Result["nowResponse"])
        GG.set("@@ddreportQuery", None)
        GG.set("@ddImage", None)
    Result["nowResponse"] = info


@pytest.fixture(scope='session')
def ddreport(request):
    # 环境获取
    env_path = request.config.getoption("--env_path")
    env_name = request.config.getoption("--env_name")
    get_env = getEnvData(env_path, env_name)
    host = get_env.get('host') or ''
    mysql = get_env.get('mysql')
    return MyFixture(host, mysql)


class MyFixture:
    def __init__(self, host, mysql):
        self.GVALUE = GG
        self.API = CustomQuery(GG, host)
        self.FC = PytestFunctions()
        self.MYSQL = None
        if mysql:
            from ddreport.db import PytestMysql
            self.MYSQL = PytestMysql(mysql)
        super().__init__()


def pytest_generate_tests(metafunc):
    fixturenames = metafunc.definition.fixturenames
    dd_parames = [i for i in fixturenames if i.startswith("dd__")]
    if dd_parames:
        key = dd_parames[0]
        metafunc.parametrize(key, [])


def pytest_runtest_protocol(item, nextitem):
    # copy-item-function
    def copy_item(curitem):
        newitem = Function.from_parent(name=curitem.originalname, parent=curitem.parent, callspec=curitem.callspec,
                                       fixtureinfo=curitem._fixtureinfo, originalname=curitem.originalname)
        return newitem

    fixturenames = [i for i in item.fixturenames if i.startswith("dd__")]
    if fixturenames:
        key = fixturenames[0]
        parametrize = GG.get(key[4:]) or []
        if parametrize and isinstance(parametrize,Iterable):
            for n, paramet in enumerate(parametrize):
                new_item = copy_item(item)
                new_item.own_markers = []
                new_item.callspec.params[key] = paramet
                new_item.callspec.indices[key] = n
                new_item.callspec._idlist.append(f"{key}{n}")
                del new_item.callspec._idlist[0]
                new_item.name = new_item.originalname + f"[{key}{n}]"
                new_nodeid = '::'.join(new_item.nodeid.split("::")[:-1] + [new_item.name])
                new_item._nodeid = new_nodeid
                for k, v in dd_paramet.items():
                    new_item.funcargs[k] = dd_paramet[k]
                #new_item.ihook.pytest_runtest_logstart(nodeid=new_nodeid, location=item.location)
                runtestprotocol(new_item, nextitem=None)
                #new_item.ihook.pytest_runtest_logfinish(nodeid=new_item._nodeid, location=item.location)
            return True
    else:
        for k, v in dd_paramet.items():
            item.funcargs[k] = dd_paramet[k]

def pytest_report_teststatus(config, report):
    # 更新终端打印（.  s   F  E）
    if report.outcome == 'error':
        return report.outcome, 'E', None
