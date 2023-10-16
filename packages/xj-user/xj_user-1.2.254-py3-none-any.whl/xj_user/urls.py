# _*_coding:utf-8_*_

from django.urls import re_path

from .apis import user_apply_apis
from .apis import user_cards_apis
from .apis import user_contact_book
from .apis import user_detail_info
from .apis import user_edit
from .apis import user_info
from .apis import user_list
from .apis import user_login
from .apis import user_login_short_message
from .apis import user_login_wechat
from .apis import user_password
from .apis import user_platform
from .apis import user_relate_apis
from .apis import user_sso_serve
from .apis import user_statistics
from .apis.user_add import UserAdd
from .apis.user_login_main import UserLoginMain
from .service_register import register
from .apis import user_subcompany_apis

# 应用名称
app_name = 'xj_user'

register()
# 应用路由
urlpatterns = [
    # 平台相关API
    re_path(r'^platform/?$', user_platform.UserPlatform.as_view(), name="用户的平台CRUD"),
    re_path(r'^platform_list/?$', user_platform.UserPlatform.list, name="用户的平台列表"),
    re_path(r'^get_user_platform/?$', user_platform.UserPlatform.get_user_platform, name="获取当前用户的平台信息"),

    # 登录操作
    re_path(r'^login/?$', user_login.UserLogin.as_view(), name="用户登录"),
    re_path(r'^login_main/?$', UserLoginMain.login_main, name="登录总接口"),
    re_path(r'^js_sdk/?$', user_sso_serve.UserSsoServe.get_js_sdk, name="微信公众号JS-SDK"),
    re_path(r'^login_short_message/?$', user_login_short_message.ShortMessageLogin.sms_login, name="短信登录"),
    re_path(r'^login/?$', user_login.UserLogin.as_view(), name="原始账号密码登录接口"),
    re_path(r'^sso_serve/?$', user_sso_serve.UserSsoServe.as_view(), ),
    re_path(r'^login_wechat/?$', user_login_wechat.WechetLogin.as_view(), name="微信登录"),
    re_path(r'^register/?$', UserLoginMain.register, name="用户注册"),
    re_path(r'^add/?$', UserAdd.add, name="管理员添加用户"),
    re_path(r'^secondary_authorization/?$', UserLoginMain.secondary_authorization, name="二次授权"),
    re_path(r'^bind_phone/?$', UserLoginMain.bind_phone, name="绑定手机号"),

    # 个人信息相关
    re_path(r'^info/?$', user_info.UserInfo.as_view(), name="产看个人信息"),
    re_path(r'^edit/?$', user_edit.UserEdit.user_edit, name="user_list_detail用户信息编辑"),
    re_path(r'^delete/?$', user_edit.UserEdit.as_view(), name="用户删除"),
    re_path(r'^password/?$', user_password.UserPassword.as_view(), name="用户修改验证码"),
    re_path(r'^list/?$', user_list.UserListAPIView.as_view(), name="用户列表"),
    re_path(r'^bind_identity/?$', user_edit.UserEdit.bind_identity, name="用户身份绑定"),

    # 详细信息以及绑定信息
    re_path(r'^detail/?$', user_detail_info.UserDetail.as_view(), name="查看用户的详细信息"),
    re_path(r'^list_detail/?$', user_detail_info.UserListDetail.as_view(), name="用户详细信息列表"),
    re_path(r'^detail_edit/?$', user_detail_info.UserDetailEdit.as_view(), name="用户详细信息编辑"),
    re_path(r'^detail_extend_fields/?$', user_detail_info.UserDetailExtendFields.as_view(), name="用户详细信息扩展字段映射"),
    re_path(r'^bank_card/?(?P<detail_id>\d+)?$', user_cards_apis.UserBankAPIView.as_view(), name="银行卡管理CRUD"),
    re_path(r'^contact_book/?$', user_contact_book.UserContactBook.as_view(), name="用户通讯录"),

    # 用户关系-以及相关的营销或等接口
    re_path(r'^relate_type/?$', user_relate_apis.UserRelateTypeApis.as_view(), name="关系类型CURD"),
    re_path(r'^relate_user/?$', user_relate_apis.UserRelateToUserApis.as_view(), name="用户与关系关系类型映射的CRUD"),
    re_path(r'^distribution_relate/?$', user_relate_apis.UserRelateToUserApis.distribution_relate, name="用戶分三級分銷關係查詢"),

    # 镖行业务接口
    re_path(r'^bind_bxtx_relate/?$', user_relate_apis.UserRelateToUserApis.bind_bxtx_relate, name="镖行业务接口-绑定业务员和邀请人"),
    re_path(r'^bxtx_relate_user/?$', user_relate_apis.UserRelateToUserApis.bxtx_relate_user, name="镖行业务接口-查看下级用户"),

    # 劳务通业务接口
    re_path(r'^relate_user_tree/?$', user_relate_apis.UserRelateToUserApis.relate_user_tree, name="劳务通-树状结构接口"),
    re_path(r'^laowu_bind_bxtx_relate/?$', user_relate_apis.UserRelateToUserApis.laowu_bind_bxtx_relate, name="劳务通-绑定关系"),

    # 待分离接口
    re_path(r'^statistics/?$', user_statistics.UserStatisticsAPI.as_view(), ),


    # 用户审批接口
    re_path(r'^apply_type_list/?$', user_apply_apis.UserApplyApis.apply_type_list, name="审配类型列表"),
    re_path(r'^apply_add/?$', user_apply_apis.UserApplyApis.add_user_apply, name="提交用户审批"),
    re_path(r'^agree_apply/?$', user_apply_apis.UserApplyApis.agree_user_apply, name="同意用户审批"),
    re_path(r'^disagree_apply/?$', user_apply_apis.UserApplyApis.disagree_user_apply, name="同意用户审批"),
    re_path(r'^apply_list/?$', user_apply_apis.UserApplyApis.user_apply_list, name="用户审批列表"),
    re_path(r'^apply_statistics/?$', user_apply_apis.UserApplyApis.user_apply_statistics, name="用户审批统计"),

    # 分子公司接口
    re_path(r'^subcompany/?(?P<detail_id>\d+)?$', user_subcompany_apis.UserSubCompanyAPIView.as_view(), name="分子公司管理"),

]
