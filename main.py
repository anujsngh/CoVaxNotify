from playsound import playsound
import datetime as dt
import threading
import requests
import json
import time


def fire_alarm():
    playsound("imperial_alarm.mp3")


def main():
    while 1:
        st = time.time()
        today_date = dt.date.today().strftime("%d-%m-%Y")
        url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=486001&date={today_date}"
        response = requests.get(url)
        json_response = json.dumps(response.json(), indent=4)
        json_dict = json.loads(json_response)
        centers_list = json_dict["centers"]
        cached_session = {}
        for center in centers_list:
            for session in center["sessions"]:
                if session["min_age_limit"] == 45:
                    print(f"Checking for {center['name']} : {session['date']}")
                    if session["available_capacity_dose1"] > 0:
                        cached_session[center['name']] = {}
                        cached_session[center['name']]['Date'] = session['date']
                        cached_session[center['name']]['Doses'] = session['available_capacity_dose1']
                        print(f"Center Name : {center['name']}")
                        print(f"Date : {session['date']}")
                        print(f"Available Doses : {session['available_capacity_dose1']}")
                        print(f"Center Address : {center['address']}")
                        print()
                    else:
                        print(f"No slots for {session['vaccine']} at {center['name']} on {session['date']}")
                        print()

        if cached_session != {}:
            print(cached_session)
            threading.Thread(target=fire_alarm).start()

        time.sleep(30 - (time.time() - st))


if __name__ == '__main__':
    main()
