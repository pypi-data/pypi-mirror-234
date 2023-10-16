# VeilCord.
<img src="https://img.shields.io/pypi/v/veilcord?style=for-the-badge&logo=python">
<a href="https://github.com/imvast" target="_blank">
    <img alt="followers" src="https://img.shields.io/github/followers/imvast?color=f429ff&style=for-the-badge&logo=github&label=Follow"/>
</a>

```less
                > Custom Discord Tools Going To Be Used For My Projects
                      And Available To Anyone Else Who Wants To Use <
```


---

### Installation
```yaml
! package NOT FULLY available for commercial usage !
pip install veilcord
```

### Example Usages
```py
from veilcord import VeilCord

veilcord = VeilCord(
    session = None, # for custom tls_client sessions
    device_type = "browser", # types : browser, mobile, app (aka desktop)
    user_agent = None # for custom user agent
)
```

```py
# GETTING X-Super-Properties
xsup = veilcord.generateXProp()
print(f"(+) Retrieved XSup: {xsup}")
```

```py
# GETTING ALL THE COOKIES AND FINGERPRINT
fp, cookies = veilcord.getFingerprint(
    xsup, 
    withCookies = True, # true or false -- will return cookies that are returned in the expirements req
    cookieType = "json" # if withCookies is true this can be either "json" or "cookiejar"  -- by default its cookiejar
)
print(f"(+) Retrieved Fingerprint: {fp}")
print(f"(+) Retrieved Cookies: {cookies}")
# returns a tuple.  [0] - Fingerprint  |  [1] - COOKIESJAR or JSON
```

```py
# GET THE NEW SESSION ID BS  || this can also be used for websocket connection scroll down to see example

sessionID = veilcord.getSession(
    token = "",
)
print(f"(+) Got Session ID: {sessionID}")
```

```py
## Getting Discord build number

buildNum = VeilCord.getBuildNum()
print(buildNum)

# -- or with all the extra stats

buildNum, buildTS, url = VeilCord.getBuildNum(withStat=True)
print("URL:", url)
print("Build Number:", buildNum)
print("Build Timestamp:", buildTS)
```

#### Custom Sessions
```py
session = veilcord.openSession(
    custom_rpc = {
        "status": "online",
        "since": 0,
        "activities": [{
            "name": "Custom Status",
            "type": 4,
            "state": "vast#1337",
            "emoji": ""
        }],
        "afk": False
    }
)

veilcord.getSession(
    token = "", # obv the token
    session = session, # the session returned from veilcord.openSession()  (if u are using keepAlive)
    keep_alive = True,  # keep the session alive until closed with veilcord.closeSession()
    show_hb = True # prints when it sends the heartbeat and when the next one is
)

# close the session, if keepAlive is enabled.
veilcord.closeSession(session)
```

---

## * [imvast@discord](https://discord.com/users/1118654675898617891) | [imvast@github](https://github.com/imvast) | [vast.sh](https://vast.sh) *