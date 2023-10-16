login_response_good = {
    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLXJlZnJlc2giOnRydWUsIlgtdXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTY5MzkyNDQyNCwiaWF0IjoxNjkzMzE5NjI0fQ.0tHMvgn7C1Tpd9udlYIEdjE61ZXC90uVTNvPdgbi4lQ',
    'session_token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLWRpc3BsYXluYW1lIjoiQWRtaW5pc3RyYXRvciIsIlgtcHJpdmlsZWdlcyI6WyJMb2dpbiIsIkNvbmZpZ3VyZVNlbGYiLCJSZWFkTWVkaWEiLCJDb25maWd1cmVNZWRpYSIsIlJlYWRVc2VyIiwiQ29uZmlndXJlVXNlciIsIkNvbmZpZ3VyZVN5c3RlbSIsIkNvbmZpZ3VyZUZpcm13YXJlIiwiQ29uZmlndXJlQ2FwdHVyZSIsIlJlYWREZXZpY2UiLCJSZWFkVHJhY2UiLCJDb25maWd1cmVUcmFjZSIsIkNvbmZpZ3VyZVN0b3JlIl0sIlgtdXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTY5MzMyMTQyNCwiaWF0IjoxNjkzMzE5NjI0fQ.gQP-ZRFpEBKKXHpsF9lRe3UQvG0CRmylsbA-IH9EI6Y"

}

login_response_bad = {
  "error": {
    "code": "InvalidCredentials",
    "data": None,
    "message": "The provided credentials are invalid"
  }
}


refresh_login_responses = {
    'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLXJlZnJlc2giOnRydWUsIlgtdXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTY5MzkyNDQyNCwiaWF0IjoxNjkzMzE5NjI0fQ.0tHMvgn7C1Tpd9udlYIEdjE61ZXC90uVTNvPdgbi4lQ',
    'session_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJYLWRpc3BsYXluYW1lIjoiQWRtaW5pc3RyYXRvciIsIlgtcHJpdmlsZWdlcyI6WyJMb2dpbiIsIkNvbmZpZ3VyZVNlbGYiLCJSZWFkTWVkaWEiLCJDb25maWd1cmVNZWRpYSIsIlJlYWRVc2VyIiwiQ29uZmlndXJlVXNlciIsIkNvbmZpZ3VyZVN5c3RlbSIsIkNvbmZpZ3VyZUZpcm13YXJlIiwiQ29uZmlndXJlQ2FwdHVyZSIsIlJlYWREZXZpY2UiLCJSZWFkVHJhY2UiLCJDb25maWd1cmVUcmFjZSIsIkNvbmZpZ3VyZVN0b3JlIl0sIlgtdXNlcm5hbWUiOiJhZG1pbiIsImV4cCI6MTY5MzMyMTYxNywiaWF0IjoxNjkzMzE5ODE3fQ.seRFatv_Rq6oSRaKiosvWP64Z58IVWADReVAdSTdyZ4'
}

refresh_login_response_bad = {
  "error": {
    "code": "UnhandledException",
    "data": {
      "exception": "signature format is incorrect"
    },
    "message": "An exception occurred that was not handled"
  }
}


lock_response_bad = {"error":
                         {"code": "LockError",
                          "data":
                              {"accessed": "2023-08-28T19:50:37+0000",
                               "acquired": "2023-08-28T19:50:37+0000",
                               "lock_owner": "Administrator"},
                          "message": "The analyser is currently locked"
                          }
                     }

lock_response_bad2 = {"error":
                          {'code': 'LockError',
                           'data':
                               {'accessed': '2023-08-29T15:27:19+0000',
                                'acquired': '2023-08-29T15:27:19+0000',
                                'lock_owner': 'Live Trace'},
                           'message': 'The analyser is currently locked'
                           }
                      }

lock_response_good = {"accessed": "2023-08-29T15:37:43+0000",
                      "acquired": "2023-08-29T15:37:43+0000",
                      "id": "H+DBL3Lj",
                      "key": "rsaHohL9",
                      "lock_name": "Administrator",
                      "owner": "Administrator"
                      }

