import json

RoomID = {
    "2F-A": 100455344,
    "2F-B": 100455346,
    "3F-A": 100455350,
    "3F-B": 100455352,
    "3F-C": 100455354,
    "3FA-": 111488386,
    "4F-A": 100455356,
    "4FA-": 111488388,
    "5F-A": 100455358,
    "6F-A": 100455360,
    "7F-A": 106658017,
}


def find_dev_id(sess, seat_name, date):
    room_id = RoomID[seat_name[:4]]

    if room_id is None:
        return None

    current_seat_url = (
        "https://libseat.njfu.edu.cn/ic-web/reserve?roomIds="
        + str(room_id)
        + "&resvDates="
        + date
        + "&sysKind=8"
    )

    data = json.loads(sess.get(current_seat_url).text)

    for seat in data["data"]:
        if seat["devName"] == seat_name:
            return {"id": seat["devId"], "data": seat}

    return None