# 自动化签到程序
import requests

err = "签到失败！"
token = "QVL8OserRp1enCufAgIAeAAAAAAAAAAU"


def userInfo():
    url = "http://mobile-consumer-sapp.chery.cn/web/user/current/details"
    params = {
        "access_token": token
    }

    headers = {
        "Host": "mobile-consumer-sapp.chery.cn",
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c2c) NetType/WIFI Language/zh_CN",
    }

    response = requests.get(url, params=params, headers=headers)
    code = response.json()['status']
    msg = response.json()['message']
    if code == 200:
        points = response.json()['data']['pointAccount']['payableBalance']
        return points
    else:
        return None


def checkIn():
    url = "http://mobile-consumer-sapp.chery.cn/web/event/trigger?access_token={}".format(token)
    headers = {
        "Host": "mobile-consumer-sapp.chery.cn",
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
        "Origin": "https://hybrid-sapp.chery.cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ios/1.0.0",
        "Referer": "https://hybrid-sapp.chery.cn/",
    }

    data = {"eventCode": "SJ10002"}

    response = requests.post(url, headers=headers, json=data)
    code = response.json()['status']
    msg = response.json()['message']
    if code == 200:
        return msg
    else:
        return "{},原因：{}".format(err, msg)


def isCheckIn():
    url = "http://mobile-consumer-sapp.chery.cn/web/task/record/sign-in/lottery"
    params = {
        "taskCode": "SignUpLottery03",
        "access_token": token
    }

    headers = {
        "Host": "mobile-consumer-sapp.chery.cn",
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
        "Origin": "https://hybrid-sapp.chery.cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ios/1.0.0",
        "Referer": "https://hybrid-sapp.chery.cn/",

    }

    response = requests.get(url, params=params, headers=headers)
    code = response.json()['status']
    msg = response.json()['message']
    status = response.json()['data']['todayCompleted']
    count = response.json()['data']['continualDays']
    if code == 200 and status == True:
        return True, count
    else:
        return False, -1


def get_lottery_info(check_in_count):
    prize_data = [
        {"stage": 7},
        {"stage": 15},
        {"stage": 30},
        {"stage": 60},
        {"stage": 90},
        {"stage": 180},
        {"stage": 360},
        {"stage": 540},
        {"stage": 720},
        {"stage": 1000}
    ]
    sorted_prizes = sorted(prize_data, key=lambda x: x['stage'])
    current_stage = None
    next_stage = None
    days_remaining = 0
    for prize in sorted_prizes:
        if check_in_count >= prize['stage']:
            current_stage = prize['stage']
        elif next_stage is None:  # 找到第一个未满足的阶段
            next_stage = prize['stage']
            days_remaining = prize['stage'] - check_in_count
            break  # 找到最近的未满足阶段后就可以退出

    return {
        "current_stage": current_stage,
        "next_stage": next_stage,
        "days_remaining": days_remaining if next_stage else 0
    }


def wxPush(title, content):
    re = requests.get("http://api.day.app/5J7ZXN6GCFxwZXMzCCgvUm/{}/{}".format(title, content))
    code = re.json()['code']
    msg = re.json()['message']
    if code == 200:
        return msg
    else:
        return "{}，原因：{}".format(err, msg)


def lotteryInfo(count):
    info = get_lottery_info(count)
    F = f"当前可参与抽奖阶段: {info['current_stage'] if info['current_stage'] is not None else '无'}"
    if info['next_stage']:
        FA = f"下一个抽奖阶段: {info['next_stage']} (还需签到{info['days_remaining']}天)"
        return f"{F}\n{FA}"
    else:
        return f"{F}\n已解锁所有抽奖阶段！"


if __name__ == "__main__":
    isCheckIn0 = isCheckIn()
    point0 = userInfo()
    if isCheckIn0[0] == False:
        checkIn = checkIn()
        isCheckIn = isCheckIn()
        if isCheckIn[0] == True:
            point = userInfo()
            wxPush("签到成功！",
                   "签到天数:{}\n当前积分:{}\n{}".format(isCheckIn[1], point,
                                                         lotteryInfo(isCheckIn[1])))
        else:
            wxPush("签到失败！", "请手动签到！")
    else:
        wxPush("今日已完成签到！",
               "签到天数:{}\n当前积分:{}\n{}".format(isCheckIn0[1], point0, lotteryInfo(isCheckIn0[1])))
