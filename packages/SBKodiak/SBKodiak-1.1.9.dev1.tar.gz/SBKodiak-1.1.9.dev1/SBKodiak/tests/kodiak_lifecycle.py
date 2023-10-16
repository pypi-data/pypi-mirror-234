import os
import time

import paramiko

from kodiak_testing.KodiakAPI.KodiakControl import KodiakControlClass, KodiakWrapper
from kodiak_testing.KodiakAPI.KodiakGlobals import KodiakGlobals


def do_main():
    print('Running test through system')

    kw = KodiakWrapper("192.168.1.247", "mholsey", "", "gThV9h4LQmmSiYFNTcjBuvoRPvEC3LpW")

    print('Making a Kodiak Control object')
    my_kodiak = KodiakControlClass()

    print(f'Logging into kodiak using: {KodiakGlobals.my_kodiak_user}, {KodiakGlobals.my_kodiak_pass}')
    my_kodiak.login(kw)
    print('Logged in!') if my_kodiak.kodiak_session.logged_in else print('Login Variable not set!')

    print('Checking if we can get a refresh of the login')
    my_kodiak.refresh(kw)

    print('Locking the Module')
    if not my_kodiak.lock(kw):
        print("Failed to lock the system!")
        print(KodiakGlobals.last_response[-1])
        return

    print('Checking lock status')
    print(my_kodiak.get_lock_status(kw))

    # x = input('Is the lock correct?')
    # default_value = "n"
    # if x is default_value:
    #     return

    print('Starting the trace')
    print(my_kodiak.start(kw, trigger=True))

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.160', 22, username='root', password='sb')

    for x in range(16):
        if len(str(x)) < 2:
            x = "0" + str(x)

        print(f'sending a trigger to 1{x}')
        os_cmd = f'sbecho trigger=1{x} > /proc/vlun/nvme'
        print(f'Sending os command : {os_cmd} : to IP : 192.168.1.160')

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(os_cmd)
        print(ssh_stdin)
        print(ssh_stdout)
        print(ssh_stderr)
        # print(os.system(f'plink -ssh root@192.168.1.160 -pw sb "{os_cmd}"'))

        time.sleep(0.05)

        print('checking if the module triggered')
        response = my_kodiak.get_module_status(kw)

        print(response)

        if response:
            if response[0]['triggered']:
                print(response[0]['triggered'])
                print(f"MODULE WAS TRIGGERED ON PORT: 1{x}")
                break
    else:
        print("Did not trigger kodiak on any port, are you sure the trigger is correct and module attached?")
        # return

    print("stopping kodiak")
    print(my_kodiak.stop(kw))

    print('Unlocking Module')
    my_kodiak.unlock(kw)

    print('Checking the module is unlocked')
    print(my_kodiak.get_lock_status(kw))


if __name__ == "__main__":
    do_main()



"""
import os
import time

import paramiko

from kodiak_testing.KodiakAPI.KodiakControl import KodiakControlClass
from kodiak_testing.KodiakAPI.KodiakGlobals import KodiakGlobals


def do_main():
    print('Running test through system')

    print('Making a Kodiak Control object')
    my_kodiak = KodiakControlClass(kodiak_ip_address=KodiakGlobals.my_kodiak_ip, private_key="gThV9h4LQmmSiYFNTcjBuvoRPvEC3LpW")

    print(f'Logging into kodiak using: {KodiakGlobals.my_kodiak_user}, {KodiakGlobals.my_kodiak_pass}')
    my_kodiak.login(KodiakGlobals.my_kodiak_user, KodiakGlobals.my_kodiak_pass)
    print('Logged in!') if my_kodiak.kodiak_session.logged_in else print('Login Variable not set!')

    print('Checking if we can get a refresh of the login')
    my_kodiak.refresh()

    print('Locking the Module')
    if not my_kodiak.lock():
        print("Failed to lock the system!")
        print(KodiakGlobals.last_response[-1])
        return

    print('Checking lock status')
    print(my_kodiak.get_lock_status())

    # x = input('Is the lock correct?')
    # default_value = "n"
    # if x is default_value:
    #     return

    print('Starting the trace')
    print(my_kodiak.start(trigger=True))

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.160', 22, username='root', password='sb')

    for x in range(16):
        if len(str(x)) < 2:
            x = "0" + str(x)

        print(f'sending a trigger to 1{x}')
        os_cmd = f'sbecho trigger=1{x} > /proc/vlun/nvme'
        print(f'Sending os command : {os_cmd} : to IP : 192.168.1.160')

        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(os_cmd)
        print(ssh_stdin)
        print(ssh_stdout)
        print(ssh_stderr)
        # print(os.system(f'plink -ssh root@192.168.1.160 -pw sb "{os_cmd}"'))

        time.sleep(0.05)

        print('checking if the module triggered')
        response = my_kodiak.get_module_status()

        print(response)

        if response:
            if response[0]['triggered']:
                print(response[0]['triggered'])
                print(f"MODULE WAS TRIGGERED ON PORT: 1{x}")
                break
    else:
        print("Did not trigger kodiak on any port, are you sure the trigger is correct and module attached?")
        # return


    print("stopping kodiak")
    print(my_kodiak.stop())

    print('Unlocking Module')
    my_kodiak.unlock()


    print('Checking the module is unlocked')
    print(my_kodiak.get_lock_status())



if __name__ == "__main__":
    do_main()"""