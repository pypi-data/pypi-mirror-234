from django.contrib import admin

from config.config import JConfig
# 引入用户平台
from .models import *

config = JConfig()


class BaseInfoAdmin(admin.ModelAdmin):
    fields = (
        'id', 'uuid', 'user_no', 'user_name', 'nickname', 'full_name', 'phone', 'email', 'user_type', 'privacies',
        'user_info', 'register_ip', 'register_time', 'is_delete')
    list_display = (
        'id', 'uuid_short', 'user_no', 'user_name', 'nickname', 'full_name', 'phone', 'email', 'user_type',
        'user_info_short', 'privacies_short', 'register_ip', 'register_time', 'is_delete')
    list_display_links = ['user_name', 'phone', 'email']
    list_filter = ['user_type']
    search_fields = ('uuid', 'user_name', 'full_name', 'nickname', 'email', 'phone')
    readonly_fields = ['id', 'uuid']
    list_per_page = 20


class DetailInfoAdmin(admin.ModelAdmin):
    fields = (
        'id', 'user', 'real_name', 'sex', 'birth', 'tags', 'signature', 'avatar', 'cover', 'id_card_type', 'id_card_no',
        'language', 'region_code', 'more',
        'field_1', 'field_2', 'field_3', 'field_4', 'field_5', 'field_6', 'field_7', 'field_8', 'field_9',
        'field_10', 'field_11', 'field_12', 'field_13', 'field_14', 'field_15'
    )
    list_display = (
    'user', 'real_name', 'sex', 'birth', 'tags', 'avatar', 'cover', 'language', 'region_code')
    search_fields = ('user__user_name', 'user__full_name', 'real_name')
    readonly_fields = ['id']
    raw_id_fields = ['user']
    list_per_page = 20


class AuthAdmin(admin.ModelAdmin):
    fields = ('id', 'platform', 'user', 'password', 'salt', 'algorithm', 'token', 'ticket',
              'last_update_ip', 'create_time', 'update_time')
    list_display = ('platform', 'user', 'password', 'salt', 'algorithm', 'token_short',
                    'ticket_short', 'create_time', 'update_time')
    list_display_links = ['user']
    search_fields = ('user__user_name', 'user__full_name')
    list_filter = ['platform']
    readonly_fields = ['id', 'create_time', 'update_time']
    raw_id_fields = ['user']
    list_per_page = 20

    # def platform(self, obj):
    #     return obj.platform


class ExtendFieldAdmin(admin.ModelAdmin):
    fields = ('id', 'field', 'field_index', 'description', 'type', 'config', 'default', 'sort')
    list_display = ('field', 'field_index', 'description', 'type', 'config', 'default', 'sort')
    readonly_fields = ['id']


class AccessLogAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'ip', 'create_time', 'client_info', 'more',)
    list_display = ('user', 'ip', 'create_time', 'client_info',)
    readonly_fields = ['id', 'create_time']
    raw_id_fields = ['user']


class HistoryAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'field', 'old_value', 'new_value', 'create_time',)
    list_display = ('user', 'field', 'old_value', 'new_value', 'create_time',)
    readonly_fields = ['id', 'create_time']
    raw_id_fields = ['user']


class RestrictRegionAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'region_code',)
    list_display = ('user', 'region_code',)
    readonly_fields = ['id']
    raw_id_fields = ['user']


class PlatformAdmin(admin.ModelAdmin):
    fields = ('id', 'platform_id', 'platform_code', 'platform_name')
    list_display = ('id', 'platform_id', 'platform_code', 'platform_name')
    list_display_links = ['platform_code']
    search_fields = ('platform_id', 'platform_name', 'platform_code')


class PlatformsToUsersAdmin(admin.ModelAdmin):
    fields = ('user', 'platform', 'platform_user_id',)
    list_display = ('platform', 'user', 'platform_user_id',)
    # readonly_fields = ['id']
    raw_id_fields = ['user']


class ContactBookAdmin(admin.ModelAdmin):
    fields = ('id', 'user_id', 'friend', 'phone', 'phones', 'telephone', 'telephones',
              'email', 'qq', 'address', 'more', 'remarks')
    list_display = ('id', 'user_id', 'friend', 'phone', 'phones', 'telephone', 'telephones',
                    'email', 'qq', 'address', 'more', 'remarks')
    readonly_fields = ['id']
    raw_id_fields = ['user_id']


class UserSsoServeAdmin(admin.ModelAdmin):
    fields = ('id', 'sso_code', 'sso_name', 'sso_url', 'description', 'sso_appid', 'sso_account_id')
    list_display = ('id', 'sso_code', 'sso_name', 'sso_url', 'description')
    readonly_fields = ['id']


class UserSsoToUserAdmin(admin.ModelAdmin):
    fields = ('id', 'sso_serve', 'user', 'sso_unicode', 'sso_ticket', 'union_code',)
    list_display = ('id', 'sso_serve', 'user', 'sso_unicode', 'sso_ticket', 'union_code')
    readonly_fields = ['id']
    raw_id_fields = ['user']


class UserRelateTypeAdmin(admin.ModelAdmin):
    fields = ("id", "relate_key", "relate_name", "is_multipeople", "description",)
    list_display = ("id", "relate_key", "relate_name", "is_multipeople", "description",)
    readonly_fields = ['id']


class UserRelateToUserAdmin(admin.ModelAdmin):
    fields = ("id", "user", "with_user", "user_relate_type",)
    list_display = ("id", "user", "with_user", "user_relate_type",)
    readonly_fields = ['id']
    raw_id_fields = ['user']


class UserBankCardsAdmin(admin.ModelAdmin):
    fields = ("id", "user", "bank_card_num", "open_account_bank")
    list_display = ("id", "user", "bank_card_num", "open_account_bank")
    readonly_fields = ['id']
    raw_id_fields = ['user']


admin.site.register(BaseInfo, BaseInfoAdmin)
admin.site.register(DetailInfo, DetailInfoAdmin)
admin.site.register(Auth, AuthAdmin)
admin.site.register(ExtendField, ExtendFieldAdmin)
admin.site.register(AccessLog, AccessLogAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(RestrictRegion, RestrictRegionAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(PlatformsToUsers, PlatformsToUsersAdmin)
# admin.site.register(Permission, PermissionAdmin)
# admin.site.register(PermissionValue, PermissionValueAdmin)
# admin.site.register(Group, GroupAdmin)
admin.site.register(ContactBook, ContactBookAdmin)
admin.site.register(UserSsoServe, UserSsoServeAdmin)
admin.site.register(UserSsoToUser, UserSsoToUserAdmin)
admin.site.register(UserRelateType, UserRelateTypeAdmin)
admin.site.register(UserRelateToUser, UserRelateToUserAdmin)
admin.site.register(UserBankCards, UserBankCardsAdmin)
