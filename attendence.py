import streamlit as st
import requests
#from dotenv import load_dotenv
import os
#from streamlit_qrcode_scanner import qrcode_scanner

#load_dotenv()           # Load the environment variables            

st.title('attendance')


def get_cookies(username,password):
    headers = {
    'accept': 'application/json, text/plain, /',
    'accept-language': 'en-GB,en;q=0.8',
    'clienttzofst': '330',
    'content-type': 'application/json',
    'origin': 'https://student.bennetterp.camu.in',
    'priority': 'u=1, i',
    'referer': 'https://student.bennetterp.camu.in/v2/?id=663474b11dd0e9412a1f793f',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    }

    json_data = {
        'dtype': 'M',
        'Email': username,
        'pwd': password,
    }

    response = requests.post('https://student.bennetterp.camu.in/login/validate', headers=headers, json=json_data)
    # student_id = response.json()["student_id"]
    # print(response.json())
    stu_id=(response.json()["output"]["data"]["logindetails"]["Student"][0]["StuID"])
    cookie = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
    # print(cookie)
    return cookie, stu_id

def mark_attendance(stu_id, cookie, qr_code):
    cookies = {
        'connect.sid': cookie,
    }

    headers = {
        'accept': 'application/json, text/plain, /',
        'accept-language': 'en-GB,en;q=0.8',
        'clienttzofst': '330',
        'content-type': 'application/json',
        'origin': 'https://student.bennetterp.camu.in',
        'priority': 'u=1, i',
        'referer': 'https://student.bennetterp.camu.in/v2/timetable',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
    }

    json_data = {
        'attendanceId': qr_code,
        'StuID': stu_id,
        'offQrCdEnbld': True,
    }

    response = requests.post(
        'https://student.bennetterp.camu.in/api/Attendance/record-online-attendance',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    
    return response.json()["output"]["data"]["code"]


stu_profiles = [
    {
        "username": "e22cseu0824@bennett.edu.in",
        "password": "Deoghar#@5373",
        "name": "Vaibhav kasuhik",
        "category": ["Automata", "AI"]
    }
]



# check boxes
category = st.radio(
    "Category?",
    ["Automata", "Cloud Computing", "AI", "Blockchain", "Cyber Sec", "DataScience"]
)


# next button 
if category:
    # print(category)

    qr_code = qrcode_scanner(key='qrcode_scanner')

    if qr_code:
        for i in stu_profiles:
            if category in i["category"]:
                try: 
                    cookie, stu_id = get_cookies(i["username"], i["password"])
                    response = mark_attendance(stu_id, cookie, qr_code)
                    st.write(i["name"], response)
                except:
                    st.write(i["name"], "Error")


# for i in stu_profiles:
#     cookie, stu_id = get_cookies(i["username"], i["password"])
#     response = mark_attendance(stu_id, cookie, "66cd6c1be75561757d9ab726_66cd6c1be75561757d9ab727")
#     print(i["name"], response)
