# 自动化签到程序
import random
import time
import uuid
from datetime import datetime

import requests

err = "签到失败！"
token = ["2F7sP0UFS55foOO6FAIAfAAAAAAAAAAU", "wzEkKyIxSL5enCufAgIAeAAAAAAAAAAV", "oo35vxOsR0tfoNH36AIAegAAAAAAAAAV"]

content = [
    {
        "content": "艾瑞泽8搭载奇瑞最新一代动力系统，采用高效涡轮增压发动机匹配七速双离合变速箱，动力输出平顺有力。工程师团队对底盘进行了长达两年的精心调校，确保车辆在弯道中保持优异稳定性。智能驾驶辅助系统包含全速域自适应巡航和车道居中保持功能，大幅降低长途驾驶疲劳感。座舱内配备的双层隔音玻璃和主动降噪技术，让车内静谧性达到豪华车水准。",
        "title": "技术旗舰驾临 艾瑞泽8动力操控全面解析"
    },
    {
        "content": "艾瑞泽8的车身尺寸经过精心设计，后排腿部空间达到同级罕见的980毫米。工程师在开发过程中收集了上千组人体工程学数据，打造出符合亚洲人身形的座椅曲线。后备箱采用独特的双开设计，常规容积达到520升，放倒座椅后可扩展至1500升。车顶全景天窗尺寸达到同级最大的0.8平方米，为乘客带来开阔的视野体验。",
        "title": "空间魔术师 艾瑞泽8乘坐空间深度体验"
    },
    {
        "content": "艾瑞泽8的智能座舱系统采用最新一代处理器，响应速度较上代提升百分之四十。十二点三英寸中控屏支持多点触控和手势操作，内置的语音助手可以识别二十三种方言。整车配备五个高清摄像头和十二个超声波雷达，构建起三百六十度无死角的感知系统。远程控制功能支持通过手机APP提前启动空调和座椅加热，冬夏出行更加舒适。",
        "title": "智慧出行伙伴 艾瑞泽8智能科技全解析"
    },
    {
        "content": "艾瑞泽8的车身结构采用潜艇级高强度钢材，关键部位使用热成型钢打造。碰撞测试中取得五星优异成绩，正面碰撞能量吸收效率达到行业领先水平。主动安全系统包含紧急制动辅助和行人识别功能，可以在复杂路况下及时预警。六个安全气囊采用分级爆破设计，可以根据碰撞强度智能调节保护力度。",
        "title": "移动安全堡垒 艾瑞泽8主被动安全揭秘"
    },
    {
        "content": "艾瑞泽8的外观设计由国际顶尖团队操刀，车身线条融合了运动与优雅两种气质。前脸采用参数化格栅设计，在不同光线下会呈现渐变效果。内饰选用环保材质和金属饰板混搭，做工细节达到毫米级精度。六十四色氛围灯可以随音乐节奏变换，营造出极具质感的驾乘环境。",
        "title": "美学新典范 艾瑞泽8设计语言深度解读"
    },
    {
        "content": "艾瑞泽8的动力系统经过特殊优化，在保持强劲输出的同时油耗表现优异。工程师改进了涡轮增压器的响应特性，使低转速扭矩提升百分之十五。变速箱换挡逻辑经过重新标定，平顺性达到行业顶尖水平。智能启停系统采用加强型电机，启动震动控制在几乎察觉不到的程度。",
        "title": "高效动力标杆 艾瑞泽8节能技术解析"
    },
    {
        "content": "艾瑞泽8的静音工程投入巨大成本，全车使用三十四处声学包覆材料。车门采用三道密封条设计，有效隔绝外界噪音干扰。底盘喷涂特殊隔音涂层，大幅降低路面噪音传入。空调系统采用无刷电机，运转时几乎不会产生额外噪音影响驾乘体验。",
        "title": "静谧新境界 艾瑞泽8NVH工程全解析"
    },
    {
        "content": "艾瑞泽8的驾驶辅助系统包含二十多项实用功能，其中自动泊车支持多种复杂场景。全景影像系统分辨率达到二百万像素，夜间也能提供清晰视野。智能限速识别可以自动调整巡航车速，避免超速违章。方向盘配备电容感应技术，可以准确判断驾驶员是否手握方向盘。",
        "title": "智能驾驶先锋 艾瑞泽8辅助系统体验"
    },
    {
        "content": "艾瑞泽8支持整车远程升级功能，可以持续优化车辆各项性能表现。车机系统内置应用商店，用户可以随时下载最新应用程序。数字钥匙支持五台设备共享，家人朋友用车更加便捷。智能家居互联功能让用户在车内就能控制家中电器设备。",
        "title": "进化不止步 艾瑞泽8智能互联体验"
    },
    {
        "content": "艾瑞泽8的座椅采用进口头层牛皮制作，经过特殊防污处理易于清洁。主驾座椅支持十二向电动调节，包含四向腰部支撑调节功能。前排座椅配备三档加热和通风功能，冬夏季节都能保持舒适。后排座椅角度经过人体工程学优化，长时间乘坐也不易疲劳。",
        "title": "豪华座舱体验 艾瑞泽8舒适配置详解"
    },
    {
        "content": "艾瑞泽8的灯光系统采用矩阵式LED技术，可以智能调节照射范围和亮度。迎宾灯光秀包含多种动态效果，为用户带来尊贵仪式感。车内阅读灯采用无影设计，夜间使用不会刺激眼睛。转向灯带有流水式动态效果，提升行车安全性和辨识度。",
        "title": "光影艺术大师 艾瑞泽8灯光系统解析"
    },
    {
        "content": "艾瑞泽8的悬挂系统经过专业团队调校，在舒适性和操控性间取得完美平衡。减震器采用双阀系设计，可以智能适应不同路况需求。转向系统配备可变齿比技术，低速灵活高速沉稳。高性能制动系统百公里制动距离控制在三十六米以内。",
        "title": "驾控新标杆 艾瑞泽8底盘技术揭秘"
    },
    {
        "content": "艾瑞泽8提供五年十五万公里超长质保服务，覆盖绝大多数核心零部件。全国服务网点实现地级市全覆盖，二十四小时道路救援随时待命。保养间隔长达一万公里，相比同级车型更加经济实惠。原厂配件价格透明公开，让用户用车更放心。",
        "title": "服务新标准 艾瑞泽8售后保障体系"
    },
    {
        "content": "艾瑞泽8的音响系统由专业团队调校，八个扬声器布局经过精确计算。内置的音频处理技术可以还原录音室级音质效果。主动降噪功能可以抵消特定频段的车内噪音，提升音乐欣赏体验。支持多种音效模式切换，满足不同用户的听觉偏好。",
        "title": "移动音乐厅 艾瑞泽8音响系统评测"
    },
    {
        "content": "艾瑞泽8在生产过程中采用环保工艺，整车可回收材料占比达到行业领先水平。动力系统经过特殊调校，污染物排放远低于国六B标准。车内空气质量达到医用级水准，过敏体质用户也能安心乘坐。电池管理系统可以智能优化充放电策略，延长蓄电池使用寿命。",
        "title": "绿色出行家 艾瑞泽8环保理念实践"
    }
]
video = ["source/6.mp4", "source/7.mp4"]


