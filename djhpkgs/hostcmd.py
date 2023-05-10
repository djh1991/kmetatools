import sys

def hostcmd(command, user="dengjh", password="dengjh123", host="10.128.68.3"):
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,
        port = 22,
        username = user,
        password = password,)
    stdin, stdout, stderr = client.exec_command(command)
    for line in stdout:
        sys.stdout.write(line)
        #click.secho(line.strip(), fg="green", bg="black", bold=True)
    
    stderr_data = str(stderr.read(), "utf-8")
    if stderr_data != "":
        sys.stderr.write(stderr_data)
        #click.secho(stderr_data.strip(), fg="red", bg="black", bold=True)
    client.close()

if __name__ == "__main__":

    import click
    @click.command()
    @click.argument("command")
    @click.option("--user", "-u", default="dengjh", help="远端服务器执行用户账号, default: 云管理节点mu01的dengjh账号")
    @click.option("--password", "-p", default="dengjh123", help="远端服务器执行用户密码, default: 云管理节点mu01的dengjh账号对应密码")
    @click.option("--host", "-h", default="10.128.68.3", help="远端服务器ip地址, default: 云管理节点mu01的IP地址")
    def hostcmd_para(*args, **kwagrs):
        """
        说明:
        \v  该工具用于执行远程服务器命令
        \v  默认参数是用dengjh账号密码在华为云管理节点执行命令
        \vExample:
        \v  python3 hostcmd.py "ls -hl ./"
        """
        hostcmd(*args, **kwagrs)
        #click.secho("Done!", fg="red", bg="white", underline=True)

    hostcmd_para()
