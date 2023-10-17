import sys
import uuid
import time
import json
import pymysql
import requests
import memcache  # pip install python-memcached
from elasticsearch import Elasticsearch  # ES
from concurrent.futures import ThreadPoolExecutor  # 线程次

"""
    配置文件
        所有配置在这个地方读取 
        使用内存缓存机制 memcache
        没有读取到内存中的配置，这个包相当于不能用

"""
mc = memcache.Client(['127.0.0.1:11211'], debug=True)
config_dict = mc.get("my_config_dict")
if not config_dict:
    print("无法使用该包...")
    sys.exit(0)


# 静态函数
class ModeStatic:
    # 运行计算机判断 【通过判断计算机，方便链接内网，加快数据库访问速度，判断资源位置】
    @staticmethod
    def run_machine():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
        machine_cfg = {
            'd4:d8:53:ff:fc:52': {
                'type': 'win_gx8r9',
                'platform': 0
            },
            '52:54:00:55:0b:d4': {
                'type': 'esc_tx',
                'platform': 1
            },
            '52:54:00:03:18:2c': {
                'type': 'esc_jike_pachong1',
                'platform': 1
            },
        }

        if mac_address in machine_cfg:
            return machine_cfg[mac_address]
        else:
            return {'type': 'other', 'platform': 0}


# requests 封装
class HttpJike:
    def __init__(self, *args, **kwargs):
        self.method = kwargs.get("method", "GET")
        self.url = kwargs['url']
        self.json_params = kwargs.get("json_params", None)
        self.headers = kwargs.get("headers", config_dict['base_headers'])
        self.ret_data = self.req()  # 请求

    def req(self):
        try:
            self.response = requests.request(
                self.method,
                url=self.url,
                headers=self.headers,
                json=self.json_params)
            if self.response.status_code == 200:
                return self.ret()
            else:
                return self.ret(code=self.response.status_code, msg='状态码错误')
        except Exception as e:
            return self.ret(code=500, msg=str(e))

    # 返回数据
    def ret(self, code=200, msg='ok'):
        return {
            'code': code,
            'msg': msg,
        }