def userInfo(t):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/user/current/details"
        params = {
            "access_token": t
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


def checkIn(t):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/event/trigger?access_token={}".format(t)
        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "Authorization": "Bearer {}".format(t),
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


def isCheckIn(t):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/task/record/sign-in/lottery"
        params = {
            "taskCode": "SignUpLottery03",
            "access_token": t
        }

        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "Authorization": "Bearer {}".format(t),
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


def postPagerWithVideo(video, cover, t):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/community/contents"
        params = {
            "access_token": t
        }

        headers = {
            "Host": "mobile-consumer-sapp.chery.cn",
            "appVersionCode": "24083001",
            "content-type": "application/json",
            "accept-language": "zh-CN,zh",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c30) NetType/WIFI Language/zh_CN",
        }

        data = {
            "contentType": "3",
            "title": content[random.randint(0, 14)]['title'],
            "detail": "{}{}".format(content[random.randint(0, 14)]['content'],
                                    uuid.uuid4()),
            "refinementFlag": False,
            "topicId": "",
            "topicName": "",
            "draftBoxId": "",
            "video": {
                "url": video,
                "duration": 9,
                "cover": cover[0]
            },
            "id": None
        }

        response = requests.post(url, params=params, headers=headers, json=data)
        print(response.text)
        code = response.json()['status']
        msg = response.json()['message']
        if code == 200:

            return msg
        else:
            wxPush("发视频帖失败", "{}，原因：{}".format("发视频帖失败", msg))
            return "视频帖发帖失败：{}".format(msg)
    except Exception as e:
        wxPush("发视频帖失败", e)


