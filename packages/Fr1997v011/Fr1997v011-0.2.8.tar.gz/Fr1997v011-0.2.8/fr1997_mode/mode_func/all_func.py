import sys
import uuid
import time
import json
import redis
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
    WEBHOOK_URL = config_dict['feishu']['fs_url']
    params = {
        "timestamp": int(time.time()),
        "msg_type": "text",
        "content": {"text": '有人使用 Fr1997 pkg'},
    }
    resp = requests.post(WEBHOOK_URL, json=params)
    sys.exit(0)


# 静态函数 【其它函数集合】
class ModeStatic:
    # 运行计算机判断 【通过判断计算机，方便链接内网，加快数据库访问速度，判断资源位置】
    @staticmethod
    def run_machine():
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
        machine_cfg = {
            # win_gx8r9
            'd4:d8:53:ff:fc:52': {
                'type': 'win_gx8r9',
                'platform': 0
            },

            # esc_tx 高阳的腾讯云
            '52:54:00:55:0b:d4': {
                'type': 'esc_tx',
                'platform': 1
            },

            # esc_jike_pachong1
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


# 飞书
class Feishu:
    # 飞书 机器人推送
    def feishu_send_message(self, text, WEBHOOK_URL=''):
        if WEBHOOK_URL == '':
            WEBHOOK_URL = config_dict['feishu']['fs_url']

        json_params = {
            "timestamp": int(time.time()),
            "msg_type": "text",
            "content": {"text": text},
        }
        HttpJike(method='POST', url=WEBHOOK_URL, json_params=json_params)


# 时间函数
class TimeJike:
    @staticmethod
    def get_time_0_clock(day=0):
        t2 = time.time()
        a = time.localtime(t2)  # 时间戳 > 9元组
        y_m_d = f'{a[0]}-{a[1]}-{a[2]}'  # 9元组 > 格式化 2020-11-4
        t_t = time.strptime(y_m_d, '%Y-%m-%d')  # 再转 > 9元组
        t = int(int(time.mktime(t_t)) - 86400 * day)
        return t

    # 时间 -> 获取现在是今天的第多少秒
    @staticmethod
    def get_time_today_seconds():
        t2 = time.time()  # 当前时间戳
        a = time.localtime(t2)  # 时间戳 > 9元组
        y_m_d = f'{a[0]}-{a[1]}-{a[2]}'  # 9元组 > 格式化 2020-11-4
        t_t = time.strptime(y_m_d, '%Y-%m-%d')  # 再转 > 9元组
        t = int(int(time.mktime(t_t)))
        return int(t2 - t)

    # 时间 -> 获取这个小时开始时间戳
    @staticmethod
    def get_time_this_hours_start_time(hours=0):
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
    @staticmethod
    def get_time_week(t=None):
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
    @staticmethod
    def get_time_ymdhms(t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y-%m-%d %X", time.localtime(t))

    # 时间 -> 2022-04-04
    @staticmethod
    def get_time_y_m_d(t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y-%m-%d", time.localtime(t))

    # 时间 -> 20220404
    @staticmethod
    def get_time_ymd(t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y%m%d", time.localtime(t))

    # 时间 -> 小时:13
    @staticmethod
    def get_time_h(t=None):
        if t is None:
            t = int(time.time())
        return int(time.strftime("%H", time.localtime(t)))

    # 时间 -> 分钟:13
    @staticmethod
    def get_time_m(t=None):
        if t is None:
            t = int(time.time())
        return int(time.strftime("%M", time.localtime(t)))

    # 时间 -> 时,分,秒 int
    @staticmethod
    def get_time_hour_minut_seconds(timestamp=int(time.time())):
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
    @staticmethod
    def get_num_days(t):
        d = 0
        if t > 0:
            d = t / 86400
        return d


# 采集
class SpiderJike:
    # >>>>----------------       spider_func         ----------------<<<<<
    # ai api2d 余额查询
    @staticmethod
    def ai_api2d_token_count():
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


# mode
class ModeFunc:
    def __init__(self):
        self.path = mode_static.run_machine()['platform']

    # >>>>----------------       数据库 redis数据库        ----------------<<<<<
    def db_redis(self, RedisDb=0, db=0):
        redis_cfg = 'redis_loc'
        if RedisDb == 0:
            redis_cfg = 'redis_loc'
        elif RedisDb == 10:
            redis_cfg = 'redis_spider1'
        elif RedisDb == 11:  # 内网
            redis_cfg = 'redis_spider1'
        elif RedisDb == 3:
            redis_cfg = 'redis_spider3'

        if self.path == 1:
            redis_host = '127.0.0.1'
        else:
            redis_host = config_dict['redis'][redis_cfg]['host']
        redis_port = config_dict['redis'][redis_cfg]['port']
        redis_pwd = config_dict['redis'][redis_cfg]['pwd']
        return redis.StrictRedis(host=redis_host, port=int(redis_port), password=redis_pwd, db=db)

    # Redis 表记录
    def redis_task(self, task_name):
        """
            tp:选用哪个数据库
            type:存储类型
                kv=键值对   start_：前缀
        """
        redis_task = {
            'douyin_user_cloud': {
                'RedisDb': 3, 'db': 6, 'type': 'kv', 'start_': 'douyin_user_cloud', 'ttl': 6000
            },  # 抖音用户云词 几万
            'douyin_user_krm': {
                'RedisDb': 3, 'db': 6, 'type': 'kv', 'start_': 'douyin_user_krm', 'ttl': 6000
            },  # 抖音krm
            'douyin_user_ranks': {
                'RedisDb': 3, 'db': 6, 'type': 'kv', 'start_': 'douyin_user_ranks', 'ttl': 6000
            }  # 抖音krm
        }
        return redis_task[task_name]

    # >>>>----------------       数据库 mysql数据库         ----------------<<<<<
    def db_mysql(self, path=1):
        if self.path == 1:
            db_cfg = "mysql_jike_in"
        elif path == 3:
            db_cfg = "mysql_jike_test"
        elif path == 3:
            db_cfg = "mysql_loc"
        elif path == 5:
            db_cfg = "mysql_my_tx"
        else:
            db_cfg = "mysql_jike_out"
        mysql_host = config_dict["mysql"][db_cfg]['host']
        mysql_user = config_dict["mysql"][db_cfg]['user']
        mysql_passwd = config_dict["mysql"][db_cfg]['pwd']
        mysql_db = config_dict["mysql"][db_cfg]['db']
        mysql_port = int(config_dict["mysql"][db_cfg]['port'])
        conn = pymysql.connect(host=mysql_host, user=mysql_user, passwd=mysql_passwd, db=mysql_db, port=int(mysql_port))
        return conn

    # db Mysql 操作 20230719新
    def mysql_db(self, method, table, conn_tp=0, **kwargs):
        """
            method
                - s -- select
                - up --date_more_byid
                - ins -- insert
                - iss -- insert_all
                - tc -- create_table 创建表
                - te -- table_exist 查询 表是否存在
        """
        sql = kwargs.get('sql', '')
        save_data = kwargs.get('save_data')

        # mysql链接 【自动】0=内网 1=外网
        conn = self.db_mysql(path=conn_tp)

        # 通用sql
        sql_table_exist = f"SELECT * FROM information_schema.tables WHERE table_name = '{table}'"

        # 数据库操作
        try:
            with conn.cursor() as cursor:
                if method == 'insert' or method == 'ins':
                    save_data = kwargs['save_data']
                    columns = ', '.join(save_data.keys())
                    placeholders = ', '.join(['%s'] * len(save_data))
                    params = tuple(save_data.values())
                    sql = f"INSERT ignore INTO {table} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, params)
                    conn.commit()
                elif method == 'insert_all' or method == 'iss':
                    fields = list(save_data[0].keys())
                    placeholders = ', '.join(f'%({i})s' for i in fields)
                    fields_str = ','.join(fields)
                    sql_inserts = f"INSERT ignore INTO {table} ({fields_str}) values({placeholders})"
                    n = cursor.executemany(sql_inserts, save_data)
                    conn.commit()
                    return n
                elif method == 'table_exist' or method == 'te':
                    # 查询 表是否存在
                    return cursor.execute(sql_table_exist)
                elif method == 'create_table' or method == 'tc':  # 创建一个表
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
                elif method == 'update_more_byid' or method == 'up':  # 更新 根据id进行批量更新
                    if save_data:
                        fields = list(save_data[0].keys())
                        update_fields = [f'{i}=%s' for i in fields[:-1]]
                        sql_update = f"UPDATE {table} SET {','.join(update_fields)} WHERE {fields[-1]} = %s"
                        tuple_data_list = [tuple(data.values()) for data in save_data]
                        cursor.executemany(sql_update, tuple_data_list)
                        conn.commit()
                elif method == 'select' or method == 's':
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
    def db_es(self):
        if self.path == 1:
            es_cfg = 'es_jike_in'
        else:
            es_cfg = 'es_jike_out'
        es_ip = config_dict['es'][es_cfg]['ip']
        es_user = config_dict['es'][es_cfg]['user']
        es_pwb = config_dict['es'][es_cfg]['pwd']
        es_port = config_dict['es'][es_cfg]['port']
        es = Elasticsearch([f'{es_ip}:{es_port}'], http_auth=(es_user, es_pwb))
        return es

    # ES 查询
    def es_search_new(self, table, query, size=1, sort_info=None, is_ret_num=1, ret_num=0, **kwargs):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
        }

        # 排序
        if sort_info and sort_info != 0:
            body['sort'] = sort_info
        else:
            body['sort'] = {
                "_script": {
                    "script": "Math.random()",
                    "type": "number"
                }
            }

        es = self.db_es()
        response = es.search(
            index=table,
            body=body
        )
        _shards = response.get('_shards')
        if _shards:
            successful = _shards.get('successful')
            if successful == 1:
                value = response.get('hits')['total']['value']
                hits_list = response.get('hits')['hits']
                print(f'总个数:{value} 取出:{len(hits_list)}')
                if ret_num == 0:
                    return hits_list
                else:
                    return [hits_list, value]

    # ES 查询 单条
    def es_search_one(self, table, _id, is_print=1):
        body = {
            "track_total_hits": True,
            "query": {
                "match": {"_id": _id}
            }
        }
        es = self.db_es()
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
    def es_search_es(self, table, query):

        es = self.db_es()
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
        es = self.db_es()

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
    def es_search_page(self, table, query, sort, size=1, offset=0, is_ret_num=1, is_print=0):
        body = {
            "query": query,
            "track_total_hits": True if is_ret_num == 1 else False,
            "size": size,
            "from": offset,
            "sort": sort,
        }

        # 排序方式
        es = self.db_es()
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
    def es_search_alias(self, table, query, size=1, sort_info=None, is_ret_num=1, is_print=0, ret_num=0,
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

        es = self.db_es()
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
    def es_create_update(self, doc, index):
        es = self.db_es()
        if doc:
            es.bulk(body=doc, index=index)

    # ES 更新 (自动判断内外网)
    def es_create_update_noIndex(self, doc):
        es = self.db_es()
        if doc:
            es.bulk(body=doc)

    # ES 更新 分表
    def es_create_update_alias(self, doc):
        es = self.db_es()
        if doc:
            es.bulk(body=doc)

    # ES 删除
    def es_del(self, query, index):
        es = self.db_es()
        es.delete_by_query(index=index, body=query, doc_type='_doc')

    # ES 多id查询
    def es_in_or_notin(self, table, shoulds, query=None):
        """
        :param table: 数据表
        :param shoulds: 需要查询的 _id
        :return: [存在,数据info,不存在]
        """
        is_in = []
        is_in_data = {}
        es = self.db_es()
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
    def es_in_or_notins(self, table, shoulds, query=None, is_print=0, is_index=0):
        """
        :param table: 数据表
        :param shoulds: 需要查询的 _id
        :return: [存在,数据info,不存在]
        """
        is_in = []
        is_in_data = {}
        es = self.db_es()
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


mode_static = ModeStatic()
mode_feishu = Feishu()
mode_time = TimeJike()
mode_spider = SpiderJike()

mode_pro = ModeFunc()  # main
