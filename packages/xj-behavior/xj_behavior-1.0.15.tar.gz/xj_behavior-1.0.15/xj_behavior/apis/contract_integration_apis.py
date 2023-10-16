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

from ..services.contract_integration_services import ContractIntegrationServices
from ..utils.custom_response import util_response
from ..utils.custom_tool import request_params_wrapper


class ContractIntegrationApis(APIView):

    @request_params_wrapper
    def writing(self, *args, request_params, **kwargs):
        data, err = ContractIntegrationServices.writing(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def contract_add(self, *args, request_params, **kwargs):
        data, err = ContractIntegrationServices.contract_add(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @request_params_wrapper
    def contract_load(self, *args, request_params, **kwargs):
        data, err = ContractIntegrationServices.contract_load(request_params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