# mode
class ModeFunc:
    def __init__(self):
        self.path = mode_static.run_machine()['platform']

    # >>>>----------------       db_func         ----------------<<<<<
    def db_mysql(self, path=1):
        if self.path == 1:
            return self.mysql_in_conn()
        else:
            return self.mysql_conn()

    # db Mysql locale
    def loc_mysql_conn(self):
        mysql_host = config_dict['mysql_loc_host']
        mysql_user = config_dict["mysql_loc_user"]
        mysql_passwd = config_dict["mysql_loc_pwd"]
        mysql_db = config_dict["mysql_loc_db"]
        mysql_port = config_dict["mysql_loc_port"]
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, password=mysql_passwd, db=mysql_db)
        return conn

    # db Mysql develop
    def mysql_conn(self):
        mysql_host = config_dict["mysql_host"]
        mysql_user = config_dict["mysql_user"]
        mysql_passwd = config_dict["mysql_pwd"]
        mysql_db = config_dict["mysql_db"]
        mysql_port = int(config_dict["mysql_port"])
        conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, port=int(mysql_port))
        return conn

    # db Mysql online
    def mysql_in_conn(self):
        mysql_host = config_dict["mysql_host_in"]
        mysql_user = config_dict["mysql_user"]
        mysql_passwd = config_dict["mysql_pwd"]
        mysql_db = config_dict["mysql_db"]
        mysql_port = int(config_dict["mysql_port_in"])
        conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, port=int(mysql_port))
        return conn

    # db Mysql test
    def mysql_old_test_conn(self):
        mysql_test_host = config_dict["mysql_test_host"]
        mysql_test_user = config_dict["mysql_test_user"]
        mysql_test_pwd = config_dict["mysql_test_pwd"]
        mysql_test_db = config_dict["mysql_test_db"]
        mysql_test_port = config_dict["mysql_test_port"]

        conn = pymysql.connect(host=mysql_test_host, port=mysql_test_port, user=mysql_test_user,
                               password=mysql_test_pwd, db=mysql_test_db)
        return conn

    # db mysql sql
    def mysql_updates_sql(self, table_name, key):
        sql = 'UPDATE '
        sql += f'{table_name} SET '
        for i in key[:-1]:
            sql += f'{i} = (%s),'
        sql = sql[:-1]
        sql += f' WHERE {key[-1]} = (%s)'
        return sql

    # db Mysql 操作
    def mysql_mode(self, sql='', method='', conn_tp=1, fields=None, table=None, save_data=None, ignore=1, **kwargs):
        """
        :param sql:
        :param method: 查=s 新查=find 增=add 批增=add_more
        :param conn_tp:
        :param fields:
        :param table:
        :param save_data: 存储数据
        :param ignore:
        :param field: 查询字段
        :return:
        """
        mysql_field = ["where"]
        find_fields = kwargs.get('find_fields')
        choose = kwargs.get('choose')
        order = kwargs.get('order')  # +=asc -=desc rand
        limit = kwargs.get('limit')

        if conn_tp == 3:
            conn = self.mysql_old_test_conn()  # 莫凡 测试 外网
        elif conn_tp == 4:
            conn = self.loc_mysql_conn()  # 莫凡 测试 外网
        else:
            conn = self.db_mysql(path=conn_tp)  # 【自动】0=内网 1=外网

        # 批量添加
        def mysql_add_more_sql(fields, table, ignore):
            fields_1 = ','.join([f'`{i}`' for i in fields])
            fields_2 = ','.join([f'%({i})s' for i in fields])
            sql = f"insert into {table}({fields_1}) values ({fields_2})"
            if ignore:
                sql = sql[:6] + ' ignore ' + sql[7:]
            return sql

        # 字段处理
        def field_do(find_fields):
            new_field = []
            for f in find_fields:
                if f in mysql_field:
                    f = f'`{f}`'
                new_field.append(f)
            return ','.join(new_field)

        # 数据库操作
        try:
            with conn.cursor() as cursor:
                if method == 'sql':
                    cursor.execute(sql)
                    conn.commit()
                elif method == 'add_more':
                    sql = mysql_add_more_sql(fields=fields, table=table, ignore=ignore)
                    add_up = kwargs.get('add_up')
                    if add_up:
                        sql += f' on DUPLICATE key update {add_up}'
                    save_count = cursor.executemany(sql, save_data)
                    conn.commit()
                    return save_count
                elif method == 'update_more':
                    update_more_data = kwargs.get('update_more_data')
                    cursor.executemany(sql, update_more_data)
                    conn.commit()
                elif method == 'find':
                    sql_find = 'SELECT '
                    sql_find += field_do(find_fields=find_fields)
                    sql_find += ' FROM '
                    sql_find += f'`{table}`'

                    # 搜索条件
                    if choose:
                        sql_find += f' WHERE '
                        choose_all = []
                        for cs in choose:
                            cs_each = f'{cs[0]} {cs[1]} {cs[2]}'
                            choose_all.append(cs_each)
                        sql_find += ' and '.join(choose_all)

                    # 排序
                    if order:
                        if order == 'rand':
                            sql_find += f' order by rand()'
                        else:
                            if '+' in order:
                                order_rule = 'asc'
                            else:
                                order_rule = 'desc'
                            order = order.replace('+', '').replace('-', '')
                            sql_find += f' order by {order} {order_rule}'

                    # limit
                    if limit:
                        sql_find += f' limit {limit}'
                    cursor.execute(sql_find)
                    return cursor.fetchall()
                elif method == 'truncate_table':
                    truncate_table = f"truncate table {table}"
                    cursor.execute(truncate_table)
                    conn.commit()
                elif method == 'table_field':
                    describe_query = f"DESCRIBE {table}"
                    cursor.execute(describe_query)
                    columns = cursor.fetchall()
                    return [column[0] for column in columns]
                elif method == 'table_field_info':
                    describe_query = f"DESCRIBE {table}"
                    cursor.execute(describe_query)
                    columns = cursor.fetchall()
                    return columns
                elif method == 'add_field':
                    alter_query = f"ALTER TABLE {table} "
                    column_queries = []
                    field_columns = kwargs['field_columns']
                    if field_columns:
                        for column in field_columns:
                            column_query = f"ADD COLUMN {column['field']} {column['type']} DEFAULT {column['default']}"
                            column_queries.append(column_query)
                        alter_query += ", ".join(column_queries)
                        cursor.execute(alter_query)
                        conn.commit()
                else:
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            print(f"数据库链接错误:{e}")
        finally:
            conn.close()

    # db Mysql 操作 20230719新
    def mysql_mode1(self, method, table, conn_tp=0, **kwargs):
        sql = kwargs.get('sql', '')
        save_data = kwargs.get('save_data')

        if conn_tp == 3:
            conn = self.mysql_old_test_conn()  # 莫凡 测试 外网
        elif conn_tp == 4:
            conn = self.loc_mysql_conn()  # 本地
        elif conn_tp == 'tx':
            conn = pymysql.connect(host='101.35.29.36', port=3306, user='fr1997', password='914673123gao',
                                   db="tx_fr1997_db1")
        else:
            conn = self.db_mysql(path=conn_tp)  # 【自动】0=内网 1=外网

        # 通用sql
        sql_table_exist = f"SELECT * FROM information_schema.tables WHERE table_name = '{table}'"

        # 数据库操作
        try:
            with conn.cursor() as cursor:
                if method == 'insert':
                    save_data = kwargs['save_data']
                    columns = ', '.join(save_data.keys())
                    placeholders = ', '.join(['%s'] * len(save_data))
                    params = tuple(save_data.values())
                    sql = f"INSERT ignore INTO {table} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, params)
                    conn.commit()
                elif method == 'insert_all':
                    fields = list(save_data[0].keys())
                    placeholders = ', '.join(f'%({i})s' for i in fields)
                    fields_str = ','.join(fields)
                    sql_inserts = f"INSERT ignore INTO {table} ({fields_str}) values({placeholders})"
                    n = cursor.executemany(sql_inserts, save_data)
                    conn.commit()
                    return n
                elif method == 'table_exist':  # 查询 表是否存在
                    return cursor.execute(sql_table_exist)
                elif method == 'create_table':  # 创建一个表
                    table_exist = cursor.execute(sql_table_exist)
                    if table_exist:
                        print('表已经存在')
                        return '表已经存在'
                    """
                        TINYINT = [-128,127]
                        SMALLINT = [-32768,32767]
                    """
                    fields_sql = []
                    field_cfg = kwargs['field_cfg']
                    for f in field_cfg['fields']:
                        name = f['f_name']
                        field_type = f['field_type']
                        comment = f.get('comment', '待增加注释')

                        if field_type == 'VARCHAR':
                            length = f.get('length', 255)
                            default = f.get('default', '')
                            fields_sql.append(f"{name} {field_type}({length}) DEFAULT '{default}' COMMENT '{comment}'")
                        elif field_type == 'INT' or field_type == 'TINYINT' or field_type == 'SMALLINT':
                            length = f.get('length', 11)
                            default = f.get('default', 0)
                            fields_sql.append(f"{name} {field_type}({length}) DEFAULT {default} COMMENT '{comment}'")
                    if fields_sql:
                        this_time = time.strftime("%Y-%m-%d %X", time.localtime(int(time.time())))
                        table_notes = f'{this_time} 【高阳】创建此表'  # 表备注
                        sql_create_base = f"CREATE TABLE {table} ({field_cfg['id']} INT AUTO_INCREMENT PRIMARY KEY,{','.join(fields_sql)}) COMMENT='{table_notes}'"
                        cursor.execute(sql_create_base)

                        # 增加唯一索引
                        field_index = field_cfg['field_index']
                        if field_index:
                            if len(field_index) == 1:
                                sql_index = f"ALTER TABLE {table} ADD UNIQUE INDEX field_index ({field_index[0]});"
                            else:
                                sql_index = f"ALTER TABLE {table} ADD CONSTRAINT field_index UNIQUE ({','.join(field_index)});"
                            cursor.execute(sql_index)
                        print(f"创建{table}成功")
                        return f"创建{table}成功"
                elif method == 'update_more_byid':  # 更新 根据id进行批量更新
                    if save_data:
                        fields = list(save_data[0].keys())
                        update_fields = [f'{i}=%s' for i in fields[:-1]]
                        sql_update = f"UPDATE {table} SET {','.join(update_fields)} WHERE {fields[-1]} = %s"
                        tuple_data_list = [tuple(data.values()) for data in save_data]
                        cursor.executemany(sql_update, tuple_data_list)
                        conn.commit()
                elif method == 'select':
                    cursor.execute(sql)
                    return cursor.fetchall()
                else:
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            print(f"数据库链接错误:{e}")
        finally:
            conn.close()

    # >>>>----------------       数据库 es数据库        ----------------<<<<<
    def db_es(self, path=1):
        if self.path == 1:
            return self.Es_kkb_mofan()
        else:
            return self.Es_kkb_mofan_out()

    # Es 环境选择
    def path_choose(self, path=0):
        if self.path == 1 and path == 1:
            es = self.Es_kkb_mofan()
        else:
            es = self.Es_kkb_mofan_out()
        return [es]

    # db es online
    def Es_kkb_mofan(self):
        es_ip = config_dict['es_ip']
        es_user = config_dict['es_user']
        es_pwb = config_dict['es_pwb']
        es_port = config_dict['es_port']
        es = Elasticsearch([f'{es_ip}:{es_port}'], http_auth=(es_user, es_pwb))
        return es

    # db es develop
    def Es_kkb_mofan_out(self):
        es_ip = config_dict['es_ip_out']
        es_user = config_dict['es_user']
        es_pwb = config_dict['es_pwb']
        es_port = config_dict['es_port']
        es = Elasticsearch([f'{es_ip}:{es_port}'], http_auth=(es_user, es_pwb))
        return es

    # ES 查询
    def es_search(self, table, query, size=1, sort=1, sort_info=None, is_ret_num=1, is_print=0, path=1, ret_num=0):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
        }

        # 根据规则排序
        if sort_info:
            body['sort'] = sort_info
        else:
            body['sort'] = {
                "_script": {
                    "script": "Math.random()",
                    "type": "number"
                }
            }

        es = self.path_choose(path=path)[0]
        response = es.search(
            index=table,
            body=body
        )
        _shards = response.get('_shards')
        if _shards:
            successful = _shards.get('successful')
            if successful == 1:
                hits_list = response.get('hits')['hits']
                if is_print:
                    value = response.get('hits')['total']['value']
                    hits_list = response.get('hits')['hits']
                    print(f'总个数:{value} 取出:{len(hits_list)}')
                if ret_num == 0:
                    return hits_list
                else:
                    return [hits_list, value]

    # ES 查询
    def es_search_one(self, table, _id, path=1, is_print=1):
        body = {
            "track_total_hits": True,
            "query": {
                "match": {"_id": _id}
            }
        }
        es = self.path_choose(path=path)[0]
        response = es.search(
            index=table,
            body=body
        )
        hits_list = response.get('hits')['hits']
        if is_print:
            value = response.get('hits')['total']['value']
            hits_list = response.get('hits')['hits']
            print(f'总个数:{value} 取出:{len(hits_list)}')
        return hits_list

    # ES 查询 纯es
    def es_search_es(self, table, query, path=1):

        es = self.path_choose(path=path)[0]
        response = es.search(
            index=table,
            body=query
        )
        return response

    # ES 数量
    def es_count(self, table):
        try:
            body = {
                "size": 1,
                "track_total_hits": True
            }
            es = self.db_es()
            response = es.search(
                index=table,
                body=body
            )
            count = response.get('hits')['total']['value']
            return count
        except:
            return -1

    # ES 合并查询
    def es_searchs(self, queries, table):
        es = self.db_es(path=1)

        def process_query(query):
            result = es.search(index=table, body=query)
            return result

        # 创建线程池
        pool = ThreadPoolExecutor(max_workers=5)  # 根据需求设置最大工作线程数

        # 提交查询任务到线程池
        futures = [pool.submit(process_query, query) for query in queries]

        # 获取查询结果
        results = [future.result() for future in futures]

        return results

    # ES 查询 分页
    def es_search_page(self, table, query, sort, size=1, offset=0, is_ret_num=1, is_print=0, path=1):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
            "from": offset,
            "sort": sort,
        }

        # 排序方式
        es = self.path_choose(path=path)[0]
        response = es.search(
            index=table,
            body=body
        )
        _shards = response.get('_shards')
        if _shards:
            successful = _shards.get('successful')
            if successful == 1:
                hits_list = response.get('hits')['hits']
                if is_print:
                    value = response.get('hits')['total']['value']
                    hits_list = response.get('hits')['hits']
                    print(f'总个数:{value} 取出:{len(hits_list)}')
                return hits_list

    # ES 查询 多表合并查询
    def es_search_alias(self, table, query, size=1, sort_info=None, is_ret_num=1, is_print=0, path=1, ret_num=0,
                        **kwargs):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
        }

        _source = kwargs.get("_source")
        if _source is not None:
            body['_source'] = _source

        # 根据规则排序
        if sort_info:
            body['sort'] = sort_info
        else:
            body['sort'] = {
                "_script": {
                    "script": "Math.random()",
                    "type": "number"
                }
            }

        es = self.path_choose(path=path)[0]
        response = es.search(
            index=table,
            body=body
        )

        hits = response['hits']
        db_total = hits['total']['value']
        hits_list = hits['hits']
        print(f'总个数:{db_total} 取出:{len(hits_list)}')

        if ret_num == 0:
            return hits_list
        else:
            return [hits_list, db_total]

    # ES 更新
    def es_create_update(self, doc, index, path=1):
        if path == 0:
            es = self.path_choose(path=path)[0]  # 强制外网链接
        else:
            es = self.db_es()
        if doc:
            es.bulk(body=doc, index=index)

    # ES 更新 (自动判断内外网)
    def es_create_update_noIndex(self, doc, path=1):
        if path == 0:
            es = self.path_choose(path=path)[0]  # 强制外网链接
        else:
            es = self.db_es()
        if doc:
            es.bulk(body=doc)

    # ES 更新 分表
    def es_create_update_alias(self, doc, path=1):
        if path == 0:
            es = self.path_choose(path=path)[0]  # 强制外网链接
        else:
            es = self.db_es()
        if doc:
            es.bulk(body=doc)

    # ES 删除
    def es_del(self, query, index, path=1):
        es = self.path_choose(path=path)[0]
        es.delete_by_query(index=index, body=query, doc_type='_doc')

    # ES 多id查询
    def es_in_or_notin(self, table, shoulds, path=1, query=None):
        """
        :param table: 数据表
        :param shoulds: 需要查询的 _id
        :param path: 1=内网 0=外网
        :return: [存在,数据info,不存在]
        """
        is_in = []
        is_in_data = {}
        es = self.path_choose(path=path)[0]
        if shoulds:
            if query is None:
                query = {
                    "bool": {
                        "must": [
                            {"terms": {"_id": shoulds}}
                        ],
                        # "must_not": {"match": {"update_time_1": 0}}
                    }
                }
            response = es.search(
                index=table,
                body={
                    "query": query,
                    "size": 1500,  # 返回数量
                    "track_total_hits": 'true',  # 显示总量有多少条
                }
            )
            if response:
                _shards = response.get('_shards')
                if _shards:
                    successful = _shards.get('successful')
                    if successful == 1:
                        # 数据集
                        hits_list = response.get('hits')['hits']
                        print('本次取出符合条件的总数:', len(hits_list))

                        for index_x, i in enumerate(hits_list):
                            _s = i['_source']
                            _id = i['_id']
                            is_in.append(_id)
                            is_in_data[f'{_id}'] = _s

        shoulds_not = [i for i in shoulds if str(i) not in is_in]
        return is_in, is_in_data, shoulds_not

    # ES 多id查询(多表)
    def es_in_or_notins(self, table, shoulds, path=1, query=None, is_print=0, is_index=0):
        """
        :param table: 数据表
        :param shoulds: 需要查询的 _id
        :param path: 1=内网 0=外网
        :return: [存在,数据info,不存在]
        """
        is_in = []
        is_in_data = {}
        es = self.path_choose(path=path)[0]
        if shoulds:
            if query is None:
                query = {
                    "bool": {
                        "must": [
                            {"terms": {"_id": shoulds}}
                        ],
                        # "must_not": {"match": {"update_time_1": 0}}
                    }
                }
            response = es.search(
                index=table,
                body={
                    "query": query,
                    "size": 1500,  # 返回数量
                    "track_total_hits": 'true',  # 显示总量有多少条
                }
            )
            if response:
                _shards = response.get('_shards')
                if _shards:
                    successful = _shards.get('successful')
                    if successful > 0:
                        # 数据集
                        hits_list = response.get('hits')['hits']
                        if is_print:
                            print('本次取出符合条件的总数:', len(hits_list))

                        for index_x, i in enumerate(hits_list):
                            _s = i['_source']
                            _id = i['_id']
                            is_in.append(_id)
                            if is_index == 1:
                                _s['_index'] = i['_index']
                            is_in_data[f'{_id}'] = _s

        shoulds_not = [i for i in shoulds if str(i) not in is_in]
        return is_in, is_in_data, shoulds_not

    # >>>>----------------       public_func        ----------------<<<<<
    def public_func_add(self):
        return 1 + 2

    # >>>>----------------       time_func         ----------------<<<<<
    def get_time_0_clock(self, day=0):
        """
        获取几天前凌晨0点时间戳 (默认今天)
        :param time_s:几天前
        :return:
        """
        t2 = time.time()
        a = time.localtime(t2)  # 时间戳 > 9元组
        y_m_d = f'{a[0]}-{a[1]}-{a[2]}'  # 9元组 > 格式化 2020-11-4
        t_t = time.strptime(y_m_d, '%Y-%m-%d')  # 再转 > 9元组
        t = int(int(time.mktime(t_t)) - 86400 * day)
        return t

    # 时间 -> 获取现在是今天的第多少秒
    def get_time_today_seconds(self):
        t2 = time.time()  # 当前时间戳
        a = time.localtime(t2)  # 时间戳 > 9元组
        y_m_d = f'{a[0]}-{a[1]}-{a[2]}'  # 9元组 > 格式化 2020-11-4
        t_t = time.strptime(y_m_d, '%Y-%m-%d')  # 再转 > 9元组
        t = int(int(time.mktime(t_t)))
        return int(t2 - t)

    # 时间 -> 获取这个小时开始时间戳
    def get_time_this_hours_start_time(self, hours=0):
        """
        :param hours: 几个小时前
        :return: 时间戳
        """
        t2 = time.time()
        a = time.localtime(t2)  # 时间戳 > 9元组
        y_m_d = f'{a[0]}-{a[1]}-{a[2]} {a[3]}:{0}'  # 9元组 > 格式化 2020-11-4
        y_m_d_s = time.strptime(y_m_d, '%Y-%m-%d %H:%M')  # 再转 > 9元组
        t = int(time.mktime(y_m_d_s)) - hours * 3600
        return t

    # 时间 -> 返回星期几 str
    def get_time_week(self, t=None):
        """
        :param t: 时间戳 默认=今日
        :return: 周几
        """
        if t is None:
            t = int(time.time())
        t_s0 = int(time.strftime("%w", time.localtime(t)))  # 获取今天星期数
        if t_s0 == 1:
            t_s = "周一"
        elif t_s0 == 2:
            t_s = "周二"
        elif t_s0 == 3:
            t_s = "周三"
        elif t_s0 == 4:
            t_s = "周四"
        elif t_s0 == 5:
            t_s = "周五"
        elif t_s0 == 6:
            t_s = "周六"
        else:
            t_s = "周日"
        return t_s

    # 时间 -> 2022-04-04 13:59:49
    def get_time_ymdhms(self, t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y-%m-%d %X", time.localtime(t))

    # 时间 -> 2022-04-04
    def get_time_y_m_d(self, t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y-%m-%d", time.localtime(t))

    # 时间 -> 20220404
    def get_time_ymd(self, t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y%m%d", time.localtime(t))

    # 时间 -> 小时:13
    def get_time_h(self, t=None):
        if t is None:
            t = int(time.time())
        return int(time.strftime("%H", time.localtime(t)))

    # 时间 -> 小时:13
    def get_time_m(self, t=None):
        if t is None:
            t = int(time.time())
        return int(time.strftime("%M", time.localtime(t)))

    # 时间 -> 时,分,秒 int
    def get_time_hour_minut_seconds(self, timestamp=int(time.time())):
        """
        返回当前 时,分,秒 int
        :param timestamp: 时间戳
        :return: 时 分 秒
        """
        HOUR = timestamp // (60 * 60)
        MINUT = (timestamp - (HOUR * (60 * 60))) // 60
        SECONDS = timestamp - ((HOUR * (60 * 60)) + (MINUT * 60))
        return HOUR, MINUT, SECONDS

    #  时间 -> 秒返回天
    def get_num_days(self, t):
        d = 0
        if t > 0:
            d = t / 86400
        return d

    # >>>>----------------       spider_func         ----------------<<<<<
    def feishu_send_message(self, text, WEBHOOK_URL=''):
        if WEBHOOK_URL == '':
            WEBHOOK_URL = config_dict['feishu']['fs_url']

        json_params = {
            "timestamp": int(time.time()),
            "msg_type": "text",
            "content": {"text": text},
        }
        res = HttpJike(method='POST', url=WEBHOOK_URL, json_params=json_params)
        if res.ret_data['code'] == 200:
            data_data = res.response.json()
            print(data_data)

        # resp = requests.post(WEBHOOK_URL, json=params)
        # if resp.status_code == 200:
        #     result = resp.json()
        #     if result.get('StatusMessage') == 'success' and result.get('StatusCode') == 0:
        #         return '发送成功'
        #     else:
        #         return '发送失败'
        # else:
        #     return '状态码错误'

    # ai api2d 余额查询
    def ai_api2d_token_count(self):
        url = "https://oa.api2d.net/dashboard/billing/credit_grants"
        token = config_dict['api2d']['token1']
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }
        res = HttpJike(method='GET', url=url, headers=headers)

        if res.ret_data['code'] == 200:
            data_data = res.response.json()
            token_count = data_data['total_granted']
            return token_count


mode_static = ModeStatic()
mode_pro = ModeFunc()
