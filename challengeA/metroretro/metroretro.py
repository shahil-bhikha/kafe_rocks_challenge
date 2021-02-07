#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 23:26:57 2021

@author: shahil
"""

import time
import requests

class metroretro:

    def __init__(self, username, passw):
        self.base_url = "https://metroretro.io"
        self.login_payload = {
            "email": username,
            "password": passw
        }

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
            "origin": self.base_url,
            "referer": self.base_url + "/login/email"
        }

    def connect(self):
        count = 0
        while count < 3:
            try:
                self.sess = requests.session()
                resp = self.sess.post(
                    self.base_url + "/login/email", data=self.login_payload, headers=self.headers)
            except requests.exceptions.Timeout:
                print("Timeout occured trying again in 5 mins")
                count += 1
                time.sleep(60*5)
                continue
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                print(e)
                break

            return resp.ok

    def getBoards(self, boardName):
        try:
            resp = self.sess.get(self.base_url + "/api/v1/boards?before=")
        except requests.exceptions as e:
            # catastrophic error. bail.
            print(e)
            return
        except Exception as e:
             print(e)
             return

        ID = ""
        for b in resp.json():
            if b["name"] == boardName:
                ID = b["id"]

        return ID

    def getBoardData(self, boardID, fileFormat):
        board_options = {
            "format": fileFormat,
            "dl": "1"
        }

        try:
            resp = self.sess.get(
                self.base_url + "/api/v1/boards/{0}/export".format(boardID), params=board_options)
        except requests.exceptions as e:
            # catastrophic error. bail.
            print(e)
            return

        return resp.text
