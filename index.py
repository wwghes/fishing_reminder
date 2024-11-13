import datetime
import requests
import json
import os
from zhdate import ZhDate as lunar_date

WEBHOOK_WEBCHAT = os.environ.get('WECHATWORK_WEBHOOK')
WEBHOOK_LANK = os.environ.get('LANK_WEBHOOK')

def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


def time_parse(today):
    # print(today.year, today.month, today.day)

    # 农历节日所在日期
    # print("大年时间: ", lunar_date(today.year+1, 1, 1).to_datetime().date())
    # print("端午时间: ", lunar_date(today.year, 5, 5).to_datetime().date())
    # print("中秋时间: ", lunar_date(today.year, 8, 15).to_datetime().date())

    # 新历节日所在日期
    # print("元旦时间: ", f"{today.year+1}-01-01")
    # print("清明时间: ", f"{today.year+1}-04-05")
    # print("劳动时间: ", f"{today.year+1}-05-01")

    # 距离除夕
    distance_new_year_eve = calculate_distance(today=today, m=12, d=29, lunar=True)
    # 距离大年
    distance_big_year = calculate_distance(today=today, m=1, d=1, lunar=True)
    # 距离元夕
    distance_1_15 = calculate_distance(today=today, m=1, d=15, lunar=True)
    # 距离端午
    distance_5_5 = calculate_distance(today=today, m=5, d=5, lunar=True)
    # 距离中元
    distance_7_15 = calculate_distance(today=today, m=7, d=15, lunar=True)
    # 距离中秋
    distance_8_15 = calculate_distance(today=today, m=8, d=15, lunar=True)
    # 距离重阳
    distance_9_9 = calculate_distance(today=today, m=9, d=9, lunar=True)

    # 距离元旦
    distance_year = calculate_distance(today=today, m='01', d='01')
    # 距离妇女
    distance_3_8 = calculate_distance(today=today, m='03', d='08')
    # 距离清明
    distance_4_5 = calculate_distance(today=today, m='04', d='05')
    # 距离劳动节
    distance_5_1 = calculate_distance(today=today, m='05', d='01')
    # 距离儿童节
    distance_6_1 = calculate_distance(today=today, m='06', d='01')
    # 距离国庆节
    distance_10_1 = calculate_distance(today=today, m='10', d='01')
    # 距离圣诞节
    distance_12_25 = calculate_distance(today=today, m='12', d='25')

    time_ = [
        {
            "v": distance_year,
            "title": "元旦节"
        },
        {
            "v": distance_new_year_eve,
            "title": "除夕夜"
        },
        {
            "v": distance_big_year,
            "title": "过春节"
        },
        {
            "v": distance_1_15,
            "title": "元夕节"
        },
        {
            "v": distance_3_8,
            "title": "富女节"
        },
        {
            "v": distance_4_5,
            "title": "清明节"
        },
        {
            "v": distance_5_1,
            "title": "劳动节"
        },
        {
            "v": distance_5_5,
            "title": "端午节"
        },
        {
            "v": distance_6_1,
            "title": "巨婴节"
        },
        {
            "v": distance_7_15,
            "title": "中元节"
        },
        {
            "v": distance_8_15,
            "title": "中秋节"
        },
        {
            "v": distance_9_9,
            "title": "重阳节"
        },
        {
            "v": distance_10_1,
            "title": "国庆节"
        },
        {
            "v": distance_12_25,
            "title": "圣诞节"
        },
    ]

    # 企业微信卡片只支持显示6个，所以只能移除距离较远的多余节日
    time_ = sorted(time_, key=lambda x: x['v'], reverse=False)
    while len(time_) > 6:
        time_.pop()

    print(time_)
    return time_


def calculate_distance(today, m, d, lunar=False):
    if lunar:
        distance = (lunar_date(today.year, m, d).to_datetime().date() -
                    today).days
        distance = distance if distance > 0 else (
            lunar_date(today.year + 1, m, d).to_datetime().date() - today).days
    else:
        distance = (datetime.datetime.strptime(f"{today.year}-{m}-{d}",
                                               "%Y-%m-%d").date() - today).days
        distance = distance if distance > 0 else (datetime.datetime.strptime(
            f"{today.year + 1}-{m}-{d}", "%Y-%m-%d").date() - today).days
    return distance


