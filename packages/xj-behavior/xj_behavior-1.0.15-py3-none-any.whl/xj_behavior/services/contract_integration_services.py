import sys

from orator import DatabaseManager
from decimal import Decimal
from config.config import JConfig
from xj_behavior.utils.utility_method import get_chinese_initials
from xj_finance.utils.utility_method import generate_code

config = JConfig()
db_config = {
    config.get('main', 'driver', "mysql"): {
        'driver': config.get('main', 'driver', "mysql"),
        'host': config.get('main', 'mysql_host', "127.0.0.1"),
        'database': config.get('main', 'mysql_database', ""),
        'user': config.get('main', 'mysql_user', "root"),
        'password': config.get('main', 'mysql_password', "123456"),
        "port": config.getint('main', 'mysql_port', "3306")
    }
}
db = DatabaseManager(db_config)


class ContractIntegrationServices():

    # 合同添加
    @staticmethod
    def contract_add(contract):

        contract_data = {}

        if not sys.modules.get("xj_thread.services.thread_category_service.ThreadCategoryService"):
            from xj_thread.services.thread_category_service import ThreadCategoryService
            category, category_err = ThreadCategoryService.list(params={"value": "LABOR_CONTRACT"})
            if not category['list'] and category_err:
                return None, category_err
            category_id = category['list'][0]['id']
        # ——————————————————————————————检查企业用户start———————————————————————————————————————————— #
        if not sys.modules.get("xj_user.services.user_detail_info_service.DetailInfoService"):
            from xj_user.services.user_detail_info_service import DetailInfoService
            corporate_account, err = DetailInfoService.get_detail(
                user_id=contract.get("corporate_account_id", ""))
            if err:
                return None, err
            # ——————————————————————————————检查企业用户end———————————————————————————————————————————— #

            # ——————————————————————————————检查客户start———————————————————————————————————————————— #
            user_name, err = DetailInfoService.get_detail(
                search_params={"nickname": contract.get("nickname", "")})
            if user_name:
                user_id = user_name['user_id']
            else:
                # 3、如果不存在该客户创建（不用登录的客户,不会隶属于组织结构，会绑定到企业账号旗下）
                if not sys.modules.get("xj_user.services.user_service.UserService"):
                    from xj_user.services.user_service import UserService
                    user, user_err = UserService.user_add({
                        'nickname': contract.get("nickname", ""),
                        'full_name': contract.get("nickname", ""),
                        'user_type': "UNKNOWN"
                    })
                    if user_err:
                        return None, user_err
                    user_id = user['user_id']
                # 4、第一次录入 自动绑定客户账户和企业账户隶属关系
                if not sys.modules.get("xj_user.services.user_service.UserService"):
                    from xj_user.services.user_relate_service import UserRelateToUserService
                    user_enterprise, user_enterprise_err = UserRelateToUserService.laowu_bind_bxtx_relate(
                        {"user_id_list": user_id, "with_user_id": contract.get("corporate_account_id", ""),
                         "relate_key": "belong"})
                    if user_enterprise_err:
                        return None, user_enterprise_err
            # ——————————————————————————————检查客户end———————————————————————————————————————————— #

        # ——————————————————————————————根据企业用户生成合同start———————————————————————————————————————————— #
        # 如何合同编码不存在 则为生成编码
        if not contract.get("transact_no", ""):
            initials = get_chinese_initials(corporate_account.get("nickname", ""))
            transact_no = generate_code("HL_" + str(initials))
            contract_data['transact_no'] = transact_no
        # ——————————————————————————————根据企业用户生成合同end———————————————————————————————————————————— #

        # ——————————————————————————————合同数据录入start———————————————————————————————————————————— #
        contract_data['user_id'] = user_id  # 客户id
        contract_data['with_user_id'] = contract.get("salesman_id", "")  # 业务员id
        contract_data['group_id'] = contract.get("group_id", "")  # 业务员所属大区
        contract_data['category_id'] = category_id
        # 9、查询合同是否存在 如果已经存在导入的合同隶属主合同 后续统计合同金额累加
        if not sys.modules.get("xj_thread.services.thread_item_service.ThreadItemService"):
            from xj_thread.services.thread_item_service import ThreadItemService
            thread_detail, thread_err_detail = ThreadItemService.detail(
                search_params={"transact_no": contract_data.get("transact_no", ""), "category_id": category_id},
                sort="id")
            if thread_detail:
                contract_data['main_thread_id'] = thread_detail['id']
                contract_data['is_subitem_thread'] = 1
            # 10、合同数据录入
            thread, thread_err = ThreadItemService.add(contract_data)
            if thread_err:
                return None, thread_err
            # ——————————————————————————————合同数据录入end———————————————————————————————————————————— #

        contract_id = thread.get("id")

        if contract_data.get("main_thread_id", ""):
            contract_id = contract_data.get("main_thread_id", "")

        contract_detail, contract_err = ThreadItemService.detail(contract_id)
        if contract_err:
            return None, contract_err

        return {"contract_id": contract_detail['id'], "transact_no": contract_detail['transact_no']}, None

    # 合同整合添加
    @staticmethod
    def writing(request_params):
        corporate_account_id = request_params.get("corporate_account_id", "")
        if not corporate_account_id:
            return None, "隶属企业不能为空"
        contract = request_params.get("contract", "")
        invoice = request_params.get("invoice", "")
        finance = request_params.get("finance", "")
        if contract:
            contract['corporate_account_id'] = corporate_account_id
            contract_service, contract_err = ContractIntegrationServices.contract_add(contract)
            if contract_err:
                return None, contract_err
            print("合同")

        if invoice:
            if not sys.modules.get("xj_invoice.services.invoice_service.InvoiceService"):
                from xj_invoice.services.invoice_service import InvoiceService
                for item in invoice:
                    item['thread_id'] = contract_service.get("contract_id", "")
                invoice_service, invoice_err = InvoiceService.batch_add({"invoice_list": invoice})
                if invoice_err:
                    return None, invoice_err
            print("发票")
        if finance:
            if not sys.modules.get("xj_finance.services.finance_labor_service.FinanceLaborService"):
                from xj_finance.services.finance_labor_service import FinanceLaborService
                finance['order_no'] = contract_service.get("transact_no", "")
                finance_service, finance_err = FinanceLaborService.larbor_add(finance)
                if finance_err:
                    return None, finance_err
            print("财务")

        return None, None

    # 合同加载查询
    @staticmethod
    def contract_load(request_params):
        results = db.table('thread as t') \
            .select(
            't.*',
            'u.nickname',
            'g.group_name'
        ) \
            .left_join('user_base_info as u', 't.user_id', '=', 'u.id') \
            .left_join('role_user_group as g', 't.group_id', '=', 'g.id') \
            .where_raw('t.category_id=160') \
            .group_by('transact_no')

        results_list = results.items

        return results_list, None
