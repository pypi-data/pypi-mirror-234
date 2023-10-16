# THIS ISNT AVAILABLE PUBLICALLY YET UNLESS YOU KNOW HOW TO RUN IT WITHOUT HELP

from time       import sleep, time
from tls_client import Session
from requests   import post, get, exceptions
from terminut   import log

available = ["CAPSOVLER", "ANTICAPTCHA", "CAPBYPASS", "CAPMONSTER", "HCOPTCHA", "CAPGURU", "24CAP"]

class Solver:
    def __init__(
        self,
        session: Session,
        service: available = "CAPSOLVER",
        capKey: str = None,
        siteKey: str = "4c672d35-0701-42b2-88c3-78380b0db560",
        siteUrl: str = "https://discord.com",
        rqData: str = None,
        user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    ):
        self.valid_services = {
            "CAPSOLVER": "https://api.capsolver.com",
            "ANTICAPTCHA": "https://api.anti-captcha.com",
            "CAPBYPASS": "https://api.capbypass.com",
            "CAPMONSTER": "https://api.capmonster.cloud"
            # will add more later
        }
        self.session = session
        self.service = service
        self.capKey  = capKey
        self.siteKey = siteKey
        self.siteUrl = "https://" + siteUrl if "http" not in siteUrl else siteUrl
        self.rqData  = rqData
        self.ua      = user_agent
        
        if not capKey:
            raise ValueError("A captcha service key is required in order to solve the captcha :/")
        
    def solveCaptcha(self) -> str:
        if self.service in self.valid_services:
            domain = self.valid_services[self.service]
            return self.solveGeneric(domain)
        elif self.service == "HCOPTCHA":
            return self.solveHCOP(domain="https://api.hcoptcha.online/api")
        elif self.service == "CAPGURU":
            return self.solveSecondary("http://api.captcha.guru")
        elif self.service == "24CAP":
            return self.solveSecondary("https://24captcha.online")
        else:
            raise ValueError(f"Invalid captcha service  |> {available}")
    
    def solveGeneric(self, domain: str) -> str:
        try:
            taskType = "HCaptchaTurboTask" if "capsolver" in domain else "HCaptchaTask"
            data1 = {
                "clientKey": self.capKey,
                "task": {
                    "type": taskType,
                    "websiteURL": self.siteUrl,
                    "websiteKey": self.siteKey,
                    "enterprisePayload": {
                        "rqdata": self.rqData
                    } if self.rqData else None,
                    "userAgent": self.ua,
                    "proxy": self.getProxyFromSession(self.session)
                }
            }
            resp1 = post(f"{domain}/createTask", json=data1)
            
            invalid_errs = ["ERROR_KEY_DENIED_ACCESS", "ERROR_KEY_DOES_NOT_EXIST", "ERROR_ZERO_BALANCE"]
            if any(error_name in resp1.text for error_name in invalid_errs):
                return log.error("Invalid Captcha Service Key!")
            
            if resp1.json().get("errorId") == 0:
                taskId = resp1.json().get("taskId")
                data = {
                    "clientKey": self.capKey,
                    "taskId": taskId
                }
                resp = post(f"{domain}/getTaskResult", json=data)
                status = resp.json().get("status")

                while status == "processing":
                    sleep(1)
                    resp = post(f"{domain}/getTaskResult", json=data)
                    status = resp.json().get("status")

                if status == "ready":
                    return resp.json().get("solution").get("gRecaptchaResponse")
                else:
                    return self.solveCaptcha()
            else:
                return self.solveGeneric(domain)
        except exceptions.ConnectionError:
            return self.solveGeneric(domain)

    def solveHCOP(self, domain: str) -> str:
        taskType = "hcaptchaEnterprise"
        data1 = {
            "api_key": self.capKey,
            "task_type": taskType,
            "data": {
                "host": (self.siteUrl.replace("https://", "")),
                "sitekey": self.siteKey,
                "useragent": self.ua,
                "proxy": Solver.getProxyFromSession(self.session, 1)
            }
        }
        resp1 = post(f"{domain}/createTask", json=data1, timeout=60)
        
        if "Wrong API key" in resp1.text: 
            return log.error("Invalid Captcha Service Key!")
        
        if not resp1.json().get("error"):
            taskId = resp1.json().get("task_id")
            data = {
                "api_key": self.capKey,
                "task_id": taskId
            }
            resp = post(f"{domain}/getTaskData", json=data, timeout=60)
            status = resp.json().get("task").get("state")

            while status == "processing":
                sleep(1)
                resp = post(f"{domain}/getTaskData", json=data, timeout=60)
                status = resp.json().get("task").get("state")

            if status == "completed":
                return resp.json().get("task").get("captcha_key")
            else:
                return self.solveCaptcha()
        else:
            return self.solveHCOP(domain)
        
    
    def solveSecondary(self, domain: str):
        payload = {
            "key": self.capKey,
            "method": "hcaptcha",
            "sitekey": self.siteKey,
            "pageurl": self.siteUrl,
            "userAgent": self.ua,
            "json": 1
        }

        res = post(f"{domain}/in.php", json=payload)
        
        if "ERROR_WRONG_USER_KEY" in res.text: 
            return log.error("Invalid Captcha Service Key!")

        payload = {
            "key": self.capKey,
            "action": "get",
            "id": f"{res.json().get('request')}",
            "json": 1
        }
        res = post(f"{domain}/res.php", json=payload)
        while res.json().get("request") == "CAPCHA_NOT_READY":
            res = post(f"{domain}/res.php", json=payload)
            sleep(1)
            
        return res.json().get("request")
        

    
    @staticmethod
    def getProxyFromSession(session: Session, t=0) -> str:
        protocol, sessionProxy = session.proxies.get("http").split("://")
        sessionProxy = sessionProxy.replace(":", "vast on top").replace("@", "vast on top")
        if len(sessionProxy.split("vast on top")) == 4:
            user, password, host, port = sessionProxy.split("vast on top")
            if t == 1:
                return f"{user}:{password}@{host}:{port}"
            return f"{protocol}:{host}:{port}:{user}:{password}"
        else:
            host, port = sessionProxy.split("vast on top")
            if t == 1:
                return f"{host}:{port}"
            return f"{protocol}:{host}:{port}"