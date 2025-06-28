# 自动化签到程序
import random
import time
import uuid
from datetime import datetime

import requests

err = "签到失败！"
token = "QVL8OserRp1enCufAgIAeAAAAAAAAAAU"


def userInfo():
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/user/current/details"
        params = {
            "access_token": token
        }

        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "content-type": "application/json",
            "accept-language": "zh-CN,zh",
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
    except Exception as e:
        wxPush("积分获取失败", e)


def checkIn():
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/event/trigger?access_token={}".format(token)
        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json",
            "accept-language": "zh-CN,zh",
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
    except Exception as e:
        wxPush("签到失败", e)


def isCheckIn():
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/task/record/sign-in/lottery"
        params = {
            "taskCode": "SignUpLottery03",
            "access_token": token
        }

        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "Authorization": "Bearer {}".format(token),
            "Content-Type": "application/json",
            "accept-language": "zh-CN,zh",
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
    except Exception as e:
        wxPush("签到检查失败", e)


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


def postPagerWithVideo(video, cover):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/community/contents"
        params = {
            "access_token": token
        }

        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "appVersionCode": "24083001",
            "content-type": "application/json",
            "accept-language": "zh-CN,zh",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c30) NetType/WIFI Language/zh_CN",
        }

        data = {
            "contentType": "2",
            "title": "【10万级家轿卷王！奇瑞艾瑞泽8真香警告】",
            "detail": "【10万级家轿卷王！奇瑞艾瑞泽8真香警告】🔥  \n\n✨ 1.6T爆197马力，7秒级破百！同级最强鲲鹏动力，油耗仅6.5L！  \n✨ 近4.8米车长+2.79米轴距，后排能跷二郎腿，B级空间A级价！  \n✨ 双12.3寸曲面屏+索尼8音响，L2.5级智驾全系标配！  \n💥 终身质保+终身免流量，11.99万起售，合资车看完直哆嗦！  \n\n#奇瑞艾瑞泽8 #十万级家轿天花板  \n👉 试过才知道：10万预算买30万享受！防伪：{}".format(
                uuid.uuid4()),
            "refinementFlag": False,
            "topicId": "4984941113360139749",
            "topicName": "安全，你可以永远相信奇瑞",
            "draftBoxId": "",
            "video": {
                "url": video,
                "duration": 9,
                "cover": cover[0]
            },
            "id": None
        }

        response = requests.post(url, params=params, headers=headers, json=data)
        code = response.json()['status']
        msg = response.json()['message']
        if code == 200:
            time.sleep(5)
            wxPush("完成发视频帖", "目前积分：{}".format(userInfo()))
            return msg
        else:
            wxPush("发视频帖失败", "{}，原因：{}".format("发视频帖失败", msg))
            return "视频帖发帖失败：{}".format(msg)
    except Exception as e:
        wxPush("发视频帖失败", e)


def post():
    file_p1 = [
        'source/cover.jpg'
    ]
    file_p2 = [
        "source/1.jpg",
        "source/2.jpg",
        "source/3.jpg",
        "source/4.jpg",
        "source/5.jpg"
    ]

    # 发帖
    for i in range(2):
        print("第{}次发视频帖".format(i + 1))
        video = uploadVideo(getOss())
        cover = uploadPic(file_p1)
        postPagerWithVideo(video, cover)
        time.sleep(5)
        print("第{}次发优质帖".format(i + 1))
        imgs = uploadPic(file_p2)
        postPagerWithPic(imgs)
        time.sleep(5)
        share()
        print("第{}次分享".format(i + 1))
        time.sleep(5)


def share():
    url = "http://mobile-consumer-sapp.chery.cn/web/community/contents/5676626939043317981/share"
    params = {
        "access_token": token
    }

    headers = {
        "Host": "mobile-consumer-sapp.chery.cn",
        "appVersionCode": "24083001",
        "content-type": "application/json",
        "accept-language": "zh-CN,zh",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c30) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wxb9166feb639e35a2/153/page-frame.html"
    }
    data = {}
    try:
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=data  # 自动设置Content-Type为application/json
        )
        print(response.text)
        # 解析JSON响应
        code = response.json()['status']
        msg = response.json()['message']
        if code == 200:
            time.sleep(5)
            wxPush("完成分享", "目前积分：{}".format(userInfo()))
            return msg
        else:
            wxPush("分享失败", "{}，原因：{}".format("分享失败", msg))
            return "{}，原因：{}".format("分享失败", msg)
    except Exception as e:
        wxPush("分享失败", e)