lock_status_good = {'accessed': '2023-08-29T15:37:43+0000',
                    'acquired': '2023-08-29T15:37:43+0000',
                    'id': 'H+DBL3Lj',
                    'lock_name': 'Administrator',
                    'owner': 'Administrator'}


unlock_response_good = {
    "accessed": None,
    "acquired": None,
    "id": "",
    "lock_name": "",
    "owner": ""
}

unlock_response_bad = {
  "error": {
    "code": "LockError",
    "data": {
      "accessed": "2023-08-31T17:08:11+0000",
      "acquired": "2023-08-31T17:08:11+0000",
      "lock_owner": "Administrator"
    },
    "message": "The analyser is currently locked"
  }
}

start_response_good = {
    [{"buffer": {"limit": 75497328, "max_buffer_size": 77309411328, "trigger_point": None, "trigger_position": 100,
                 "used": 144, "wrapped": False},
      "current": {"almp": 0, "cachemem": 0, "cxl": False, "dllps": 22865, "eidle": False, "errors": 0, "io": 0,
                  "speed": 2, "tlps": 3, "training": 0, "width": 2},
      "last_second": {"almp": 0, "cachemem": 0, "cxl": 0, "dllps": 91442, "eidle": 0, "errors": 0, "io": 0, "tlps": 3,
                      "training": 0}, "latest_ts": 0, "name": "dn.0", "overflowed": False, "recording": True,
      "trigger_ts": 18446744073709551615, "triggered": False, "type": "data"}, {
         "buffer": {"limit": 75497328, "max_buffer_size": 77309411328, "trigger_point": None, "trigger_position": 100,
                    "used": 432, "wrapped": False},
         "current": {"almp": 0, "cachemem": 0, "cxl": False, "dllps": 33277, "eidle": False, "errors": 0, "io": 0,
                     "speed": 2, "tlps": 3, "training": 0, "width": 2},
         "last_second": {"almp": 0, "cachemem": 0, "cxl": 0, "dllps": 133093, "eidle": 0, "errors": 0, "io": 0,
                         "tlps": 3, "training": 0}, "latest_ts": 0, "name": "up.0", "overflowed": False,
         "recording": True, "trigger_ts": 18446744073709551615, "triggered": False, "type": "data"},
     {"buffer": {"limit": 1073741824, "max_buffer_size": 1073741824, "used": 0, "wrapped": False}, "current": {
         "signals": [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]},
      "name": "sideband.0", "type": "sideband"}, {
         "buffer": {"limit": 1073741824, "max_buffer_size": 1073741824, "trigger_point": None, "trigger_position": 100,
                    "used": 0, "wrapped": False}, "current": {"nacks": 0, "reads": 8, "timeouts": 0, "writes": 6},
         "last_second": {"nacks": 0, "reads": 16, "timeouts": 0, "writes": 12}, "latest_ts": 0, "name": "smbus.0",
         "recording": False, "trigger_ts": 18446744073709551116, "triggered": False, "type": "smbus"}],
    [{'buffer': {'limit': 75497328, 'max_buffer_size': 77309411328, 'trigger_point': None, 'trigger_position': 100,
                 'used': 144, 'wrapped': False},
      'current': {'almp': 0, 'cachemem': 0, 'cxl': False, 'dllps': 22865, 'eidle': False, 'errors': 0, 'io': 0,
                  'speed': 2, 'tlps': 3, 'training': 0, 'width': 2},
      'last_second': {'almp': 0, 'cachemem': 0, 'cxl': 0, 'dllps': 91442, 'eidle': 0, 'errors': 0, 'io': 0, 'tlps': 3,
                      'training': 0}, 'latest_ts': 0, 'name': 'dn.0', 'overflowed': False, 'recording': True,
      'trigger_ts': 18446744073709551615, 'triggered': False, 'type': 'data'}, {
        'buffer': {'limit': 75497328, 'max_buffer_size': 77309411328, 'trigger_point': None, 'trigger_position': 100,
                   'used': 432, 'wrapped': False},
        'current': {'almp': 0, 'cachemem': 0, 'cxl': False, 'dllps': 33277, 'eidle': False, 'errors': 0, 'io': 0,
                    'speed': 2, 'tlps': 3, 'training': 0, 'width': 2},
        'last_second': {'almp': 0, 'cachemem': 0, 'cxl': 0, 'dllps': 133093, 'eidle': 0, 'errors': 0, 'io': 0,
                        'tlps': 3, 'training': 0}, 'latest_ts': 0, 'name': 'up.0', 'overflowed': False,
        'recording': True, 'trigger_ts': 18446744073709551615, 'triggered': False, 'type': 'data'}, {
        'buffer': {'limit': 1073741824, 'max_buffer_size': 1073741824, 'used': 0, 'wrapped': False}, 'current': {
            'signals': [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                        1]}, 'name': 'sideband.0', 'type': 'sideband'}, {
        'buffer': {'limit': 1073741824, 'max_buffer_size': 1073741824, 'trigger_point': None, 'trigger_position': 100,
                   'used': 0, 'wrapped': False}, 'current': {'nacks': 0, 'reads': 8, 'timeouts': 0, 'writes': 6},
        'last_second': {'nacks': 0, 'reads': 16, 'timeouts': 0, 'writes': 12}, 'latest_ts': 0, 'name': 'smbus.0',
        'recording': False, 'trigger_ts': 18446744073709551116, 'triggered': False, 'type': 'smbus'}]
}

