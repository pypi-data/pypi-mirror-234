#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: github.com/imvast
@Date: 7/31/2023
"""

from .__session__ import SessionManager

from base64       import b64encode
from json         import dumps
from tls_client   import Session
from typing       import Optional, Literal, List, Union, Tuple
from json         import dumps
from time         import time
from requests     import get
from re2          import search, findall
from asyncio      import run


# def timeit(func): # debugging
#     def wrapper(*args, **kwargs):
#         start_time = time()
#         result = func(*args, **kwargs)
#         end_time = time()
#         execution_time = end_time - start_time
#         print(f"Function '{func.__name__}' took {execution_time:.6f} seconds to execute.")
#         return result
#     return wrapper


class HTTPClient:
    def __init__(self):
        self.session = Session(client_identifier="firefox_115", random_tls_extension_order=True)


class VeilCord:
    def __init__(
        self,
        session:        Optional[Session] = HTTPClient().session,
        device_type:    Literal["browser", "mobile", "app"] = "browser",
        user_agent:     Optional[str] = None,
        device_version: Optional[str] = None,
        build_num:      Optional[int] = None
    ) -> None:
        self.session = HTTPClient().session if session is None else session
        self.user_agent_browser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        self.user_agent_mobile = "Discord-Android/170014;RNA"
        self.user_agent_app = (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9016 Chrome/108.0.5359.215 Electron/22.3.12 Safari/537.36"
        )
        self.device_type_browser = "Windows"
        self.device_type_mobile  = "Android"
        
        self.currentBuildNUM = VeilCord.getBuildNum() if not build_num else build_num
        self.currentCapNum = VeilCord.getCapabilitiesNum()

        if device_type == "browser":
            self.device_type = "browser"
            self.user_agent = self.user_agent_browser if user_agent is None else user_agent
        elif device_type == "mobile":
            self.device_type = "mobile"
            self.user_agent = self.user_agent_mobile if user_agent is None else user_agent
        elif device_type == "app":
            self.device_type = "app"
            self.user_agent = self.user_agent_app if user_agent is None else user_agent
        else:
            raise ValueError("An invalid device_type was provided. Acceptable values: ['browser', 'mobile', 'app']")
        
        if user_agent:
            browser_patterns = {
                "Discord Client": r"discord/([\d.]+)",
                "Chrome": r"Chrome/([\d.]+)",
                "Firefox": r"Firefox/([\d.]+)",
                "Edge": r"Edge/([\d.]+)",
                "Safari": r"Safari/([\d.]+)",
                "Opera": r"OPR/([\d.]+)|Opera/([\d.]+)"
            }
            
            for browser, pattern in browser_patterns.items():
                match = search(pattern, user_agent)
                if match:
                    self.browser = str(browser)
                    self.bversion = str(match.group(1))
        else:
            self.browser = "Firefox"
            self.bversion = device_version if device_version else "115.0"
        
        
    # session mg
        
    def openSession(self, custom_rpc: dict = None):
        session_manager = SessionManager(
            self.user_agent, 
            self.currentBuildNUM,
            self.device_type, 
            self.currentCapNum,
            custom_rpc
        )
        return session_manager
        
    def getSession(
        self,
        token: str,
        session: SessionManager = None,
        keep_alive: bool = False, 
        show_hb: bool = False
    ) -> Union[str, None]:
        if session is None:
            session = SessionManager(self.user_agent, self.currentBuildNUM, self.device_type, self.currentCapNum)
            if keep_alive:
                raise SyntaxError("Session cannot be null with keepAlive enabled.")
        session_id = run(session.get_session(token, keep_alive, show_hb))
        return session_id

    def closeSession(self, session):
        session.close_session()
        return True
    

    
    def generateXProp(
        self,
        browser_vers: Optional[str] = None,
        build_num:    Optional[int] = None
    ):
        if self.device_type == "mobile":
            xsup = {
                "os": self.device_type_mobile,
                "browser": "Discord Android",
                "device": "RMX2117L1",
                "system_locale": "en-US",
                "client_version": "177.21 - rn",
                "release_channel": "googleRelease",
                "device_vendor_id": "c3c29b3e-4e06-48ff-af49-ec05c504c63e",
                "os_version": "31",
                "client_build_number": 1750160087099,
            }
        elif self.device_type == "browser":
            xsup = {
                "os": self.device_type_browser,
                "browser": self.browser,
                "device": "",
                "system_locale": "en-US",
                "browser_user_agent": self.user_agent,
                "browser_version": self.bversion,
                "os_version": "10",
                "release_channel": "stable",
                "client_build_number": build_num if build_num else self.currentBuildNUM,
            }
        elif self.device_type == "app":
            xsup = {
                "os": self.device_type_browser,
                "browser": "Discord Client",
                "release_channel": "stable",
                "client_version": browser_vers if browser_vers else "1.0.9016",
                "os_version": "10.0.22621",
                "os_arch": "x64",
                "system_locale": "en-US",
                "browser_user_agent": self.user_agent,
                "browser_version": "22.3.2",
                "client_build_number": build_num if build_num else self.currentBuildNUM,
                "native_build_number": 35236
            }
        else:
            raise ValueError("An invalid type for generateXProp() was provided. Acceptable values: ['browser', 'mobile', 'app']")
        
        xsup["client_event_source"] = None
        xsup["referrer"] = ""
        xsup["referring_domain"] = ""
        xsup["referrer_current"] = ""
        xsup["referring_domain_current"] = ""
        
        return b64encode(dumps(xsup, separators=(',', ':')).encode()).decode()


    def getFingerprint(
        self,
        xsup: Optional[str] = None,
        withCookies: Optional[bool] = True,
        cookieType: Literal["json", "cookiejar"] = "cookiejar",
        custom_headers: dict = None
    ) -> Union[str, List[str]]:
        if not xsup:
            xsup = self.generateXProp()
        if self.device_type == "mobile":
            headers = {
                'Host': 'discord.com',
                'X-Super-Properties': xsup,
                'Accept-Language': 'en-US',
                'X-Discord-Locale': 'en-US',
                'X-Debug-Options': 'bugReporterEnabled',
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json',
            } if not custom_headers else custom_headers
        elif self.device_type == "browser":
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.5",
                "connection": "keep-alive",
                "host": "discord.com",
                "referer": "https://discord.com/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": self.user_agent,
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-super-properties": xsup
            } if not custom_headers else custom_headers
        elif self.device_type == "app":
            headers = {
                "authority": "discord.com",
                "accept": "*/*",
                "accept-language": "en-US",
                "connection": "keep-alive",
                "content-type": "application/json",
                "origin": "https://discord.com",
                "referer": "https://discord.com/",
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                "user-agent": self.user_agent,
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-discord-timezone": "America/New_York",
                "x-super-properties": xsup,
            } if not custom_headers else custom_headers
        else:
            raise ValueError("An invalid type for getFingerprint() was provided. Acceptable values: ['browser', 'mobile', 'app']")
        response = self.session.get('https://discord.com/api/v9/experiments', headers=headers)
        if withCookies:
            cookies = response.cookies if cookieType == "cookiejar" else dumps(response.cookies.get_dict())
            return response.json().get("fingerprint"), cookies
        return response.json().get("fingerprint")


    # non self #
    def getBuildNum() -> int:
        try:
            res = get("https://discord.com/login").text
            bn_file = "https://discord.com/assets/{}.js".format(compile(r'assets/+([a-z0-9]+)\.js').findall(res)[-2])
            bn_res = get(bn_file).text
            bn_index = bn_res.find('buildNumber')+24
            BUILD_NUM = int(bn_res[bn_index:bn_index+6])
            return BUILD_NUM
        except:
            return 225093

    def getCapabilitiesNum() -> int:
        return 16381
        try:
            cookie = {
                "OptanonConsent": "isIABGlobal=false&datestamp=Thu+Jul+27+2023+21%3A05%3A10+GMT-0400+(Eastern+Daylight+Time)&version=6.33.0&hosts=&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1",
            }

            resp_welcome = get("https://discord.com/welcome/", cookies=cookie)
            script_links = findall(r'<script[^>]+src="([^"]+)"', resp_welcome.text)
            last_script_link = script_links[-1]

            resp_script = get("https://discord.com" + last_script_link)
            script_content = resp_script.text

            cappattern = r'capabilities:(\d+)'
            match = search(cappattern, script_content)

            return int(match.group(1)) if match else 16381
        except:
            return 16381  # last known

    def extractCode(invite) -> Union[str, None]:
        """Extracts the invite code from a Discord invite link"""
        code_regex = r"(?:(?:http:\/\/|https:\/\/)?discord\.gg\/|discordapp\.com\/invite\/|discord\.com\/invite\/)?([a-zA-Z0-9-]+)"
        match = search(code_regex, invite)
        if match:
            try:
                return match.group(1)
            except:
                return match.group(0)
        else:
            return None
        



## out of the class for old projects use

def extractCode(invite):
    return VeilCord.extractCode(invite=invite)