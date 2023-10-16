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
        parser.add_argument(
            "--delete",
            action="store_true",
            help="是否执行删除测试用例",
        )
        parser.add_argument(
            "--add",
            action="store_true",
            help="是否执行添加测试用例",
        )
        parser.add_argument(
            "--edit",
            action="store_true",
            help="是否执行编辑测试用例",
        )
        parser.add_argument(
            "--list",
            action="store_true",
            help="是否执行列表测试用例",
        )

    # 核心业务逻辑，通过options字典接收name参数值，拼接字符串后输出
    def handle(self, *args, **options):
        from xj_user.services.user_apply_services import UserApplyServices
        if options.get("add"):
            data, err = UserApplyServices.add_apply_record(params={
                "apply_type_id": 1,
                "user_id": 116,
                "remark": "加急备注",
                "verify_files": {"id_card_front": "https://baidu.com"}
            })
            print(data, err)
        if options.get("edit"):
            data, err = UserApplyServices.edit_apply_record(
                params={
                    "apply_type_id": 1,
                    "user_id": 1,
                    "remark": "加急备注",
                    "verify_files": {"id_card_front": "https://baidu.com"},
                    "reject_reason": "格式不合格,重新制作",
                    "verify_user_id": 298,
                    # "result": UserApplyServices.VERIFY_PASS
                    "result": UserApplyServices.VERIFY_REJECT

                },
                pk=6
            )
            print(data, err)

        if options.get("list"):
            data, err = UserApplyServices.apply_record_list()
            print(data, err)
