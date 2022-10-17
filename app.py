# Copyright (c) 2020 Cisco and/or its affiliates.
#
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at
#
#                https://developer.cisco.com/docs/licenses
#
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from flask import Flask, request
from webexteamssdk import WebexTeamsAPI
import meraki
import requests
import json
from datetime import datetime
import pytz
from flask_apscheduler import APScheduler


# Requirements
webex_bot_access_token = ''
webex_room = ''
meraki_api_key = ''
camera_serial = ''

# Flask, Webex and Meraki instantiations
app = Flask(__name__)
webex = WebexTeamsAPI(access_token=webex_bot_access_token)
dashboard = meraki.DashboardAPI(api_key=meraki_api_key, suppress_logging=True)

# Scheduler
scheduler = APScheduler()


# Webex Connect - Whatsapp
url = "https://api-sandbox.imiconnect.io/v1/whatsapp/messages"

headers = {
  'Authorization': '',
  'Content-Type': 'application/json'
}


# Flask Route
@app.route('/', methods=["GET", "POST"])
def button_press():  # put application's code here
    if request.method == "POST":
        print('Received POST')
        print(request.json)
        print(request.json['deviceName'])

        button_name = request.json['deviceName']
        button_serial = request.json['deviceSerial']
        device_url = request.json['deviceUrl']
        button_press_type = ''
        try:
            message = request.json['alertData']['message']
            button_press_type = request.json['alertData']['trigger']['button']['pressType']
            print(button_press_type)

        except KeyError:
            message = ''

        # Modifies Meraki Date
        time_stamp = request.json['sentAt']
        meraki_dashboard_time_stamp = datetime.strptime(time_stamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        ecuador_time_stamp = datetime.now(pytz.timezone('America/Guayaquil')).strftime('%Y-%m-%d %H:%M:%S')

        print(f'UTC time: {datetime.utcnow()}')
        print(f'Local Server/Laptop time: {datetime.now()}')
        print(f'Meraki Dashboard reported time: {meraki_dashboard_time_stamp}')
        print(f'Current time in Ecuador: {ecuador_time_stamp}')

        # Captures Camera Analytics
        camera_analytics = dashboard.camera.getDeviceCameraAnalyticsOverview(serial=camera_serial, timespan=43200)
        # print(camera_analytics)

        # Captures Snapshot from Meraki Camera
        image = dashboard.camera.generateDeviceCameraSnapshot(serial=camera_serial)
        camera_video_feed = dashboard.camera.getDeviceCameraVideoLink(serial=camera_serial)
        print(image)
        print(camera_video_feed)

        # Sends info to Webex Space
        if button_press_type == 'short':
            print('SHORT BUTTON PRESS')
            print('Sending Webex Message to Space')
            webex.messages.create(webex_room, markdown=f'Image taken at: {ecuador_time_stamp} (Hora de Ecuador)\n'
                                                       f'**{message}**\n'
                                                       f'Image received from Button: {button_name}\n'
                                                       f'Button serial: {button_serial}\n'
                                                       f'Button Device URL: {device_url}\n',
                                  files=[f'{image["url"]}']
                                  )
            # ADDS WEBEX CONNECT - Message to Whatsapp number\

            # payload_short_press = json.dumps({
            #     "from": "",
            #     "to": "",
            #     "contentType": "text",
            #     "content": f"Message sent using PYTHON: {message}, Image: {image['url']}"
            # })
            # print('Sending Whatsapp Message')
            # whatsapp_message_short_press = requests.request("POST", url, headers=headers, data=payload_short_press)
            # print(whatsapp_message_short_press.text)

            # api_de_luis = requests.request("post", )

            return 'Meraki Button - Short press'

        elif button_press_type == 'long':
            print('LONG BUTTON PRESS')
            webex.messages.create(webex_room, markdown=f'Long Button Pressed at: {ecuador_time_stamp} (Hora de Ecuador)\n'
                                                       f'**{message}**\n'
                                                       f'Received from Button: {button_name}\n'
                                                       f'Button serial: {button_serial}\n'
                                                       f'Button Device URL: {device_url}\n'
                                                       f'Video Feed URL: {camera_video_feed["url"]}\n'
                                  )
            return 'Meraki Button - Long Press'

        else:
            print('TESTS MERAKI DASHBOARD WEBHOOK')
            return 'Meraki Button - Webhook Test'

    print('Received GET')
    return 'Get Received'


def post_meraki_analytics():
    print('Meraki Analytics: ')
    ecuador_time_for_analytics = datetime.now(pytz.timezone('America/Guayaquil')).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Daily Report: {ecuador_time_for_analytics}")
    camera_analytics = dashboard.camera.getDeviceCameraAnalyticsOverview(serial=camera_serial, timespan=43200)
    print(camera_analytics)
    webex.messages.create(roomId=webex_room, text='SCHEDULED MESSAGE \n'
                                                  f'Date-Time {ecuador_time_for_analytics}\n'
                                                  f'Camera Analytics from device: {camera_serial}\n'
                                                  f'Camera Analytics for the last 12 Hours\n'                                                  
                                                  f'Camera Analytics - People Count: {camera_analytics[0]["entrances"]}')


if __name__ == '__main__':
    scheduler.add_job(id='Get Meraki Analytics',
                      func=post_meraki_analytics,
                      trigger='cron',
                      day_of_week='mon-sun', hour=17, minute=0)
    scheduler.start()
    app.run(port=8080)
