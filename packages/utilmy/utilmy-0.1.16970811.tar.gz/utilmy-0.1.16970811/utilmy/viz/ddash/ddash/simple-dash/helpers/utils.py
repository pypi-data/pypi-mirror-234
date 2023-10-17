import logging

import os
from threading import Timer
import subprocess

# https://gist.github.com/alexbw/1187132/5de3149db6e744502c166711114bebc97af928f3
class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

def run_subprocess_cmd(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    proc = subprocess.Popen(args_list, stdout=stdout, stderr=stderr)
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout, stderr

def renew_kerberos_ticket():
    logging.info(f'renewing kerberos ticket with krb cache file {os.environ["KRB5CCNAME"]}')
    keytab_file = os.environ['KEYTAB_FILE']
    principal = os.environ['PRINCIPAL']
    cmd = ['kinit', '-kt', keytab_file, principal]
    rcode, stdout, stderr = run_subprocess_cmd(cmd)
    if rcode != 0:
        logging.error(f'can not renew ticket, stdout: {stdout}, stderr: {stderr}')
    rcode, stdout, stderr = run_subprocess_cmd(['klist'])
    logging.debug(f'ticket info {stdout}')
    return rcode

def start_kinit_daemon():
    logging.info(f'start kinit backend')
    renew_kerberos_ticket()
    kinit = RepeatingTimer(3600, renew_kerberos_ticket)
    kinit.setDaemon(True)
    kinit.start()
    logging.info('started thread')
