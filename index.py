import datetime
import requests
import json
from zhdate import ZhDate as lunar_date


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
    # print("大年时间: ", lunar_date(today.year+1, 1, 1).to_datetime().date())
    # print("端午时间: ", lunar_date(today.year, 5, 5).to_datetime().date())
    # print("中秋时间: ", lunar_date(today.year, 8, 15).to_datetime().date())
    # print("元旦时间: ", f"{today.year+1}-01-01")
    # print("清明时间: ", f"{today.year+1}-04-05")
    # print("劳动时间: ", f"{today.year+1}-05-01")
    # print("国庆时间: ", f"{today.year+1}-10-01")

    distance_big_year = (lunar_date(today.year, 1, 1).to_datetime().date() -
                         today).days
    distance_big_year = distance_big_year if distance_big_year > 0 else (
        lunar_date(today.year + 1, 1, 1).to_datetime().date() - today).days

    distance_5_5 = (lunar_date(today.year, 5, 5).to_datetime().date() -
                    today).days
    distance_5_5 = distance_5_5 if distance_5_5 > 0 else (
        lunar_date(today.year + 1, 5, 5).to_datetime().date() - today).days

    distance_8_15 = (lunar_date(today.year, 8, 15).to_datetime().date() -
                     today).days
    distance_8_15 = distance_8_15 if distance_8_15 > 0 else (
        lunar_date(today.year + 1, 8, 15).to_datetime().date() - today).days

    distance_year = (
        datetime.datetime.strptime(f"{today.year}-01-01", "%Y-%m-%d").date() -
        today).days
    distance_year = distance_year if distance_year > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-01-01",
                                   "%Y-%m-%d").date() - today).days

    distance_4_5 = (
        datetime.datetime.strptime(f"{today.year}-04-05", "%Y-%m-%d").date() -
        today).days
    distance_4_5 = distance_4_5 if distance_4_5 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-04-05",
                                   "%Y-%m-%d").date() - today).days

    distance_5_1 = (
        datetime.datetime.strptime(f"{today.year}-05-01", "%Y-%m-%d").date() -
        today).days
    distance_5_1 = distance_5_1 if distance_5_1 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-05-01",
                                   "%Y-%m-%d").date() - today).days

    distance_10_1 = (
        datetime.datetime.strptime(f"{today.year}-10-01", "%Y-%m-%d").date() -
        today).days
    distance_10_1 = distance_10_1 if distance_10_1 > 0 else (
        datetime.datetime.strptime(f"{today.year + 1}-10-01",
                                   "%Y-%m-%d").date() - today).days

    # print("距离大年: ", distance_big_year)
    # print("距离端午: ", distance_5_5)
    # print("距离中秋: ", distance_8_15)
    # print("距离元旦: ", distance_year)
    # print("距离清明: ", distance_4_5)
    # print("距离劳动: ", distance_5_1)
    # print("距离国庆: ", distance_10_1)
    # print("距离周末: ", 5 - today.weekday())

    time_ = [
        # {
        #     "v": 5 - today.weekday(),
        #     "title": "周末"
        # },  # 距离周末
        {
            "v": distance_year,
            "title": "元旦节"
        },  # 距离元旦
        {
            "v": distance_big_year,
            "title": "过大年"
        },  # 距离过年
        {
            "v": distance_4_5,
            "title": "清明节"
        },  # 距离清明
        {
            "v": distance_5_1,
            "title": "劳动节"
        },  # 距离劳动
        {
            "v": distance_5_5,
            "title": "端午节"
        },  # 距离端午
        #{
        #    "v": distance_8_15,
        #    "title": "中秋节"
        #},  # 距离中秋
        {
            "v": distance_10_1,
            "title": "国庆节"
        },  # 距离国庆
    ]

    time_ = sorted(time_, key=lambda x: x['v'], reverse=False)
    return time_

def get_one_text():
    # 文档 https://gushi.ci/ 和 https://www.jinrishici.com/

    send_url = "https://v1.jinrishici.com/all.json"
    headers = {"Content-Type": "text/plain"}
    res = requests.post(url=send_url, headers=headers)

    return json.loads(res.text).get('content')

def get_one_image():
    # https://api.ixiaowai.cn

    send_url = "https://api.ixiaowai.cn/api/api.php?return=json"
    headers = {"Content-Type": "text/plain"}
    res = requests.post(url=send_url, headers=headers)

    print(res.json())
    # return json.loads(res.text).get('imgurl')


def send_msg():
    today = datetime.date.today()
    week_day_ = get_week_day(today)
    time_data = time_parse(today)

    one_text = get_one_text()
    # one_image = get_one_image()

    states = []
    for item in time_data:
        keyname = f"🐟距离{item['title']}"
        value = f"还有{item['v']}天"
        states.append({"keyname": keyname, "value": value})

    headers = {"Content-Type": "text/plain"}
    send_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=dbd6fb2c-f269-4d2b-9522-6b91612c676a"
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
                # "url": one_image
            },
            "vertical_content_list": [{
                "title":
                "一起去摸鱼吗？虽然被抓住就是一整天的禁闭，但鱼很好吃，所以值得！!",
                "desc":
                "\n"+one_text+"\n"
            }],
            "horizontal_content_list":
            states,
            "jump_list":[
                {
                    "type":1,
                    "url":"https://weather.com/zh-CN/weather/today/l/24.27,116.13?par=apple_todayosx",
                    "title":"🐟🐟🐟🐟苹果天气🐟🐟🐟🐟"
                },
            ],
            "card_action": {
                "type": 1,
                "url":
                "https://www.google.com.hk/search?q="+one_text,
                "appid": "APPID",
                "pagepath": "PAGEPATH"
            }
        }
    }

    res = requests.post(url=send_url, headers=headers, json=send_data)
    print(res.text)


def main_handler():
    send_msg()
    # get_one_text() 测试一言句子时使用
    # get_one_image()
    print("执行完成")

main_handler()
