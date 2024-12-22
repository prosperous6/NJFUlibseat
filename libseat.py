import json
import requests
import sys
import io
import base64
import time
from datetime import datetime
import login
import time
import seatQuery
import findSeat

reverse_url = "https://libseat.njfu.edu.cn/ic-web/reserve"


def format_timestamp_time(timestamp):
    dt_object = datetime.utcfromtimestamp(timestamp / 1000 + 8 * 3600)
    formatted_time_str = dt_object.strftime("%H:%M")
    return formatted_time_str


def format_timestamp_date(timestamp):
    dt_object = datetime.utcfromtimestamp(timestamp / 1000 + 8 * 3600)
    formatted_date_str = dt_object.strftime("%m.%d")
    return formatted_date_str


def bookSeat(username, password, seatlist, beginTime, endTime, wechat_id):
    USER = login.login(username, password)

    sess = USER["session"]
    userinfo = json.loads(USER["userinfo"])
    print(userinfo)

    reserve_response = None

    for seat in seatlist:
        data = {
            "sysKind": 8,
            "appAccNo": userinfo["data"]["accNo"],
            "memberKind": 1,
            "resvMember": [userinfo["data"]["accNo"]],
            "resvBeginTime": beginTime,
            "resvEndTime": endTime,
            "testName": "",
            "captcha": "",
            "resvProperty": 0,
            "resvDev": [
                findSeat.find_dev_id(sess, seat, beginTime[:10].replace("-", ""))["id"]
            ],
            "memo": "",
        }

        reserve_response = sess.post(reverse_url, json=data)
        print(reserve_response.text)
        if json.loads(reserve_response.text)["code"] != 0:
            continue
        else:
            break

    reserve_response = json.loads(reserve_response.text)

    seatinfo = seatQuery.currentBook(sess=sess)
    print(seatinfo)

# Push message

    time_str = "| "
    seat_str = "| "

    for reservation in seatinfo.get("data", []):
        resv_begin_time = reservation.get("resvBeginTime", "")
        resv_end_time = reservation.get("resvEndTime", "")

        dev_info = reservation.get("resvDevInfoList", [{}])[0]
        dev_name = dev_info.get("devName", "")

        time_str += (
            format_timestamp_date(resv_begin_time)
            + " "
            + format_timestamp_time(resv_begin_time)
            + "-"
            + format_timestamp_time(resv_end_time)
            + " | "
        )
        seat_str += dev_name + " | "

    messageURL = (
        "https://WEBHOOK.com/?wxid="
        + wechat_id
        + "&id="
        + username
        + "&status="
        + reserve_response["message"]
        + "&time="
        + time_str
        + "&seat="
        + seat_str
    )

    sess.get(messageURL)