start_response_good2 = {
    [{"buffer": {"limit": 75497328, "max_buffer_size": 77309411328, "trigger_point": None, "trigger_position": 100,
                 "used": 0, "wrapped": False},
      "current": {"almp": 0, "cachemem": 0, "cxl": False, "dllps": 0, "eidle": True, "errors": 0, "io": 0, "speed": 0,
                  "tlps": 0, "training": 0, "width": 0},
      "last_second": {"almp": 0, "cachemem": 0, "cxl": 0, "dllps": 0, "eidle": 4, "errors": 0, "io": 0, "tlps": 0,
                      "training": 0}, "latest_ts": 0, "name": "dn.0", "overflowed": False, "recording": True,
      "trigger_ts": 18446744073709551615, "triggered": False, "type": "data"}, {
         "buffer": {"limit": 75497328, "max_buffer_size": 77309411328, "trigger_point": None, "trigger_position": 100,
                    "used": 0, "wrapped": False},
         "current": {"almp": 0, "cachemem": 0, "cxl": False, "dllps": 0, "eidle": True, "errors": 0, "io": 0,
                     "speed": 2, "tlps": 0, "training": 0, "width": 2},
         "last_second": {"almp": 0, "cachemem": 0, "cxl": 0, "dllps": 0, "eidle": 4, "errors": 0, "io": 0, "tlps": 0,
                         "training": 0}, "latest_ts": 0, "name": "up.0", "overflowed": False, "recording": True,
         "trigger_ts": 18446744073709551615, "triggered": False, "type": "data"},
     {"buffer": {"limit": 1073741824, "max_buffer_size": 1073741824, "used": 0, "wrapped": False}, "current": {
         "signals": [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]},
      "name": "sideband.0", "type": "sideband"}, {
         "buffer": {"limit": 1073741824, "max_buffer_size": 1073741824, "trigger_point": None, "trigger_position": 100,
                    "used": 0, "wrapped": False}, "current": {"nacks": 0, "reads": 0, "timeouts": 0, "writes": 0},
         "last_second": {"nacks": 0, "reads": 0, "timeouts": 0, "writes": 0}, "latest_ts": 0, "name": "smbus.0",
         "recording": False, "trigger_ts": 18446744073709551116, "triggered": False, "type": "smbus"}],
    [{'buffer': {'limit': 75497328, 'max_buffer_size': 77309411328, 'trigger_point': None, 'trigger_position': 100,
                 'used': 0, 'wrapped': False},
      'current': {'almp': 0, 'cachemem': 0, 'cxl': False, 'dllps': 0, 'eidle': True, 'errors': 0, 'io': 0, 'speed': 0,
                  'tlps': 0, 'training': 0, 'width': 0},
      'last_second': {'almp': 0, 'cachemem': 0, 'cxl': 0, 'dllps': 0, 'eidle': 4, 'errors': 0, 'io': 0, 'tlps': 0,
                      'training': 0}, 'latest_ts': 0, 'name': 'dn.0', 'overflowed': False, 'recording': True,
      'trigger_ts': 18446744073709551615, 'triggered': False, 'type': 'data'}, {
         'buffer': {'limit': 75497328, 'max_buffer_size': 77309411328, 'trigger_point': None, 'trigger_position': 100,
                    'used': 0, 'wrapped': False},
         'current': {'almp': 0, 'cachemem': 0, 'cxl': False, 'dllps': 0, 'eidle': True, 'errors': 0, 'io': 0,
                     'speed': 2, 'tlps': 0, 'training': 0, 'width': 2},
         'last_second': {'almp': 0, 'cachemem': 0, 'cxl': 0, 'dllps': 0, 'eidle': 4, 'errors': 0, 'io': 0, 'tlps': 0,
                         'training': 0}, 'latest_ts': 0, 'name': 'up.0', 'overflowed': False, 'recording': True,
         'trigger_ts': 18446744073709551615, 'triggered': False, 'type': 'data'},
     {'buffer': {'limit': 1073741824, 'max_buffer_size': 1073741824, 'used': 0, 'wrapped': False}, 'current': {
         'signals': [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]},
      'name': 'sideband.0', 'type': 'sideband'}, {
         'buffer': {'limit': 1073741824, 'max_buffer_size': 1073741824, 'trigger_point': None, 'trigger_position': 100,
                    'used': 0, 'wrapped': False}, 'current': {'nacks': 0, 'reads': 0, 'timeouts': 0, 'writes': 0},
         'last_second': {'nacks': 0, 'reads': 0, 'timeouts': 0, 'writes': 0}, 'latest_ts': 0, 'name': 'smbus.0',
         'recording': False, 'trigger_ts': 18446744073709551116, 'triggered': False, 'type': 'smbus'}]
}

