import re
import sys
import uuid
import time
import json
import redis
import pymysql
import random
import hashlib
import requests
import memcache  # pip install python-memcached
from elasticsearch import Elasticsearch  # ES
from concurrent.futures import ThreadPoolExecutor  # 线程次
from pypinyin import pinyin, Style  # 汉字转拼音

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

    # 手机号判断
    @staticmethod
    def phone_num(num):
        num = str(num.strip())
        # 中国联通：130，131，132，155，156，185，186，145，176
        # 中国移动：134, 135 ,136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 178, 182, 183, 184, 187, 188
        # 中国电信：133,153,189
        pat_lt = re.compile(r'^1(3[0-2]|45|5[5-6]|8[5-6]|76)\d{8}$')
        pat_yd = re.compile(r'^1(3[4-9]|47|5[0-27-9]|8[2-47-8]|78)\d{8}$')
        pat_dx = re.compile(r'^1(33|53|89)\d{8}$')

        if pat_lt.match(num):
            return f"联通_{pat_lt.match(num).group()}"
        elif pat_yd.match(num):
            return f"移动_{pat_yd.match(num).group()}"
        elif pat_dx.match(num):
            return f"电信_{pat_dx.match(num).group()}"
        else:
            return 0

    # 文本截取手机号  --> dict
    @staticmethod
    def phone_text(text):
        # text 不需要去空白
        phone_dict = {}  # 号码 + 个数

        # 匹配出所有 以1开头 11位的数字
        pat = re.compile(r'1\d{10}')
        res = pat.findall(text)

        # 统计每个好吗 以及个数 判断是否是标准号码 以及 运营商
        for phone in res:
            if phone_dict.get(phone):
                phone_dict[phone] += 1
            else:
                phone_dict[phone] = 1
        return phone_dict

    # user_agent
    @staticmethod
    def get_user_agent(one=False):
        user_agents = config_dict['user_agents']
        if one:
            return random.choice(user_agents)
        else:
            return user_agents

    # Windows合法文件名 转为Windows合法文件名
    @staticmethod
    def title_path(title: str):
        lst = ['\r', '\n', '\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for key in lst:
            title = title.replace(key, '-')
        if len(title) > 60:
            title = title[:60]
        return title.strip()

    # md5
    @staticmethod
    def md5_base(self, text, salt=None):
        md5 = hashlib.md5()
        if salt:
            md5 = hashlib.md5(salt.encode('utf-8'))
        md5.update(text.encode('utf-8'))
        result = md5.hexdigest()
        return result

    # ua 详情
    @staticmethod
    def ua_info(ua_string):
        from user_agents import parse
        user_agent = parse(ua_string)

        if user_agent.is_pc:
            user_use = '电脑'
        elif user_agent.is_mobile:
            user_use = '手机'
        elif user_agent.is_tablet:
            user_use = '平板'
        else:
            user_use = '其他'

        return {
            'browser': user_agent.browser.family,  # 浏览器
            'user_use': user_use,
            'browser_sys': user_agent.os.family,  # 系统
            'browser_device_brand': user_agent.device.brand,  # '品牌'
            'browser_device_type': user_agent.device.model,  # 'iPhone'
            'browser_all': str(user_agent),  # "iPhone / iOS 5.1 / Mobile Safari 5.1"
        }

    # 图片转base64
    @staticmethod
    def img_md5(pic_path):
        import base64
        # 将本地图片转换为base64编码和md5值
        with open(pic_path, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
            my_md5 = hashlib.md5()
            img_data = base64.b64decode(image_base64)
            my_md5.update(img_data)
            myhash = my_md5.hexdigest()
        return image_base64, myhash

    # cookie解析
    @staticmethod
    def cookies_split(cookie_str: str) -> str:
        # 判断是否为字符串
        if not isinstance(cookie_str, str):
            raise TypeError("cookie_str must be str")

        # 拆分Set-Cookie字符串,避免错误地在expires字段的值中分割字符串。
        cookies_list = re.split(', (?=[a-zA-Z])', cookie_str)

        # 拆分每个Cookie字符串，只获取第一个分段（即key=value部分）
        cookies_list = [cookie.split(';')[0] for cookie in cookies_list]

        # 拼接所有的Cookie
        cookie_str = ";".join(cookies_list)

        return cookie_str


# requests 封装
class HttpJike(object):

    def __init__(self):
        self.status_code = 500
        self.msg = 'ok'
        self.text = None
        self.json = None
        self.ret_url = None

    # ip代理 隧道代理
    @staticmethod
    def proxies_choose(p=1, httpx=0):
        # 注意:目前只有 1,2 两个可以使用  httpx特殊请求
        if p is None:
            p = random.randint(1, 2)

        proxy = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['proxy']
        port = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['port']
        acc = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['acc']
        pwd = config_dict["proxy"]["tunnel"][f"proxy_{p}"]['pwd']

        proxies = {
            "http": f"http://{acc}:{pwd}@{proxy}:{port}/",
            "https": f"http://{acc}:{pwd}@{proxy}:{port}/"
        }
        if httpx == 1:
            proxies = {
                "http://": f"http://{acc}:{pwd}@{proxy}:{port}/",
                "https://": f"http://{acc}:{pwd}@{proxy}:{port}/"
            }
        return proxies

    # ip代理 抖查查代理
    @staticmethod
    def proxies_douchacha_ip(self, num=1):
        response = HttpJike.get(url=f'http://39.107.202.153:8088/get_short_proxy?num={num}')
        res = response.json
        return res['proxy_list']

    # 异步代理 的使用
    @staticmethod
    def aiohttp_proxy():
        ret = []
        ip_tunnel = config_dict['proxy']['tunnel']
        for i in ip_tunnel:
            ret.append({
                'proxy': ip_tunnel[i]['proxy'],
                'a': ip_tunnel[i]['acc'],
                'p': ip_tunnel[i]['pwd'],
            })
        return ret

    @staticmethod
    def get_headers(headers):
        if headers is None:
            return config_dict['base_headers']
        return headers

    @classmethod
    def get(cls, url, headers=None, proxies=None):
        req = cls()
        try:
            response = requests.get(
                url=url,
                headers=cls.get_headers(headers=headers),
                proxies=proxies
            )
            req.status_code = response.status_code
            req.ret_url = response.url
            req.text = response.text
            req.json = response.json()

            if response.status_code != 200:
                req.msg = '状态码错误'
        except Exception as e:
            req.msg = f'err {e}'
        return req

    @classmethod
    def post(cls, url, headers=None, data=None):
        req = cls()
        try:
            response = requests.post(
                url=url,
                headers=cls.get_headers(headers=headers),
                data=json.dumps(data),
            )
            req.status_code = response.status_code
            req.text = response.text
            req.json = response.json()

            if response.status_code != 200:
                req.msg = '状态码错误'
        except Exception as e:
            req.msg = f'err {e}'
        return req


# 飞书
class Feishu:
    # 飞书 机器人推送
    def feishu_send_message(self, text, WEBHOOK_URL=''):
        if WEBHOOK_URL == '':
            WEBHOOK_URL = config_dict['feishu']['fs_url']

        data = {
            "timestamp": int(time.time()),
            "msg_type": "text",
            "content": {"text": text},
        }
        res = HttpJike.post(url=WEBHOOK_URL, data=data)
        if res.status_code == 200:
            print(res.json)

    # 飞书 应用token
    def feishu_get_token(self, app_id, app_secret):
        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            post_data = {"app_id": app_id,
                         "app_secret": app_secret}
            res = HttpJike.post(url=url, data=post_data)
            if res.status_code == 200:
                tenant_access_token = res.json["tenant_access_token"]
                return tenant_access_token
        except:
            pass

    # 飞书 批量新增
    def feishu_add_more_view(self, app_token, table_id, records, tenant_access_token):
        url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_create'

        headers = {
            'Authorization': f"Bearer {tenant_access_token}",
            'Content-Type': "application/json; charset=utf-8",
        }
        data = {
            "records": records
        }
        res = HttpJike.post(url=url, headers=headers, data=data)
        if res.status_code == 200:
            data_data = res.json
            code = data_data.get('code')
            msg = data_data.get('msg')
            data = data_data.get('data')
            if code == 0 and msg == "success" and data:
                return 1


# 时间
class TimeJike:
    @staticmethod
    def zero_clock(day=0):
        t2 = time.time()
        a = time.localtime(t2)  # 时间戳 > 9元组
        y_m_d = f'{a[0]}-{a[1]}-{a[2]}'  # 9元组 > 格式化 2020-11-4
        t_t = time.strptime(y_m_d, '%Y-%m-%d')  # 再转 > 9元组
        t = int(int(time.mktime(t_t)) - 86400 * day)
        return t

    # 时间 -> 获取现在是今天的第多少秒
    @staticmethod
    def today_seconds():
        t2 = time.time()  # 当前时间戳
        a = time.localtime(t2)  # 时间戳 > 9元组
        y_m_d = f'{a[0]}-{a[1]}-{a[2]}'  # 9元组 > 格式化 2020-11-4
        t_t = time.strptime(y_m_d, '%Y-%m-%d')  # 再转 > 9元组
        t = int(int(time.mktime(t_t)))
        return int(t2 - t)

    # 时间 -> 获取这个小时开始时间戳
    @staticmethod
    def hours_start_time(hours=0):
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
    def week(t=None):
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

    # 时间 -> 20220404
    @staticmethod
    def ymd(t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y%m%d", time.localtime(t))

    # 时间 -> 2022-04-04
    @staticmethod
    def y_m_d(t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y-%m-%d", time.localtime(t))

    # 时间 -> 2022-04-04 13:59:49
    @staticmethod
    def y_m_d__h_m_s(t=None):
        if t is None:
            t = int(time.time())
        return time.strftime("%Y-%m-%d %X", time.localtime(t))

    # 时间 -> 小时:13
    @staticmethod
    def hour(t=None):
        if t is None:
            t = int(time.time())
        return int(time.strftime("%H", time.localtime(t)))

    # 时间 -> 分钟:13
    @staticmethod
    def minute(t=None):
        if t is None:
            t = int(time.time())
        return int(time.strftime("%M", time.localtime(t)))

    # 时间 -> 时,分,秒 int
    @staticmethod
    def hour_minute_seconds(timestamp=int(time.time())):
        """
        返回当前 时,分,秒 int
        :param timestamp: 时间戳
        :return: 时 分 秒
        """
        HOUR = timestamp // (60 * 60)
        MINUT = (timestamp - (HOUR * (60 * 60))) // 60
        SECONDS = timestamp - ((HOUR * (60 * 60)) + (MINUT * 60))
        return HOUR, MINUT, SECONDS


# 文本
class TextJike:
    # 清除字符串渣滓
    @staticmethod
    def word_change(xxx):
        """
        适用于mysql
        :param xxx:
        :return:
        """
        if xxx is not None:
            xxx = str(xxx)
            xxx = str(xxx).replace("'", " ")
            xxx = str(xxx).replace('"', ' ')
            xxx = str(xxx).replace('◕', ' ')
            xxx = str(xxx).replace('\\', ' ')
            xxx = str(xxx).replace('\n', ' ')
            xxx = str(xxx).replace('\r', ' ')
            xxx = str(xxx).replace('\t', ' ')
            xxx = str(xxx).replace('\f', ' ')
            xxx = str(xxx).replace('\v', ' ')
        return xxx

    # 字符串修改 --> 只要数字
    @staticmethod
    def only_number(xxx):
        try:
            if xxx:
                return int(re.sub('\D+', '', xxx))
        except:
            pass

    # 字符串修改 --> 全是数字
    @staticmethod
    def is_all_number(input_string):
        try:
            float(input_string)  # 尝试将字符串转换为浮点数
            return True  # 如果成功转换，说明字符串都是数字
        except ValueError:
            return False  # 如果转换失败，说明字符串包含非数字字符

    # 字符串修改 --> 去除数字
    @staticmethod
    def clear_number(xxx):
        try:
            if xxx:
                return int(re.sub('\d+', '', xxx))
        except:
            pass

    # 字符串修改 --> 去除html符号
    @staticmethod
    def clear_html(xxx):
        try:
            if xxx:
                return re.sub(pattern='<.+?>', repl='', string=xxx)
        except:
            pass

    # 字符串100万 --> 1000000
    @staticmethod
    def str_num_to_int(xxx):
        xxx = xxx.replace(' ', '')  # 去除空格
        if '万' in xxx:
            xxx_num = float(xxx[:-1])
            ret_xxx = xxx_num * 10000

        elif '亿' in xxx:
            xxx_num = float(xxx[:-1])
            ret_xxx = xxx_num * 100000000

        else:
            ret_xxx = xxx
        return ret_xxx


# 数据
class DataJike:
    # 列表_多个字典_排序  -----↓↓↓↓-----列表 字典 集合 -----↓↓↓↓-----
    @staticmethod
    def list_dicts_order(list_xxx, order_by, positive_or_negative=True):
        if list_xxx:
            return sorted(list_xxx, key=lambda x: x[order_by], reverse=positive_or_negative)

    # 列表 -> 变字典 自动计算 排序
    @staticmethod
    def dicts_order_auto(list_xxx, order_by=True):
        if list_xxx:
            ret_dict = {}
            for i in list_xxx:
                if i in ret_dict:
                    ret_dict[i] += 1
                else:
                    ret_dict[i] = 1
            lis = sorted(ret_dict.items(), key=lambda i: i[1], reverse=order_by)
            return lis

    # 两个列表操作 差集
    @staticmethod
    def diff(l1, l2):
        return list(set(l1).difference(set(l2)))

    # 平均分块
    @staticmethod
    def list_avg_split(list_data, each_num):
        all_list = []
        for i in range(0, len(list_data), each_num):
            all_list.append(list_data[i:i + each_num])
        return all_list

    # 字典合并
    @staticmethod
    def dict_marge(*dicts):
        result = {}
        for d in dicts:
            result.update(d)
        return result

    # 简单字典 返回最大键  {1: 82.0, 2: 18.0} --> max:1
    @staticmethod
    def dict_max(dict_data):
        result_max = max(dict_data, key=lambda x: dict_data[x])
        return result_max

    # 列表_求平均值
    @staticmethod
    def list_avg(list_data):
        if len(list_data) < 1:
            return None
        else:
            return int(sum(list_data) / len(list_data))

    # 列表 去除指定元素
    @staticmethod
    def list_remove_by(list_old, removes=None):
        new_list = []
        if list_old and removes and type(removes) == list:
            removes = list(set(removes))  # 去重
            for i in list_old:
                if i not in removes:
                    new_list.append(i)
        return new_list


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
        res = HttpJike.get(url=url, headers=headers)
        if res.status_code == 200:
            data_data = res.json
            token_count = data_data['total_granted']
            return token_count

    # 百度IP定位
    @staticmethod
    def api_baidu_ip(ip='60.12.139.18'):
        """
        http://api.map.baidu.com/location/ip?ak=您的AK&ip=您的IP&coor=bd09ll //HTTP协议
        https://api.map.baidu.com/location/ip?ak=您的AK&ip=您的IP&coor=bd09ll //HTTPS协议

        --参数
        ak    密钥   string    必填    E4jYvwZbl9slCjUALZpnl1xawvoIAlrP
        ip          string    可选
        sn    校验   string    可选
        coor  详细请求  string  可选
        -coor不出现、或为空：百度墨卡托坐标，即百度米制坐标
        -coor = bd09ll：百度经纬度坐标，在国测局坐标基础之上二次加密而来
        -coor = gcj02：国测局02坐标，在原始GPS坐标基础上，按照国家测绘行业统一要求，加密后的坐标
        """
        city = '北京'
        province = '北京'

        try:
            ak = 'E4jYvwZbl9slCjUALZpnl1xawvoIAlrP'
            url = f'http://api.map.baidu.com/location/ip?ak={ak}&ip={ip}&coor=bd09ll'
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)'
            }
            response = HttpJike.get(url=url, headers=headers)
            if response.status_code == 200:
                data_data = response.json
                content = data_data.get('content')
                status = data_data.get('status')
                if content is not None and status == 0:
                    address_detail = content.get('address_detail')
                    if address_detail is not None:
                        city_data = address_detail.get('city')
                        province_data = address_detail.get('province')

                        # 省会 城市 判断
                        if len(province_data) > 0:
                            province = province_data
                            if len(city_data) > 0:
                                city = city_data
                            else:
                                city = province
                        else:
                            pass
                        print(f'省会:{province},城市:{city}')
                        return data_data
                    else:
                        pass
                else:
                    pass
            else:
                pass
        except:
            pass
        return [province, city]

    # 和风天气
    @staticmethod
    def api_qweather(location):
        key = 'fd9e6c4c11254fe19f2b4f46c3653397'
        url = f'https://geoapi.qweather.com/v2/city/lookup?&location={location}&key={key}'
        response = HttpJike.get(url=url)
        if response.status_code == 200:
            j = response.json
            id = j['location'][0]['id']

            # 二,根据城市id 获取城市天气
            url = f'https://devapi.qweather.com/v7/weather/now?location={id}&key={key}'
            headers = {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
            }
            response = HttpJike.get(url=url)
            if response.status_code == 200:
                weather_now = response.json
                t_s = time.strftime("%X", time.localtime(time.time()))

                location = f'{location}'
                t_s = f'{t_s}'
                temp = f"{weather_now['now']['temp']}℃"  # 当前温度
                feelsLike = f"{weather_now['now']['feelsLike']}℃"  # 体感温度
                text_now = f"{weather_now['now']['text']}"  # 当前天气
                feng = f"{weather_now['now']['windDir']}{weather_now['now']['windScale']}级 {weather_now['now']['windSpeed']}公里/小时"  # 风
                humidity = f"{weather_now['now']['humidity']}%"  # 湿度
                precip = f"{weather_now['now']['precip']}毫米"  # 降水量值
                pressure = f"{weather_now['now']['pressure']}百帕"  # 大气压强
                vis = f"{weather_now['now']['vis']}公里"  # 能见度值
                cloud = f"{weather_now['now']['cloud']}%"  # 当前云量
                return {'location': location,
                        't_s': t_s,
                        'temp': temp,
                        'feelsLike': feelsLike,
                        'text_now': text_now,
                        'feng': feng,
                        'humidity': humidity,
                        'precip': precip,
                        'pressure': pressure,
                        'vis': vis,
                        'cloud': cloud,
                        }

    # 发送QQ邮件
    @staticmethod
    def send_email(title, text):
        """
        pip install PyEmail
        pip install email
        pip install smtplib
        """

        # 发送邮件配置
        import smtplib
        from email.mime.text import MIMEText
        # email 用于构建邮件内容
        from email.header import Header

        from_addr = '1079146598@qq.com'  # 发信方邮箱
        password = 'ouacnpxmtbavjecc'  # 收信方授权码
        to_addr = '3084447185@qq.com'  # 收信方邮箱
        # to_addr = '1048995287@qq.com'  # 王伟南

        smtp_server = 'smtp.qq.com'  # 发信服务器

        # ，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(text, 'plain', 'utf-8')  # 正文内容

        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(title)

        server = smtplib.SMTP_SSL(host=smtp_server)  # 开启发信服务
        server.connect(smtp_server, 465)  # 加密传输

        server.login(from_addr, password)  # 登录发信邮箱
        server.sendmail(from_addr, to_addr, msg.as_string())  # 发送邮件
        server.quit()  # 关闭服务器

    # fr1997 web 请求ip
    @staticmethod
    def api_fr1997_ip():
        url = 'https://dv.fr1997.cn/test_ip'
        res = HttpJike.get(url=url, proxies=HttpJike.proxies_choose(1))
        if res.status_code == 200:
            return res.json['test_ip']


# 抖音
class DouyinJike:
    # 抖音视频id短链
    def short_url(self, url):
        return HttpJike.get(url=url).ret_url

    # 抖音 链接 > video_id
    def get_video_id(self, video_url, tp=1):
        # 最终 https://www.douy...in.com/video/7218785833724185917
        if '://v.douyin' in video_url:
            pat = re.compile(r'https://v.douyin.com/[-_a-zA-Z0-9]{5,10}/')
            res = pat.findall(video_url)
            if res:
                v_url = self.get_video_id(self.short_url(res[0]))
                return v_url
        if 'www.douyin.com' in video_url and 'modal_id' in video_url:
            url1 = video_url.split('modal_id=')
            if url1:
                url2 = url1[-1]
                video_ids = []
                for i in url2:
                    if i in '1234567890':
                        video_ids.append(i)
                    else:
                        break
                video_id = ''.join(video_ids)
                return video_id
        if '.douyin.com/video' in video_url:
            video_idstr1 = video_url.split('/')
            if len(video_url) >= 5:
                video_idstr2 = video_idstr1[4]
                # 去除末尾杂项
                video_ids = []
                for i in video_idstr2:
                    if i in '1234567890':
                        video_ids.append(i)
                    else:
                        break
                video_id = ''.join(video_ids)
                return video_id
        if '/www.douyin.com/user/' in video_url and 'modal_id' in video_url:  # 其他
            video_idstr1 = video_url.split('modal_id=')[-1]
            video_ids = []
            for i in video_idstr1:
                if i in '1234567890':
                    video_ids.append(i)
                else:
                    break
            video_id = ''.join(video_ids)
            return video_id
        if 'www.iesdouyin.com/share/video/' in video_url:
            video_id = video_url.split('www.iesdouyin.com/share/video/')[-1].split('/?')[0]
            return video_id

        # 强制识别 可能出现问题(强制识别 视频id为19位数字)
        pat = re.compile(r'\d{19}')
        res = pat.findall(video_url)
        if res:
            return res[0]

    # 抖音 链接 > sec_uid
    def get_douyin_sec_uid(self, user_url, tp=1):  # https://v.douyin.com/i3TDetD
        try:
            if 'www.douyin.com' in user_url and 'MS4' in user_url:
                sec_uid = user_url.split('https://www.douyin.com/user/')[-1].split('?')[0]
                return sec_uid

            if '://v.douyin.com':
                url_pattern = r'https://v\.douyin\.com/\w+/'
                matches = re.findall(url_pattern, user_url)
                if matches:
                    user_url = matches[0]
                res = HttpJike.get(url=user_url).ret_url
                sec_uid = res.split('https://www.iesdouyin.com/share/user/')[-1].split('?')[0]
                return sec_uid
        except:
            pass


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
    @staticmethod
    def redis_task(task_name):
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
    def es_search_merge(self, queries, table):
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

    # 分词 老版本
    @staticmethod
    def word_split_old(self, txt, num=100, clear_myself="???"):
        import jieba

        try:
            num = int(num)
        except:
            num = 100

        # 文本过滤 [去空格 去数字]
        txt = str(txt).replace('\n', '').replace('\r', '').replace('\\', '')
        txt = str(txt).replace(' ', '')
        txt = str(txt).replace("'", " ").replace('"', ' ').replace('◕', ' ').replace(':', ' ').replace('：', ' ')
        words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
        counts = {}  # 通过键值对的形式存储词语及其出现的次数

        # 单个词语不计算在内
        for word in words:
            if word != clear_myself:
                if len(word) == 1:
                    continue
                else:
                    counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

        # 根据词语出现的次数进行从大到小排序
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)
        if num > len(items):
            num = len(items)

        # 分级选择
        data_list = []
        for i in range(num):
            data_dict = {}
            word, count = items[i]
            data_dict['word'] = word
            data_dict['count'] = count
            if count >= 100:
                data_dict['category'] = '100'
            elif count >= 50:
                data_dict['category'] = '50'
            elif count >= 10:
                data_dict['category'] = '10'
            elif count >= 7:
                data_dict['category'] = '7'
            elif count >= 4:
                data_dict['category'] = '4'
            else:
                data_dict['category'] = '1'
            data_list.append(data_dict)
            # print("{0:<5}{1:>5}".format(word, count))
        return data_list

    # 汉字 => 拼音
    def chinese_to_pinyin(self, chinese="你好", ret=1):
        """
            ret = 1  -->  [['ni3'], ['hao3']]
            ret = 2  -->  nh
            ret = 3  -->  n

            英文的全部转换为小写

            更多复杂判断 都在这里写
                符号开头的返回 ”other“
                数字开头的返回 ”number“
        """
        try:
            chinese = chinese.lower()
            if chinese:
                # 将中文转换为拼音，设置输出格式为带声调的拼音
                pinyin_list = pinyin(chinese, style=Style.TONE3)

                # 提取每个拼音的第一个字母
                first_letters = [p[0][0] for p in pinyin_list]

                # 将字母列表连接成字符串
                first_letters_string = ''.join(first_letters)
                if ret == 2:
                    return first_letters_string
                elif ret == 3:
                    first_word = first_letters_string[:1]
                    if first_word in config_dict['numbers'] or first_word in config_dict['numbers_str']:  # 数字开头
                        return "number"
                    elif first_word == ' ':
                        return "empty"
                    elif first_word not in config_dict['low_word']:  # 符号开头
                        return "other"
                    else:
                        return first_letters_string[:1]
                else:
                    return pinyin_list
            else:
                return "empty"
        except:
            return "other"


mode_feishu = Feishu()  # 飞书app api
mode_time = TimeJike()  # 时间处理
mode_text = TextJike()  # 文本处理
mode_data = DataJike()  # 数据处理
mode_spider = SpiderJike()  # 数据请求
mode_static = ModeStatic()  # 其它函数

mode_pro = ModeFunc()  # main
