import logging

import russh

private_key = russh.PrivateKeyAuth(private_key="/home/nikhil/.ssh/nikhil_rsa")
auth = russh.AuthMethods(private_key=private_key)
client = russh.SSHClient()

try:
    client.connect("192.168.0.112", "root", auth, port=2222, timeout=10)
    print(client.exec_command("cat /etc/os-release"))

    res = client.exec_command("hello")
    print(res)

except russh.RusshException as _e:
    logging.error(_e)

finally:
    client.close()
