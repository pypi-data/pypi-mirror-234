import sys

from orator import DatabaseManager
from decimal import Decimal
from config.config import JConfig
from xj_behavior.utils.utility_method import parse_integers

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


class CustomerStatisticsServices():
    @staticmethod
    def statistics(request_params):
        page = int(request_params.get('page', 1))
        size = int(request_params.get('size', 10))
        nickname = request_params.get('nickname', "")
        belong_id_list = request_params.get("belong_id_list", "")
        # 第一部分的子查询
        subquery_t1 = db.table('user_base_info as u') \
            .select(
            'u.id',
            'u.nickname',
            db.raw('count(t.id) as engineering_quantity'),
            db.raw('sum(t.field_1) as total_contract_amount')
        ) \
            .left_join('thread as t', 't.user_id', '=', 'u.id') \
            .where_raw('t.category_id=160') \
            .where_raw('user_type ="UNKNOWN" ') \
            .group_by('u.id')

        # 第二部分的子查询
        subquery_t2 = db.table('user_base_info as u') \
            .select(
            'u.id',
            'u.nickname',
            db.raw('sum(t.field_1) as year_total_contract_amount')
        ) \
            .left_join('thread as t', 't.user_id', '=', 'u.id') \
            .where_raw('t.category_id=160') \
            .where_raw('user_type ="UNKNOWN" ') \
            .where_raw('YEAR(t.create_time) = YEAR(CURDATE())') \
            .group_by('u.id')

        query = db.table(db.raw(f"({subquery_t1.to_sql()}) as t1")) \
            .select(
            't1.id',
            't1.nickname',
            db.raw('engineering_quantity'),
            db.raw('total_contract_amount'),
            db.raw('year_total_contract_amount')
        ) \
            .left_join(db.raw(f"({subquery_t2.to_sql()}) as t2"), 't1.id', '=', 't2.id')

        if belong_id_list:
            belong_list = parse_integers(belong_id_list)
            group_query = db.table('user_relate_to_user').select('user_id').where_in('with_user_id', belong_list).where(
                'user_relate_type_id', 5).get()
            user_ids = [item['user_id'] for item in group_query.items]

        if user_ids:
            query.where_in('user_id', user_ids)
        else:
            query.where_null('user_id')

        if nickname:
            query.where('t1.nickname', 'like', f'%{nickname}%')

        total = query.get().count()

        results = query.paginate(size, page)
        results_list = results.items

        return {'size': size, 'page': page, 'total': total, 'list': results_list}, None
