# encoding: utf-8
"""
@project: djangoModel->service_manager
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 服务治理者
@created_time: 2023/5/7 15:43
"""
import importlib
import sys

import consul
import jsonrpc
from jsonrpc.proxy import ServiceProxy
import requests

from .custom_tool import force_transform_type, singleton_decorator


@singleton_decorator
class ServiceManager():
    """服务管理者"""
    providers = None  # 服务提供者
    service_clock_key = "SERVICE_CLOCK"  # 倒计时

    def __init__(self, host="127.0.0.1", port=8500):
        port, is_pass = force_transform_type(variable=port, var_type="int")
        self.consul_client = consul.Consul(host=host, port=port)
        # self.redis_client = get_redis_connection()

    # def check_expire(self):
    #     """检查获取的有效时间，是否"""
    #     return self.redis_client.ttl("SERVICE_CLOCK")

    def find_providers(self, service_id=None):
        """
        服务治理，再consul服务中发现服务提供者
        :return:
        """
        try:
            self.providers = self.consul_client.agent.services()
            if service_id:
                self.providers = self.providers.get(str(service_id), None)
            # # 创建定时锁，到期会从新拉取服务
            # has_clock = self.redis_client.get(self.service_clock_key)
            # if not has_clock:
            #     self.redis_client.set(self.service_clock_key, "")
            #     self.redis_client.expire(self.service_clock_key, 10)
            return self.providers, None
        except requests.exceptions.ConnectionError:
            return None, "无法连接服务治理服务端"

    def find_service(self, service_id=None, arg_version="2.0", system_rpc_entry="rpc", **kwargs):
        """
        服务之间通过rpc调用
        :param arg_version: 传递路由参数类型 @note 1.0：arg；2.0 kwargs;
        :param service_id: 服务ID
        :param system_rpc_entry: 服务监听基础路由
        :return: service_cal_handle, err
        """
        # ============== section 再consul获取活跃健康可调用的服务器 start =====================
        if not service_id:
            return None, "service_id无效，没有可调用服务"

        providers, err = self.find_providers()
        if not providers is None:
            provider = providers.get(str(service_id), {})
        else:
            return None, "没有可调用服务。请检查consul是否开启，并检查服务提供则是否运行。"
        # ============== section 再consul获取活跃健康可调用的服务器 end    =====================

        # ============== section 得到获取的服务名单,并开始调用服务 start    =====================
        tagged_addresses = provider.get("TaggedAddresses", {}).get("lan_ipv4", {}).get("Address", "127.0.0.1")
        port = provider.get("TaggedAddresses", {}).get("lan_ipv4", {}).get("Port", "8000")
        request_path = "http://" + tagged_addresses + ":" + str(port) + "/" + system_rpc_entry
        try:
            service = ServiceProxy(request_path, version=arg_version)
        except jsonrpc.proxy.ServiceProxyException:
            return None, "连接服务超时"
        return service, None
        # ============== section 得到获取的服务名单,并开始调用服务 end    =====================

    def put_service(self, route="", method=None, **kwargs):
        """
        注册方法提供rpc调用
        :param route: 路由
        :param method: 方法指针
        :return: None
        """

        @jsonrpc.jsonrpc_method(route)
        def rpc_register(*args, **kwargs):
            return method(*args, **kwargs)

        return rpc_register

    def dynamic_load_class(self, import_path: str = None, class_name: str = None, find_service_in_consul=False, **kwargs):
        """
        动态加载模块中的类,返回类的指针
        :param find_service_in_consul: 是否再consul中发现服务
        :param import_path: 导入类的文件路径
        :param class_name: 导入文件中的哪一个类
        :return: class_instance,err_msg
        """
        if find_service_in_consul:
            return self.find_providers(**kwargs)
        try:
            class_instance = getattr(sys.modules.get(import_path), class_name, None)
            if class_instance is None:
                import_module = importlib.import_module(import_path)
                class_instance = getattr(import_module, class_name)
            return class_instance, None
        except AttributeError:
            return None, "系统中不存在定位模块"
        except Exception as e:
            return None, str(e)
