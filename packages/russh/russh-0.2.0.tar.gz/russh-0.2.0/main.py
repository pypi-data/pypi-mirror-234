import russh

private_key = russh.PrivateKeyAuth(private_key="/home/nikhil/.ssh/nikhil_rsa")
auth = russh.AuthMethods(private_key=private_key)
client = russh.SSHClient()

try:
    client.connect("192.168.0.112", "roott", auth, port=2222, timeout=10)
    print(client.exec_command("cat /etc/os-release"))

    res = client.exec_command("hello")
    print(res)

except Exception as _e:
    print(_e)

finally:
    client.close()
