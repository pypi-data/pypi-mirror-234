# encoding: utf-8
"""
@project: djangoModel->service_register
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 对外开放服务调用注册白名单
@created_time: 2023/1/12 14:29
"""

import xj_user
from xj_user.utils.service_manager import ServiceManager
from .services import user_service, user_detail_info_service, user_relate_service

# 对外服务白名单
register_list = [
    {
        "service_name": "get_list_detail",
        "pointer": user_detail_info_service.DetailInfoService.get_list_detail
    },
    {
        "service_name": "get_detail",
        "pointer": user_detail_info_service.DetailInfoService.get_detail
    },
    {
        "service_name": "create_or_update_detail",
        "pointer": user_detail_info_service.DetailInfoService.create_or_update_detail
    },
    {
        "service_name": "bind_user_identity",
        "pointer": user_service.UserService.bind_user_identity
    },
    {
        "service_name": "bind_bxtx_relate",
        "pointer": user_relate_service.UserRelateToUserService.bind_bxtx_relate
    },
]

server_manager = ServiceManager()


# 遍历注册
def register():
    for i in register_list:
        setattr(xj_user, i["service_name"], i["pointer"])
        server_manager.put_service(route=i["service_name"], method=i["pointer"])


if __name__ == '__main__':
    register()
