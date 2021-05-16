import email
import smtplib
from datetime import datetime
import requests

'''
# FOR 7 DAYS DATA

def create_session_info(center, session):
    return {"name": center["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "age_limit": session["min_age_limit"]}

def get_sessions(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield create_session_info(center, session)
'''

# FOR PRESENT DAY DATA

def create_session_info(session):
    return {"name": session["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "age_limit": session["min_age_limit"]}

def get_sessions(data):
    for session in data["sessions"]:
        yield create_session_info(session)

def is_available(session):
    return session["capacity"] > 0

def is_age_available(session):
    return session["age_limit"] == 18

def get_data(start_date):
    # url for 7 days
    # url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

    # url for present day
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"
    params = {"district_id": 199, "date": start_date.strftime("%d-%m-%Y")}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    return [session for session in get_sessions(data) if is_age_available(session) and is_available(session)]

def create_output(session_info):
    return f"{session_info['date']} - {session_info['name']} ({session_info['capacity']})"

print(get_data(datetime.today()))
content = "\n".join([create_output(session_info) for session_info in get_data(datetime.today())])
username = ""
password = ""

if not content:
    print("No availability")
else:
    email_msg = email.message.EmailMessage()
    email_msg["Subject"] = "Vaccination Slot Open"
    email_msg["From"] = username
    email_msg["To"] = username
    email_msg.set_content(content)

    with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
        server.starttls()
        server.login(username, password)
        server.send_message(email_msg, username, username)