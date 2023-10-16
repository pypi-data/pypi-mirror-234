# encoding: utf-8
"""
@project: djangoModel->standing_book_apis
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2023/3/24 9:47
"""
import time

from rest_framework.views import APIView

from ..services.customer_statistics_services import CustomerStatisticsServices
from ..services.standing_book_services import StandingBookServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class CustomerStatisticsApis(APIView):
    @request_params_wrapper
    def statistics(self, *args, request_params, **kwargs):
        data, err = CustomerStatisticsServices.statistics(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
