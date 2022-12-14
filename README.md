# gve_devnet_meraki_button_snapshot
Use a Meraki MT30 button to take a snapshot from a specific Meraki MV Camera and send the picture or the video to a Webex Teams Space.

## Contacts
* Max Acquatella

## Solution Components
* Meraki MT30
* Meraki MV
* Webex Teams

## Related Sandbox Environment
This PoV requires a valid Meraki and Webex Organizations (a Webex connect sandbox is optional). In this regard, we assume that there is 
a valid Meraki MV30 button registered and two modes enabled: one for short press and one for long press, as well as at
least one Meraki MV Camera (Sense enabled). For Webex teams, we require a Webex Space (Space ID) and the creation of a BOT (see 
Webex BOT documentation). In order to enable Webhook communication, please install and enable NGROK. The following links 
will help you with the requirements. 

### Cisco Meraki
#### Meraki Button: 
* Meraki API Key:
Go to the TOP-Right corner of Meraki Dashboard, click your username, select "my profile" and scroll down to "API access". Save the API Key for the script requirements (to be assigned to meraki_api_key)
* Meraki MT30 Button Installation:
https://documentation.meraki.com/MT/MT_Installation_Guides/MT30_Installation_Guide_-_Smart_Automation_Button
* Meraki Dashboard Sensor configuration:
https://documentation.meraki.com/MT/MT_General_Articles/MT_Automation_Builder
* Meraki Camera and Sense:
To get the Camera Serial number (to be assigned to camera_serial): In Dashboard, go to Camera>Camera> Select your Camera and then click "Network". The Serial Number will be located on the Left of the Screen.
To enable Sense: In Dashboard for to Camera>Camera> Select your Camera go to "Settings", Select "Sense" and on "Sense API" click Enable. 
NOTE: Not all Meraki Cameras are enabled for Sense. Sense is a licensed feature. 

### Cisco Webex Teams
#### Webex Teams BOT:
* Create a Webex BOT and get a Token (to be assigned to webex_bot_access_token):
https://developer.webex.com/docs/bots
* Create a ROOM/Space and add the BOT
* Get ROOM/Space ID (to be assigned to webex_room):
https://developer.webex.com/docs/api/v1/rooms/list-rooms

### NGROK
* Register, Install and run NGROK:
https://ngrok.com/
* NOTE: Generate an AUTH Token, you will need it for the integration with the Meraki Dashboard.
* URL for NGROK Auth Token: https://dashboard.ngrok.com/get-started/your-authtoken


## Installation/Configuration
NOTE: The following instructions apply to macOS.

### Prepare Environment/Code
#### Clone this code
```bash
git clone https://wwwin-github.cisco.com/gve/gve_devnet_meraki_button_snapshot.git
```

#### Enable a Python Virtual environment
* On Windows: https://www.youtube.com/watch?v=APOPm01BVrk
* On MAC: https://www.youtube.com/watch?v=Kg1Yvry_Ydk&t=492s

#### Install requirements.txt
```bash
pip3 install -r requirements.txt
```

### Add the following requirements in app.py

```python
# Requirements
webex_bot_access_token = ''
webex_room = ''
meraki_api_key = ''
camera_serial = ''

```
NOTE: THIS IS SAMPLE CODE, it does not follow the best practices in regards to API Keys or password protection. 
These credentials are hardcoded in app.py THIS IS NOT RECOMMENDED.
THIS CODE IS NOT INTENDED TO BE USED IN PRODUCTION ENVIRONMENTS.

### Enable NGROK
```bash
ngrok http 8080
```
NOTE: The code uses port 8080, this can be changed in the app.py

### Add NGROK URL to Maraki Dashboard:
* Go to Network-wide>Alerts>Webhooks and copy the URL generated by NGROK and your NGROK AUTH Token. 
* IMPORTANT: This URL will change everytime you restart the NGROK process, this step has to be repeated EVERYTIME you re-start NGROK.

![/IMAGES/1image.png](/IMAGES/1image.png)

## Usage

### Run the Python Flask app

from the command line, run the code: 

```bash
python3 app.py
```

To Test the integration, in Dashboard go to Network-wide>Alerts>Webhooks. You can click "Send Test Webhook", 
if NGROK is enabled and the code is running, you should get a "delivered" message in Dashboard and the code should signal it as well in the command line:

```bash
TESTS MERAKI DASHBOARD WEBHOOK
```



### Test Meraki MT30 short and long press
Once the integration is verified, proceed to test the button presses

* Short Press case: It will take a snapshot and send the picture to the Webex Space. The code will generate the following command line message:
```bash
SHORT BUTTON PRESS
Sending Webex Message to Space
```
* Long Press case: It will send a link with the video feed from the camera and send it to the Webex Space. The code will generate the following command line message:
```bash
LONG BUTTON PRESS
127.0.0.1 - - [17/Oct/2022 11:17:46] "POST / HTTP/1.1" 200 -
```
NOTE: The messages delivered in the Webex Space can be modified and adapted to your own requirements. ALSO, it is possible to change the timezone as well.

### Test without Button
It is possible as well to test this integration using the "test automation" directly from Dashboard>Sensors>Automation

![/IMAGES/2image.png](/IMAGES/2image.png)

You should get similar messages in the Webex Space, but it wil miss certain information. 

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.