def postPagerWithPic(imgUrls):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/community/contents"
        params = {
            "access_token": token
        }

        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "appVersionCode": "24083001",
            "content-type": "application/json",
            "accept-language": "zh-CN,zh",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c30) NetType/WIFI Language/zh_CN",
        }

        data = {
            "contentType": "2",
            "title": "",
            "detail": "【10万级家轿卷王！奇瑞艾瑞泽8真香警告】🔥  \n\n✨ 1.6T爆197马力，7秒级破百！同级最强鲲鹏动力，油耗仅6.5L！  \n✨ 近4.8米车长+2.79米轴距，后排能跷二郎腿，B级空间A级价！  \n✨ 双12.3寸曲面屏+索尼8音响，L2.5级智驾全系标配！  \n💥 终身质保+终身免流量，11.99万起售，合资车看完直哆嗦！  \n\n#奇瑞艾瑞泽8 #十万级家轿天花板  \n👉 试过才知道：10万预算买30万享受！\n防伪：{}".format(
                uuid.uuid4()),
            "refinementFlag": False,
            "topicId": "4984941113360139749",
            "topicName": "安全，你可以永远相信奇瑞",
            "draftBoxId": "",
            "pictureUrls": imgUrls,
            "id": None
        }
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=data
        )
        code = response.json()['status']
        msg = response.json()['message']
        if code == 200:
            time.sleep(5)
            wxPush("完成发优质帖", "目前积分：{}".format(userInfo()))
            return msg
        else:
            wxPush("发优质帖失败", "{}，原因：{}".format("发优质帖失败", msg))
            return "优质帖发帖失败：{}".format(msg)
    except Exception as e:
        wxPush("发优质帖失败", e)


def uploadPic(file_path):
    url = "http://mobile-consumer-sapp.chery.cn/web/community/common/files/images"
    params = {
        "access_token": token
    }

    headers = {
        "Host": "mobile-consumer-sapp.chery.cn",
        "Connection": "keep-alive",
        "accept-language": "zh-CN,zh",
        "Accept": "*/*",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c30) NetType/WIFI Language/zh_CN",
        "Referer": "https://servicewechat.com/wxb9166feb639e35a2/153/page-frame.html"
    }

    urls = []
    strs = "上传中"
    for i, img_path in enumerate(file_path, 1):
        time.sleep(0.2)

        try:
            with open(img_path, 'rb') as f:
                files = {'file': (img_path, f, 'image/jpeg')}
                print(strs)
                response = requests.post(url, params=params, headers=headers, files=files)

            urls.append(response.json()['data']['url'])
            strs += ".."
        except Exception as e:
            wxPush("图片上传失败", 'f"第 {i} 次上传失败: {str(e)}"')
    return urls


def getOss():
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/community/common/sts/signature"
        params = {
            "access_token": token
        }
        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "appVersionCode": "24083001",
            "content-type": "application/json",
            "accept-language": "zh-CN,zh",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c30) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wxb9166feb639e35a2/153/page-frame.html"
        }

        response = requests.get(url, params=params, headers=headers)

        return response.json()['data']
    except Exception as e:
        wxPush("获取配置失败", e)


def uploadVideo(oss_config):
    try:
        local_file_path = "source/6.mp4"
        file_name = generate_random_string() + '.mp4'  # 提取文件名
        # 构造上传URL
        upload_url = f"http://{oss_config['bucket']}.{oss_config['endpoint']}"

        # 构造FormData
        files = {
            'file': (file_name, open(local_file_path, 'rb'), 'video/mp4')
        }
        data = {
            'key': f"{oss_config['folder']}/{file_name}",  # OSS存储路径
            'policy': oss_config['policy'],
            'OSSAccessKeyId': oss_config['accessId'],
            'signature': oss_config['signature'],
            'success_action_status': '200'  # 上传成功返回200
        }

        # 发送POST请求
        response = requests.post(upload_url, data=data, files=files)
        code = response.status_code
        file_url = f"https://{oss_config['bucket']}.{oss_config['endpoint']}/{oss_config['folder']}/{file_name}"
        if code == 200:
            return file_url
        else:
            wxPush("上传视频失败：{}".format(code), "")
            raise RuntimeError
    except Exception as e:
        wxPush("上传视频失败", e)


def generate_random_string(length=18):
    """生成随机字符串"""
    chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz"
    # 生成当前时间的格式化字符串
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    a = ''.join(random.choice(chars) for _ in range(length))
    a += timestamp
    return a


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
    # 发帖
    post()
    point1 = userInfo()
    wxPush("今日完成所有任务", "积分变动：{}--》{}".format(point0, point1))
