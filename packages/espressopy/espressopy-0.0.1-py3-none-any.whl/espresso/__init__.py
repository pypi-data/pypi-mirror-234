import requests as r
import time
import json
import os
import logging
import espresso.config

logging.basicConfig(level=logging.DEBUG)

burl = "https://discord.com/api/v10"

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class member:
    @staticmethod
    def ban(uid, gid, reason, unix):
        token = espresso.config.token
        pl = {
            "delete_message_seconds": unix
        }
        h = {
            "Authorization": token,
            "X-Audit-Log-Reason": reason
            "Content-Type": "application/json"
        }
        url = burl + f"/guilds/{gid}/bans/{uid}"
        req = r.put(url, headers=h, json=pl)
        if req.status_code == 204:
            return json.stringify({"success":True})
        elif req.status_code == 403:
            print(f"{Color.BOLD}{Color.YELLOW}WARN: Trouble banning member due to permissions issue at guild {gid}, user id {uid}{Color.RESET}")
            return json.dumps({"success":False, "message":"Cannot ban member due to permissions issue."})
        else:
            print(f"{Color.BOLD}{Color.RED}ERROR: Trouble while banning member at guild {gid}, user id {uid}{Color.RESET}")
            return json.dumps({"success":False, "message":"Failed to ban member for unknown reason."})
        
        def kick(uid, gid, reason):
            token = espresso.config.token
            h = {
                "Authorization": token,
                "X-Audit-Log-Reason": reason,
                "Content-Type": "application/json"
            }
            url = burl + f"/guilds/{gid}/members/{uid}"
            req = r.delete(url, headers=h)
            if req.status_code == 204:
                return json.stringify({"success":True})
            elif req.status_code == 403:
                print(f"{Color.BOLD}{Color.YELLOW}WARN: Trouble kicking member due to permissions issue at guild {gid}, user id {uid}{Color.RESET}")
                return json.dumps({"success":False, "message":"Cannot kick member due to permissions issue."})
            else:
                print(f"{Color.BOLD}{Color.RED}ERROR: Trouble while kicking member at guild {gid}, user id {uid}{Color.RESET}")
                return json.dumps({"success":False, "message":"Failed to kick member for unknown reason."})

