import datetime
import requests
import json
import os
from zhdate import ZhDate as lunar_date

WEBHOOK = os.environ.get('WECHATWORK_WEBHOOK')


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

    # 距离大年
    distance_big_year = (lunar_date(today.year, 1, 1).to_datetime().date() -
                         today).days
    distance_big_year = distance_big_year if distance_big_year > 0 else (
        lunar_date(today.year + 1, 1, 1).to_datetime().date() - today).days
    # 距离元宵
    distance_1_15 = (lunar_date(today.year, 1, 15).to_datetime().date() -
                     today).days
    distance_1_15 = distance_1_15 if distance_1_15 > 0 else (
        lunar_date(today.year + 1, 1, 15).to_datetime().date() - today).days
    # 距离端午
    distance_5_5 = (lunar_date(today.year, 5, 5).to_datetime().date() -
                    today).days
    distance_5_5 = distance_5_5 if distance_5_5 > 0 else (
        lunar_date(today.year + 1, 5, 5).to_datetime().date() - today).days
    # 距离中秋
    distance_8_15 = (lunar_date(today.year, 8, 15).to_datetime().date() -
                     today).days
    distance_8_15 = distance_8_15 if distance_8_15 > 0 else (
        lunar_date(today.year + 1, 8, 15).to_datetime().date() - today).days
    # 距离重阳
    distance_9_9 = (lunar_date(today.year, 9, 9).to_datetime().date() -
                    today).days
    distance_9_9 = distance_9_9 if distance_9_9 > 0 else (
        lunar_date(today.year + 1, 9, 9).to_datetime().date() - today).days

    # 距离元旦
    distance_year = (
        datetime.datetime.strptime(f"{today.year}-01-01", "%Y-%m-%d").date() -
        today).days
    distance_year = distance_year if distance_year > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-01-01",
                                   "%Y-%m-%d").date() - today).days
    # 距离妇女
    distance_3_8 = (
        datetime.datetime.strptime(f"{today.year}-03-08", "%Y-%m-%d").date() -
        today).days
    distance_3_8 = distance_3_8 if distance_3_8 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-03-08",
                                   "%Y-%m-%d").date() - today).days
    # 距离清明
    distance_4_5 = (
        datetime.datetime.strptime(f"{today.year}-04-05", "%Y-%m-%d").date() -
        today).days
    distance_4_5 = distance_4_5 if distance_4_5 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-04-05",
                                   "%Y-%m-%d").date() - today).days
    # 距离劳动节
    distance_5_1 = (
        datetime.datetime.strptime(f"{today.year}-05-01", "%Y-%m-%d").date() -
        today).days
    distance_5_1 = distance_5_1 if distance_5_1 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-05-01",
                                   "%Y-%m-%d").date() - today).days
    # 距离劳动节
    distance_6_1 = (
        datetime.datetime.strptime(f"{today.year}-06-01", "%Y-%m-%d").date() -
        today).days
    distance_6_1 = distance_6_1 if distance_6_1 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-06-01",
                                   "%Y-%m-%d").date() - today).days
    # 距离国庆节
    distance_10_1 = (
        datetime.datetime.strptime(f"{today.year}-10-01", "%Y-%m-%d").date() -
        today).days
    distance_10_1 = distance_10_1 if distance_10_1 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-10-01",
                                   "%Y-%m-%d").date() - today).days
    # 距离圣诞节
    distance_12_25 = (
        datetime.datetime.strptime(f"{today.year}-12-25", "%Y-%m-%d").date() -
        today).days
    distance_12_25 = distance_12_25 if distance_12_25 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-12-25",
                                   "%Y-%m-%d").date() - today).days

    time_ = [
        {
            "v": distance_year,
            "title": "元旦节"
        },
        {
            "v": distance_big_year,
            "title": "过春节"
        },
        {
            "v": distance_1_15,
            "title": "元宵节"
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

    # 企业微信卡片只支持显示6个，所以移除距离较远的多余节日
    time_ = sorted(time_, key=lambda x: x['v'], reverse=False)
    while len(time_) > 6:
        time_.pop()

    print(time_)
    return time_


def get_one_text():
    # 文档 https://gushi.ci/ 和 https://www.jinrishici.com/

    send_url = "https://v1.jinrishici.com/all.json"
    headers = {"Content-Type": "text/plain"}
    res = requests.post(url=send_url, headers=headers)

    return json.loads(res.text).get('content')


def send_msg():
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
    send_url = WEBHOOK
    send_data = {
        "msgtype": "template_card",
        "template_card": {
            "card_type":
            "news_notice",
            "main_title": {
                "title": "劝摸",
                "desc":
                f"今天是 {today.year}年{today.month}月{today.day}日 {week_day_}",
            },
            "card_image": {
                "url": "https://i.loli.net/2020/11/18/3zogEraBFtOm5nI.jpg",
            },
            "vertical_content_list": [{
                "title": "一起去摸鱼吗？虽然被抓住就是一整天的禁闭，但鱼很好吃，所以值得！!",
                "desc": "\n" + one_text + "\n"
            }],
            "horizontal_content_list":
            states,
            "jump_list": [
                {
                    "type": 1,
                    "url":
                    "https://weather.com/zh-CN/weather/today/l/24.27,116.13?par=apple_todayosx",
                    "title": "🐟🐟🐟🐟苹果天气🐟🐟🐟🐟"
                },
            ],
            "card_action": {
                "type": 1,
                "url": "https://www.google.com.hk/search?q=" + one_text,
                "appid": "APPID",
                "pagepath": "PAGEPATH"
            }
        }
    }

    res = requests.post(url=send_url, headers=headers, json=send_data)
    print(res.text)


def main_handler():
    send_msg()
    return ("执行完成")


main_handler()