def get_one_text():
    # 文档 https://gushi.ci/ 和 https://www.jinrishici.com/

    send_url = "https://v1.jinrishici.com/all.json"
    headers = {"Content-Type": "text/plain"}
    res = requests.post(url=send_url, headers=headers, verify=False)

    return json.loads(res.text).get('content')


def send_msg_to_wechat_bot():
    today = datetime.date.today()
    week_day_ = get_week_day(today)
    time_data = time_parse(today)
    one_text = get_one_text()

    states = []
    for item in time_data:
        keyname = f"🐟距离{item['title']}"
        value = f"还有{item['v']}天"
        states.append({"keyname": keyname, "value": value})

    headers = {"Content-Type": "text/plain"}
    send_url = WEBHOOK_WEBCHAT

    send_data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type":
            "news_notice",
            "main_title": {
                "title": "浮世三千",
                "desc":
                f"今天是 {today.year}年{today.month}月{today.day}日 {week_day_}",
            },
            "card_image": {
                "url": "https://i.loli.net/2020/11/18/3zogEraBFtOm5nI.jpg",
            },
            "vertical_content_list": [{
                "title": "年年今日，灯明如昼；原火不灭，愿人依旧。",
                "desc": "\n" + one_text + "\n"
            }],
            "horizontal_content_list":
            states,
            "jump_list": [
                {
                    "type": 1,
                    "url": "https://h5.caiyunapp.com/h5",
                    "title": "🐟🐟🐟彩云天气🐟🐟🐟"
                },
            ],
            "card_action": {
                "type": 1,
                "url": "https://so.gushiwen.cn/search.aspx?value=" + one_text + "&valuej=" + one_text[0],
                "appid": "APPID",
                "pagepath": "PAGEPATH"
            }
        }
    }

    res = requests.post(url=send_url, headers=headers, json=send_data)
    print(res.text)

def send_msg_to_lank_bot():
    today = datetime.date.today()
    week_day_ = get_week_day(today)
    time_data = time_parse(today)
    one_text = get_one_text()

    states = []
    for item in time_data:
        keyname = f"🐟距离{item['title']}"
        value = f"还有{item['v']}天"
        states.append({"keyname": keyname, "value": value})

    title = "浮世三千"
    caiyunapp = "https://h5.caiyunapp.com/h5"
    helloword = "年年今日，灯明如昼；原火不灭，愿人依旧。"
    bannerImg = "img_v3_02gi_f0365316-ba7c-4617-ba52-a64be8c3fdag" # 图片 key，在飞书客户端搭建消息卡片时上传
    state = []
    for item in time_data:
        keyname = f"🐟距离{item['title']}"
        value = f"还有{item['v']}天"
        state.append({"keyname": keyname, "value": value})

    # 消息卡片方式发送，需要在飞书客户端搭建 https://open.feishu.cn/cardkit/editor?cardId=AAqC3w5HZXdoM&cardLocale=zh_cn
    send_data = {
        "msg_type": "interactive",
        "card": json.dumps({
            "type":"template",
            "data":{
                "template_id":"AAqC3w5HZXdoM",
                "template_version_name":"1.0.0",
                "template_variable": {
                    "year": today.year,
                    "month": today.month,
                    "day": today.day,
                    "week_day": week_day_,
                    "one_text": one_text,
                    "caiyunapp": caiyunapp,
                    "helloword": helloword,
                    "state":state
                }
            }
        })
    }

    headers = {"Content-Type": "application/json"}
    print(WEBHOOK_LANK)
    send_url = WEBHOOK_LANK
    res = requests.post(url=send_url, headers=headers, json=send_data)
    print(res.text)



def main_handler():
    send_msg_to_wechat_bot() # 发送到微信机器人
    send_msg_to_lank_bot() # 发送到飞书机器人
    return ("执行完成")


main_handler()
