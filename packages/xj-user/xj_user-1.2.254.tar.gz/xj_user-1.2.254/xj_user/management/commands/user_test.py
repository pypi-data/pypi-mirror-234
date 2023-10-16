# encoding: utf-8
"""
@project: djangoModel->sync_table_structure
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 更新表结构
@created_time: 2023/8/22 9:09
"""
from django.core.management import BaseCommand


class Command(BaseCommand):
    # 帮助文本, 一般备注命令的用途及如何使用。
    help = "测试调试结构"

    # 给命令添加一个名为name的参数
    def add_arguments(self, parser):
        pass

    # 核心业务逻辑，通过options字典接收name参数值，拼接字符串后输出
    def handle(self, *args, **options):
        from xj_user.services.user_apply_services import UserApplyServices
        data, err = UserApplyServices.add_apply_record(params={
            "apply_type_id": 1,
            "user_id": 1,
            "remark": "加急备注",
            "verify_files": {"id_card_front": "https://baidu.com"}
        })
        print(data, err)
