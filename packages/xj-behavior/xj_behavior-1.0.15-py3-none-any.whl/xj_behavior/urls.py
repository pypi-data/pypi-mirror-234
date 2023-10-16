# _*_coding:utf-8_*_
from django.urls import re_path

from .apis.contract_integration_apis import ContractIntegrationApis
from .apis.customer_statistics_apis import CustomerStatisticsApis
from .apis.homepage_statistics_apis import HomepageStatisticsApis
from .apis.standing_book_apis import StandingBookApis

app_name = 'xj_behavior'

# 应用路由
urlpatterns = [
    re_path(r'data?$', StandingBookApis.as_view(), ),
    re_path(r'standing_book_v2?$', StandingBookApis.standing_book_v2, ),
    re_path(r'statistics?$', HomepageStatisticsApis.statistics, ),  # 首页统计（镖镖行）
    re_path(r'invitee_export?$', HomepageStatisticsApis.invitee_export, ),  # 邀请人导出（镖镖行）
    re_path(r'customer?$', CustomerStatisticsApis.statistics, ),  # 客户列表（中迈劳务专用）
    re_path(r'contract_add?$', ContractIntegrationApis.contract_add, ),  # 合同添加（中迈劳务专用 需处理逻辑）
    re_path(r'contract_integration_entry?$', ContractIntegrationApis.writing, ),  # 合同、发票、财务整合写入（中迈劳务专用）

    re_path(r'user_detail_export?$', HomepageStatisticsApis.user_detail_export),  # 用户列表导出（镖镖行）
    re_path(r'standing_book_v2_export?$', StandingBookApis.standing_book_v2_export),  # 用户列表导出（镖镖行）
]
