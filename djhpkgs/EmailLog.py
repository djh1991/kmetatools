import sys
import datetime
from .hostcmd import hostcmd
from metaconfig import *
import glob
from jinja2 import Template

def EmailLog(logfile, tpllog, subject="TEST", logtimes=0, ENV=locals()):
    old_logs = glob.glob(logfile + "*")
    if len(old_logs) >= logtimes:
        logging.info(f"日志邮件{logfile}超过{logtimes}次, 略过不再推送")
    else:
        if os.path.exists(logfile):
            dtstr = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_%H_%M_%S")
            rlogfile = logfile + "." + dtstr
            os.system(f"mv {logfile} {rlogfile}")
        with open(logfile, 'w') as w:
            tplstr = open(tpllog, 'r').read()
            w.write(Template(tplstr).render(locals()))

        if logtimes:
            try:
                cmd = f"{PYTHON3} {KMETATOOLS}/email/SeqEmail.py {KMETATOOLS}/email/From.json {KMETATOOLS}/email/To_test.list {logfile} --subject {subject}"
                logging.info(cmd)
                hostcmd(cmd)
            except Exception as e:
                logging.info(f"{e}")
                pass                