start_response_bad = {
  "error": {
    "code": "MissingParameter",
    "data": {
      "parameter": "lock_key"
    },
    "message": "A required parameter was not present in the request"
  }
}

start_hang_response = '<!DOCTYPE html>\n<html>\n<head>\n<title>Error</title>\n<style>\n    body {\n        width: 35em;\n        margin: 0 auto;\n        font-family: Tahoma, Verdana, Arial, sans-serif;\n    }\n</style>\n</head>\n<body>\n<h1>An error occurred.</h1>\n<p>Sorry, the page you are looking for is currently unavailable.<br/>\nPlease try again later.</p>\n<p>If you are the system administrator of this resource then you should check\nthe error log for details.</p>\n<p><em>Faithfully yours, nginx.</em></p>\n</body>\n</html>\n'


stop_response_bad = {
  "error": {
    "code": "LockError",
    "data": {
      "accessed": "2023-08-31T17:27:32+0000",
      "acquired": "2023-08-31T17:08:11+0000",
      "lock_owner": "Administrator"
    },
    "message": "The provided lock key does not match the lock"
  }
}


get_users_good = {
  "count": 5,
  "members": [
    {
      "uri": "/kodiak/v1/users/admin"
    },
    {
      "uri": "/kodiak/v1/users/davidn"
    },
    {
      "uri": "/kodiak/v1/users/esse quis velit"
    },
    {
      "uri": "/kodiak/v1/users/mholsey"
    },
    {
      "uri": "/kodiak/v1/users/shynes"
    }
  ]
}