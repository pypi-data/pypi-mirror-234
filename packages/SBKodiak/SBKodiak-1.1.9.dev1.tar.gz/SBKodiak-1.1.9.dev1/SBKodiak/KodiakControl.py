"""
Python module to handle control of the Kodiak modules.

This class will also do all necessary interaction with underlying Database.

Author : Matt Holsey
Date : 09-05-2023
"""
import logging
import time
import os
import paramiko
import threading
from .sb_db import SimpleDB

from .kodiak_session_management import KodiakSession
from .KodiakGlobals import KodiakGlobals
from .kodiak_endpoints import *


"""
API KEY:
Name : mholsey
desc : mholsey test key
ID   : 

API Key : gThV9h4LQmmSiYFNTcjBuvoRPvEC3LpW
# The key is a 'secret key' so it would have to be generated once by the suer
"""


class KodiakControlClass:

    def __init__(self):

        # self.private_key = private_key if private_key else "gThV9h4LQmmSiYFNTcjBuvoRPvEC3LpW"
        self.db = SimpleDB(KodiakGlobals.database_name)

        # If the table doesn't already exist, then create a new one
        if not self.db.check_exists():
            self.db.create_table()

        self.kodiak_session = KodiakSession()

    def login(self, kw):
        """
        Login to the Kodiak

        Will attempt to log in and return the response received.

        If login was successful, it will also save these details to the database.

        :param kw: KodiakWrapper object containing the user's credentials

        :return: Boolean : True if the login worked, else False
        """

        # Attempt to log in
        response = self.kodiak_session.login(kw)

        # If there's nothing returned, then there was an error logging into the system
        if response:
            # Add the new session key
            self.db.update_kodiak_db_session_key(kw.ipaddress, response['session_token'], response['refresh_token'])
            return True
        else:
            return False

    # def refresh(self, kw):
    #     """
    #     Attempt to refresh the module's login.
    #
    #     :param kw: Kodiak wrapper containing credentials
    #
    #     :return: boolean: True if success, else False
    #     """
    #
    #     # Check if the kodiak module present in database
    #     response = self.db.get_kodiak_db(kw.ipaddress)
    #     if response:
    #         # Attempt to refresh the module's login
    #         refresh_response = self.kodiak_session.refresh_login(kw, response[6], response[3])
    #         if refresh_response:
    #             # Update the database with the new refresh / session tokens
    #             self.db.update_kodiak_db_session_key(kw.ipaddress, refresh_response['session_key'],
    #                                                  refresh_response['refresh_token'])
    #             return True
    #     else:
    #         return False

    def check_user_exists(self, kw):
        """
        Function to get a list of kodiak users and check if the standard SB one exists

        :param kw: Kodiak Wrapper
        :return: boolean - true if the sb user exists, else false
        """

        # Getting the list of users from /users
        users = self.kodiak_session.get_users(kw)
        # Standard sb user is in globals, check if string in string
        if KodiakGlobals.my_kodiak_user in str(users):
            return True

        return False

    def create_user(self, kw):
        """
        Checking and creating users on the Kodiak Module.
        This will get the user and update the database on this system with that user

        :param kw: Kodiak Wrapper

        :return: boolean : True if success, else false.
        """

        # Check if Module in DB
        db_response = self.db.get_kodiak_db(kw.ipaddress)
        if db_response:
            # check if there`s a user assigned to the kodiak, if not, create one
            if not db_response[1]:
                # if not self.check_user_exists(kw):
                created_user = self.kodiak_session.post_add_users(kw)
                print(created_user)

                self.db.update_kodiak_db_kodiak_user(kw.ipaddress, KodiakGlobals.my_kodiak_user)
                self.db.update_kodiak_db_kodiak_password(kw.ipaddress, KodiakGlobals.my_kodiak_pass)

            return True

        else:
            # return false if we couldn`t create one
            return False

    def lock(self, kw, lock_name):
        """
        Attempts to lock the Kodiak Module

        :param kw: Kodiak Wrapper
        :param lock_name: Lock name to be used for lock

        :return: boolean : True if success, else false.
        """

        # Check if Module in DB
        db_response = self.db.get_kodiak_db(kw.ipaddress)
        if db_response:
            # Attempt to lock the module
            # lock_response = self.kodiak_session.lock(kw, lock_name, db_response[4])
            lock_response = self.kodiak_session.lock(kw, lock_name, None)
            if lock_response:
                # Use the 'lock_key' response and update the DB with the key.
                self.db.update_kodiak_db_lock_key(kw.ipaddress, lock_response)
                return True
        else:

            return False

    def unlock(self, kw):
        """
        Attempt to unlock the module.

        :param kw: Kodiak wrapper containing credentials

        :return: boolean: True if success, else False
        """

        # Check if the kodiak module present in database
        response = self.db.get_kodiak_db(kw.ipaddress)
        if response:
            # Attempt to unlock the module based off of the current items in the DB
            if self.kodiak_session.unlock(kw, response[-1], response[4]):
                return True

        else:
            return False

    def get_lock_status(self, kw):
        """
        Function to get the current lock status of the kodiak module

        :param kw: Kodiak Wrapper containing credentials

        :return: Lock status or None if no response
        """
        response = self.db.get_kodiak_db(kw.ipaddress)
        if response:
            # Attempt to refresh the module's login
            lock_status = self.kodiak_session.get_lock_status(kw, response[4])
            return lock_status
        else:
            return None

    def stop(self, kw):
        """
        Sending a POST request to stop the Kodiak capture

        :return: True if success, False if fail
        """

        query_response = self.db.get_kodiak_db(kw.ipaddress)
        if not query_response:
            logging.warning("Couldn't find kodiak login in database, have you logged into the module yet?")
            return False

        message_to_send = {
            "lock_key": query_response[-1]
        }
        headers = {
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_stop

        # A post request to the API
        response = self.kodiak_session.send_post_command(message_to_send, endpoint, headers)

        if 'error' in response:
            return False

        return True

    def start(self, kw, trigger=False):
        """
        Sending a POST request to start the kodiak capture

        :return: Return true if start succeeded, else False
        """

        query_response = self.db.get_kodiak_db(kw.ipaddress)
        if not query_response:
            logging.warning("Couldn't find kodiak login in database, have you logged into the module yet?")
            return False

        message_to_send = {
            "channels": [
                {
                    "name": "dn.0",
                    "type": "data",
                    "capture": {
                      "buffer": {
                        "limit": 1075497471,
                        "post_trigger": 0,
                        "trigger_position": 100
                      },
                      "lane_control": None,
                      "speed_control": "auto",
                      "transceiver_control": {
                        "equalisation": "auto",
                        "sris": False
                      },
                      "tlp_truncation": 0
                    },
                    "prefilter": {
                      "dllp": {
                        "initfc1": True,
                        "initfc2": True,
                        "updatefc": True
                      },
                      "os": {
                        "skp": True,
                        "cskp": True
                      }
                    }
                },
                {
                    "type": "data",
                    "name": "up.0",
                    "capture": {
                        "buffer": {
                            "limit": 1075497471,
                            "post_trigger": 0,
                            "trigger_position": 100
                        },
                        "lane_control": {
                            "assignment": {
                                "mode": "manual",
                                "lanes": [
                                    0,
                                    1,
                                    3,
                                    2,
                                    4,
                                    5,
                                    6,
                                    7,
                                    8,
                                    9,
                                    10,
                                    11,
                                    12,
                                    13,
                                    14,
                                    15
                                ]
                            },
                            "lane_polarity": [
                                None,
                                None,
                                None,
                                None,
                                True,
                                True,
                                True,
                                True,
                                False,
                                False,
                                False,
                                False,
                                None,
                                None,
                                None,
                                None
                            ]
                        },
                        "speed_control": "gen5",
                        "transceiver_control": {
                            "equalisation": "dfe",
                            "sris": True
                        },
                        "tlp_truncation": 0
                    },
                    "prefilter": {
                        "dllp": {
                            "initfc1": True,
                            "initfc2": True,
                            "updatefc": True
                        },
                        "os": {
                            "skp": True,
                            "cskp": True
                        }
                    }
                }
            ],

            "mode": "trigger" if trigger else "manual",
            "lock_key": query_response[-1],
            # "lock_key": KodiakGlobals.lock_name,
        }

        # If we want to trigger the kodiak module, then add the SB_trigger definition in.
        if trigger:
            message_to_send['trigger'] = {
                "resources": {
                    "counters": [],
                    "timers": []
                },
                "start": [
                    "State 0"
                ],
                "states": [
                    {
                        "conditions": [
                            {
                                "fields": [
                                    {
                                        "mask": 255,
                                        "match": 68,
                                        "offset": 0
                                    },
                                    {
                                        "mask": 15,
                                        "match": 1,
                                        "offset": 3
                                    },
                                    {
                                        "mask": 240,
                                        "match": 0,
                                        "offset": 7
                                    },
                                    {
                                        "mask": 15,
                                        "match": 0,
                                        "offset": 10
                                    },
                                    {
                                        "mask": 252,
                                        "match": 0,
                                        "offset": 11
                                    },
                                    {
                                        "mask": 255,
                                        "match": 227,
                                        "offset": 12
                                    },
                                    {
                                        "mask": 255,
                                        "match": 26,
                                        "offset": 13
                                    }
                                ],
                                "type": "tlp_data"
                            }
                        ],
                        "name": "State 0",
                        "onMatch": [
                            {
                                "type": "trigger"
                            }
                        ]
                    }
                ]
            }

        headers = {
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_start

        # A post request to the API
        response = self.kodiak_session.send_post_command(message_to_send, endpoint, headers)

        if 'error' in response:
            return False

        return True

    def get_module_status(self, kw):
        """
        Send a GET request to the Kodiak to see its current lock status.

        :return: Response from get lock stats request
        """

        query_response = self.db.get_kodiak_db(kw.ipaddress)

        headers = {
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_status

        # Do the get request to lock endpoint
        response = self.kodiak_session.send_get_request(endpoint, headers)

        return response

    def locate_kodiak_port(self, kw, remote_ip=None):
        """
        Go through and trigger the SB system to trigger the Analyser that should be running.
        :return:
        """

        ssh = None

        # If there's a remote IP specified, use this, else just execute the command on the current system.
        if remote_ip:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(remote_ip, 22, username='root', password='sb')

        for x in range(16):
            index = x
            if len(str(index)) < 2:
                index = "0" + str(index)

            os_cmd = f'sbecho trigger=1{x} > /proc/vlun/nvme'

            if remote_ip:
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(os_cmd)
            else:
                os.system(os_cmd)

            time.sleep(0.05)

            response = self.get_module_status(kw)

            if response:
                if 'error' not in response:

                    if response[0]['triggered']:
                        # Adding the port located to the database.
                        self.db.insert_kodiak_db_standard(kw.ipaddress, x)
                        return response[0]['triggered']

        return None

    def start_auto_locate_port(self, kw):
        # self.login(kw)
        self.db.insert_kodiak_db_standard(kw.ipaddress, kw.key)

        # kw.username = KodiakGlobals.my_kodiak_user
        # kw.password = KodiakGlobals.my_kodiak_pass

        # if not self.login(kw):
        #     self.create_user(kw)
        #
        # if not self.login(kw):
        #     return False

        self.lock(kw, 'SB_LOCK')
        started = self.start(kw, trigger=True)
        # self.db.update_kodiak_db_kodiak_port(kw.ipaddress, "null")
        thread = threading.Thread(target=self.locate_kodiak_port, args=(kw, '192.168.1.160', ))
        thread.start()
        return started


class KodiakWrapper:
    def __init__(self, kodiak_ip_address, username, password, private_key):
        self.password = password
        self.username = username
        self.key = private_key
        self.ipaddress = kodiak_ip_address
