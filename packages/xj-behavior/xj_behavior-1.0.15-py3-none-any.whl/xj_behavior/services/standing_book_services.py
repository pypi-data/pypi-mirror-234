# encoding: utf-8
'''
@project: djangoModel->StandingBookServices
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 台账服务
@created_time: 2023/3/24 10:07
'''
import datetime

from orator import DatabaseManager

from config.config import JConfig
from xj_enroll.api.enroll_apis import EnrollAPI
from xj_enroll.service.enroll_record_serivce import EnrollRecordServices
from xj_finance.services.finance_transacts_service import FinanceTransactsService
from xj_role.services.user_group_service import UserGroupService
from xj_user.services.user_relate_service import UserRelateToUserService
from ..utils.custom_tool import force_transform_type
from ..utils.execl import ExcelGenerator
from ..utils.join_list import JoinList

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


class StandingBookServices():
    @staticmethod
    def standing_book(params: dict = None):
        """
        请求参数：params
        :param params: 筛选参数
        :return: list,err
        """
        page = int(params.get("page", 1))
        size = int(params.get("size", 10))

        enroll_result, err = EnrollAPI.list_handle(request_params=params)
        enroll_list = enroll_result['list']
        # print(enroll_list)
        user_id_list = list(set([i['user_id'] for i in enroll_list]))
        enroll_id_list = list(set([i['id'] for i in enroll_list]))
        # 权限模块获取部门
        group_names, err = UserGroupService.get_user_group_info(user_id_list=user_id_list,
                                                                field_list=['group_name', 'user_id'])
        # 获取业务人员
        beneficiary_users, err = UserRelateToUserService.list(
            params={'relate_key': 'beneficiary', "user_id_list": user_id_list, 'need_pagination': 0})
        beneficiary_user_map = {i["user_id"]: i["with_user_name"] for i in beneficiary_users or []}
        # 获取接单人员
        enroll_record_list, err = EnrollRecordServices.record_list(
            params={"enroll_id_list": enroll_id_list},
            need_pagination=False
        )
        enroll_record_map = {}
        for i in enroll_record_list:
            if enroll_record_map.get(i["enroll"]):
                enroll_record_map[i["enroll"]].append(i.get("full_name", "该用户不存在"))
            else:
                enroll_record_map[i["enroll"]] = [i.get("full_name", "该用户不存在")]

        current_index = (page - 1) * size
        # 获取发票相关的信息
        for item in enroll_list:
            # 添加
            group_names_str = ""
            for i in group_names.get(item.get("user_id", ""), []):
                group_names_str = group_names_str + ("," if len(group_names_str) > 0 else "") + i["group_name"]
            item["group_name"] = "游客" if not group_names_str else group_names_str  # 分组字符串

            current_index += 1
            item["index"] = current_index  # 序号
            item["beneficiary"] = beneficiary_user_map.get(item.get("user_id"), "非业务人员邀请用户")  # 邀请用户
            item["total"] = item.get("count", 0) * item.get("price", 0)  # 小计
            item["beneficiary_amount"] = float(item.get("amount", 0)) * 0.6  # 业务员提成
            item["urge_free"] = 50 if isinstance(item.get("is_urgent", None), str) and int(
                item["is_urgent"]) else 0  # 加急费用
            item["other_money"] = '-'  # 其他款项

            enroll_user_name_str = ""
            for i in enroll_record_map.get(item["id"], []):
                enroll_user_name_str = enroll_user_name_str + ("," if len(enroll_user_name_str) > 0 else "") + (i or "")
            item["enroll_user_names"] = enroll_user_name_str  # 报名名称

        enroll_result['list'] = enroll_list
        # 资金相关的数据
        finance_list, err = FinanceTransactsService.finance_standing_book(params={"enroll_id_list": enroll_id_list})
        JoinList.left_join(l_list=enroll_result['list'], r_list=finance_list, l_key="id", r_key="enroll_id")

        return enroll_result, None

    @staticmethod
    def __get_beneficiary_level(user_id, invite_relate_type_id):
        invite_user_map = {}
        first_invite_user = db.table("user_relate_to_user"). \
            where("user_relate_to_user.user_id", '=', user_id). \
            where("user_relate_type_id", invite_relate_type_id). \
            pluck('with_user_id')
        if first_invite_user:
            invite_user_map[first_invite_user] = 1

        second_invite_user = None
        if first_invite_user:
            second_invite_user = db.table("user_relate_to_user"). \
                where("user_relate_to_user.user_id", first_invite_user). \
                where("user_relate_type_id", invite_relate_type_id). \
                pluck('with_user_id')
            if second_invite_user:
                invite_user_map[second_invite_user] = 2

        if second_invite_user:
            third_invite_user = db.table("user_relate_to_user"). \
                where("user_relate_to_user.user_id", second_invite_user). \
                where("user_relate_type_id", invite_relate_type_id). \
                pluck('with_user_id')
            if third_invite_user:
                invite_user_map[third_invite_user] = 3

        return invite_user_map

    @staticmethod
    def standing_book_v2(params: dict):
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        # 获取项目信息
        enroll_result, err = EnrollAPI.list_handle(request_params=params)
        enroll_list = enroll_result['list']

        # 获取业务员相关信息
        enroll_to_user_map = {i["id"]: i["user_id"] for i in enroll_list}
        invite_relate_type_id = db.table("user_relate_type").where("relate_key", "invite").pluck('id')
        beneficiary_relate_type_id = db.table("user_relate_type").where("relate_key", "beneficiary").pluck('id')
        # ------------------------------- section 找到这一批人的业务人员的相关信息 start -------------------------------------------
        # 第一步、获取客户绑定的业务人员列表，找到了业务人员
        beneficiary_user_set = db.table("user_relate_to_user").select(
            'user_relate_to_user.user_id',
            'user_relate_to_user.with_user_id',
            "user_base_info.user_name",
            "user_base_info.full_name",
            "user_detail_info.real_name"
        ). \
            left_join("user_base_info", 'user_relate_to_user.with_user_id', '=', 'user_base_info.id'). \
            left_join("user_detail_info", 'user_relate_to_user.with_user_id', '=', 'user_detail_info.user_id'). \
            where_in("user_relate_to_user.user_id", list(set(enroll_to_user_map.values()))). \
            where("user_relate_type_id", beneficiary_relate_type_id). \
            get()
        beneficiary_id_map = {i["user_id"]: i["with_user_id"] for i in beneficiary_user_set}
        beneficiary_real_name_map = {i["user_id"]: i["real_name"] for i in beneficiary_user_set}

        # 第二步、获取业务的所属部门，找到了业务人员的所属部门
        group_user_set = db.table("role_user_to_group").select(
            'role_user_to_group.user_id',
            'role_user_to_group.user_group_id',
            "role_user_group.group_name",
            "role_user_group.group"
        ). \
            left_join("role_user_group", 'role_user_group.id', '=', 'role_user_to_group.user_group_id'). \
            where_in("role_user_to_group.user_id", list(set([i["with_user_id"] for i in beneficiary_user_set]))). \
            get()
        group_user_map = {}
        for i in group_user_set:
            if group_user_map.get(i["user_id"]):
                group_user_map[i["user_id"]].append(i)
            else:
                group_user_map[i["user_id"]] = [i]

        # 第四步、获取资金相关的信息
        bid_user_pay_map = db.table("finance_transact"). \
            where("income", '>', 0). \
            where_in("enroll_id", list(enroll_to_user_map.keys())).lists('bookkeeping_type', 'enroll_id')

        # 第五步、拼接业务信息
        for i in enroll_result['list']:
            i["beneficiary"] = beneficiary_real_name_map.get(i['user_id'], "--")  # 业务员
            beneficiary_id = beneficiary_id_map.get(i['user_id'], 0)  # 业务员的用户ID
            i["beneficiary_group_name"] = group_user_map.get(beneficiary_id, [])  # 业务人员所属部门
            i["beneficiary_percentage"] = 0  # 业务员提成默认值
            # 获取该用户前三及的邀请人，判断他的业务员是第几级
            invite_relate_level_map = StandingBookServices.__get_beneficiary_level(
                user_id=i["user_id"],
                invite_relate_type_id=invite_relate_type_id
            )
            if beneficiary_id and invite_relate_level_map.get(beneficiary_id) == 1:
                i["beneficiary_percentage"] = float(i["amount"] or 0) * 0.06
            elif beneficiary_id and invite_relate_level_map.get(beneficiary_id) == 2:
                i["beneficiary_percentage"] = float(i["amount"] or 0) * 0.04
            elif beneficiary_id and invite_relate_level_map.get(beneficiary_id) == 3:
                i["beneficiary_percentage"] = float(i["amount"] or 0) * 0.02
            i["beneficiary_percentage"] = round(i["beneficiary_percentage"], 2)

            i["bookkeeping_type"] = bid_user_pay_map.get(i['id'], "-")
        # ------------------------------- section 找到这一批人的业务人员的相关信息 end   -------------------------------------------

        # ------------------------------- section 获取开票信息 start -------------------------------------------
        # 第一步、查询
        # DATE_FORMAT(invoice_time, "%%Y-%%m-%%d %%H:%%i:%%s") as invoice_time,
        invoice_set_list = db.table("invoice_to_enroll"). \
            left_join('invoice_invoice', 'invoice_invoice.id', '=', 'invoice_to_enroll.invoice_id'). \
            left_join('thread', 'thread.id', '=', 'invoice_invoice.thread_id'). \
            select(
            db.raw("""
                enroll_id, 
                thread_id, 
                title,
                DATE_FORMAT(invoice_time, "%%Y-%%m-%%d %%H:%%i:%%s") as invoice_time,
                invoice_type_id, 
                invoice_number, 
                invoice_price, 
                tax_rate, 
                invoice_tax, 
                invoice_status
            """)). \
            where_in('enroll_id', list(set(enroll_to_user_map.keys()))). \
            get()

        # 第二步、拼接数据
        invoice_set_map = {i["enroll_id"]: i for i in invoice_set_list}
        for i in enroll_result['list']:
            i["invoice_title"] = invoice_set_map.get(i["id"], {}).get("title")
            i["invoice_time"] = invoice_set_map.get(i["id"], {}).get("invoice_time")
            i["invoice_type_id"] = invoice_set_map.get(i["id"], {}).get("invoice_type_id")
            i["invoice_number"] = invoice_set_map.get(i["id"], {}).get("invoice_number")
            i["invoice_price"] = invoice_set_map.get(i["id"], {}).get("invoice_price")
            i["tax_rate"] = invoice_set_map.get(i["id"], {}).get("tax_rate")
            i["invoice_tax"] = invoice_set_map.get(i["id"], {}).get("invoice_tax")
            i["invoice_status"] = invoice_set_map.get(i["id"], {}).get("invoice_status")
        # ------------------------------- section 获取开票信息 end   -------------------------------------------

        # ------------------------------- section 获取镖师信息 start -------------------------------------------
        # 获取报名记录相关的信息
        enroll_record_user = db.table("enroll_record"). \
            left_join("user_base_info", "user_base_info.id", '=', 'enroll_record.user_id'). \
            left_join("user_detail_info", "user_detail_info.user_id", '=', 'enroll_record.user_id'). \
            select_raw("""
                enroll_record.enroll_id,
                enroll_record.user_id,
                enroll_record.again_price,
                user_base_info.nickname as record_nickname,
                user_base_info.full_name as record_full_name,
                user_detail_info.real_name as record_real_name
            """). \
            where_in("enroll_record.enroll_id", list(enroll_to_user_map.keys())). \
            where_not_in("enroll_record.enroll_status_code", [124, 234]). \
            get()
        enroll_record_user_map = {i["enroll_id"]: i for i in enroll_record_user}

        # 获取资金相关的信息,286 为平台用户
        bid_worker_pay_record = db.table("finance_transact"). \
            select('transact_time', 'enroll_id', 'account_id', 'income', 'outgo', 'pay_mode_id', 'bookkeeping_type'). \
            where("account_id", '=', 286). \
            where("income", '=', 0). \
            where_in("enroll_id", list(enroll_record_user_map.keys())).get()
        bid_worker_pay_record_map = {i["enroll_id"]: i for i in bid_worker_pay_record}
        # 拼接数据
        for i in enroll_result['list']:
            i["again_price"] = enroll_record_user_map.get(i["id"], {}).get("again_price")
            i["record_nickname"] = enroll_record_user_map.get(i["id"], {}).get("record_nickname")
            i["record_full_name"] = enroll_record_user_map.get(i["id"], {}).get("record_full_name")
            i["record_real_name"] = enroll_record_user_map.get(i["id"], {}).get("record_real_name")
            # 资金余额相关的逻辑
            i["pay_mode_id"] = bid_worker_pay_record_map.get(i["id"], {}).get("pay_mode_id")
            i["record_transact_time"] = bid_worker_pay_record_map.get(i["id"], {}).get("transact_time")
            i["record_outgo"] = bid_worker_pay_record_map.get(i["id"], {}).get("outgo")
            i["record_bookkeeping_type"] = bid_worker_pay_record_map.get(i["id"], {}).get("bookkeeping_type",
                                                                                          '-')  # 镖师佣金的线上和线下支付
        # ------------------------------- section 获取镖师信息 end   -------------------------------------------

        return enroll_result, None

    @staticmethod
    def standing_book_v2_export(params: dict):
        params, err = force_transform_type(variable=params, var_type="dict", default={})
        # 获取项目信息
        params = {
            "page": 1,
            "size": 100000,
            **params
        }
        enroll_result, err = StandingBookServices.standing_book_v2(params)
        data = enroll_result["list"]
        header = {
            "beneficiary": "业务员",
            # "": "所属部门",
            "region_code": "归属地区",
            # "": "合同编号",
            "real_name": "客户名称",
            "title": "项目名称",
            "create_time": "业务时间",
            "amount": "应收合计",
            # "": "收款方式",
            "paid_amount": "收款金额",
            "spend_time": "收款时间",
            "invoice_time": "开票时间",
            "invoice_type_id": "专/普票",
            "invoice_number": "发票号码",
            "invoice_price": "开票金额",
            # "": "金额(不含税)",
            "invoice_tax": "税额",
            "tax_rate": "税率",
            "invoice_title": "发票抬头",
            "record_real_name": "接单镖师",
            "again_price": "镖师佣金",
            "bookkeeping_type": "付款方式",
            "record_transact_time": "付款时间",
            "record_outgo": "付款金额",
            "beneficiary_percentage": "业务提成",
            # "record_transact_time": "验收时间",
        }
        excel_generator = ExcelGenerator(data, header)
        now = datetime.datetime.now()  # 获取当前日期和时间
        timestamp = now.strftime("%Y%m%d%H%M%S")  # 格式化日期和时间
        filename = f"业务台账_{timestamp}.xlsx"
        path = excel_generator.generate_excel_response(filename)
        return path, None
