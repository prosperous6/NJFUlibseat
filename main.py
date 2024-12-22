# Use database

from datetime import datetime, timedelta
import json
import libseat
import sqlite3


conn = sqlite3.connect("data.db")
cursor = conn.cursor()


def generate_time_range(time_range, days_after=0):
    current_date = datetime.now()
    target_date = current_date + timedelta(days=days_after)

    start_time_str, end_time_str = time_range.split("-")
    start_time = datetime.strptime(
        f'{target_date.strftime("%Y-%m-%d")} {start_time_str.strip()}', "%Y-%m-%d %H:%M"
    )
    end_time = datetime.strptime(
        f'{target_date.strftime("%Y-%m-%d")} {end_time_str.strip()}', "%Y-%m-%d %H:%M"
    )
    result = {
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return json.dumps(result, indent=2)


cursor.execute("SELECT * FROM users where enable = 1")
loaddata = cursor.fetchall()
print(loaddata)

for user in loaddata:
    time_range = json.loads(generate_time_range(user[3], 2))
    print(user)
    aaa = list(user[2].split(","))
    print(aaa)
    for i in aaa:
        print(i)
    libseat.bookSeat(
        str(user[0]),
        str(user[1]),
        list(user[2].split(",")),
        str(time_range["start_time"]),
        str(time_range["end_time"]),
        str(user[4]),
    )