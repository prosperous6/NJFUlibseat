import requests
import time
import json
from datetime import datetime, timedelta


def extract_required_fields(original_json, target_resv_status=1027):
    original_json = json.loads(original_json)
    new_json_data = {
        "code": original_json["code"],
        "message": original_json["message"],
        "data": [],
    }

    for reservation in original_json["data"]:
        if reservation["resvStatus"] == target_resv_status:
            new_reservation = {
                "resvBeginTime": reservation["resvBeginTime"],
                "resvEndTime": reservation["resvEndTime"],
                "resvStatus": reservation["resvStatus"],
                "resvDevInfoList": [],
            }

            for dev_info in reservation["resvDevInfoList"]:
                new_dev_info = {
                    "devName": dev_info["devName"],
                    "roomName": dev_info["roomName"],
                }
                new_reservation["resvDevInfoList"].append(new_dev_info)

            new_json_data["data"].append(new_reservation)

    return new_json_data


def currentBook(sess):
    beginDate = datetime.now().date()
    endDate = beginDate + timedelta(days=3)
    url = (
        "https://libseat.njfu.edu.cn/ic-web/reserve/resvInfo?beginDate="
        + str(beginDate)
        + "&endDate="
        + str(endDate)
    )

    resp = sess.get(url)

    return extract_required_fields(resp.text)