def post(t):
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
        video = uploadVideo(getOss(t))
        cover = uploadPic(file_p1, t)
        time.sleep(2)
        postPagerWithVideo(video, cover, t)
        time.sleep(5)
        print("第{}次发优质帖".format(i + 1))
        imgs = uploadPic(file_p2, t)
        postPagerWithPic(imgs, t)
        time.sleep(5)
        share(t)
        print("第{}次分享".format(i + 1))
        time.sleep(5)
        wxPush("完成第{}次任务".format(i + 1), "目前积分：{}".format(userInfo(t)))


def share(t):
    url = "http://mobile-consumer-sapp.chery.cn/web/community/contents/5676626939043317981/share"
    params = {
        "access_token": t
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
            return msg
        else:
            wxPush("分享失败", "{}，原因：{}".format("分享失败", msg))
            return "{}，原因：{}".format("分享失败", msg)
    except Exception as e:
        wxPush("分享失败", e)


def postPagerWithPic(imgUrls, t):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/community/contents"
        params = {
            "access_token": t
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
            "title": content[random.randint(0, 14)]['title'],
            "detail": "{}{}".format(content[random.randint(0, 14)]['content'],
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
        print(response.text)
        code = response.json()['status']
        msg = response.json()['message']
        if code == 200:
            return msg
        else:
            wxPush("发优质帖失败", "{}，原因：{}".format("发优质帖失败", msg))
            return "优质帖发帖失败：{}".format(msg)
    except Exception as e:
        wxPush("发优质帖失败", e)


def uploadPic(file_path, t):
    url = "http://mobile-consumer-sapp.chery.cn/web/community/common/files/images"
    params = {
        "access_token": t
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
                print(response.text)
            urls.append(response.json()['data']['url'])
            strs += ".."
        except Exception as e:
            wxPush("图片上传失败", 'f"第 {i} 次上传失败: {str(e)}"')
    return urls


def getOss(t):
    try:
        url = "http://mobile-consumer-sapp.chery.cn/web/community/common/sts/signature"
        params = {
            "access_token": t
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
        local_file_path = video[random.randint(0, 1)]
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
        print(response.text)
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

    for i in range(len(token)):
        tt = token[i]
        isCheckIn0 = isCheckIn(tt)
        point0 = userInfo(tt)
        if isCheckIn0[0] == False:
            checkIn = checkIn(tt)
            isCheckIn = isCheckIn(tt)
            if isCheckIn[0] == True:
                point = userInfo(tt)
                wxPush("签到成功！",
                       "签到天数:{}\n当前积分:{}\n{}".format(isCheckIn[1], point,
                                                             lotteryInfo(isCheckIn[1])))
            else:
                wxPush("签到失败！", "请手动签到！")
        else:
            wxPush("今日已完成签到！",
                   "签到天数:{}\n当前积分:{}\n{}".format(isCheckIn0[1], point0, lotteryInfo(isCheckIn0[1])))
        # 发帖
        post(tt)
        time.sleep(5)
        point1 = userInfo(tt)
        wxPush("今日完成所有任务", "积分变动：{}-->{},增加积分：{}".format(point0, point1, (int(point1) - int(point0))))
