import sys, os, re
import subprocess

def qidSearch(qid, user, qstat="/opt/pbs/default/bin/qstat"):
    """根据用提交任务的jobid号查询运行状态"""
    qcmd = f"{qstat} -a -u {user} {qid} | grep ^{qid}"
    p = subprocess.Popen(qcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait() #等待qcmd命令执行结束    
    pout = str(p.stdout.read(), "utf-8").strip()
    if pout != "":
        out = re.split("\s+", pout)
        return out 

if __name__ == "__main__":
    qid = sys.argv[1]
    user = sys.argv[2]
    qidSearch(qid, user)
