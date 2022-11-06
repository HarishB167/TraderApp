import os
from getpass import getpass

import requests as rqs

from . import constants, utils

class Login:

    def twofa(self, user_id, request_id, twofa_type="app_code", skip_session=None):
        print("Making TWO FA request")
        twofa_value = input("Enter app code : ")
        print("Request id : ", request_id)
        r = rqs.post(constants.ZERODHA_TWOFA_URL, data={'user_id': user_id, 'request_id': request_id, "twofa_value": twofa_value, "twofa_type": twofa_type, 'skip_session': ""})
        print("Response : ", r.json()['status'])
        return r

    def login(self):
        id = input("Enter user id : ")
        u_pass = getpass("Enter password : ")
        print("Id is : ", id)
        r = rqs.post(constants.ZERODHA_LOGIN_URL, data={'user_id': id, 'password': u_pass})
        print("Response : ", r.json()['status'])
        
        if r.status_code == 200:
            data = r.json()
            request_id = data['data']['request_id']
            r2 = self.twofa(id, request_id)
            self.save_enctoken(r2.cookies['enctoken'])
            self.save_user_id(id)
            return r, r2
        return None, None

    def save_enctoken(self, enctoken):
        print("Saving enctoken : ", enctoken)
        utils.save_broker_data("enctoken", enctoken)

    def save_user_id(self, user_id):
        utils.save_broker_data("user_id", user_id)
