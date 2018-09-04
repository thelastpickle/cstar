# Copyright 2017 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#import paramiko.client
from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_CREAT, LIBSSH2_FXF_WRITE, LIBSSH2_FXF_READ \
    LIBSSH2_SFTP_S_IRUSR, LIBSSH2_SFTP_S_IRGRP, LIBSSH2_SFTP_S_IWUSR, \
    LIBSSH2_SFTP_S_IROTH
import os, socket
import re

from cstar.output import err, debug, msg
from cstar.exceptions import BadSSHHost, BadEnvironmentVariable, NoHostsSpecified
from cstar.executionresult import ExecutionResult

SFTP_MODE = LIBSSH2_SFTP_S_IRUSR | \
           LIBSSH2_SFTP_S_IWUSR | \
           LIBSSH2_SFTP_S_IRGRP | \
           LIBSSH2_SFTP_S_IROTH
SFTP_FLAGS = LIBSSH2_FXF_CREAT | LIBSSH2_FXF_WRITE
PING_COMMAND = "echo ping"

_alnum_re = re.compile(r"[^a-zA-Z0-9\|_]")


class Remote(object):
    def __init__(self, hostname, ssh_username=None, ssh_password=None, ssh_identity_file=None):
        if hasattr(hostname, "ip"):
            self.hostname = hostname.ip
        else:
            self.hostname = hostname
        if not self.hostname:
            raise NoHostsSpecified("No SSH host specified")
        self.ssh_username = ssh_username
        self.ssh_password = ssh_password
        self.ssh_identity_file = ssh_identity_file
        self.channel = None
        self.session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def _connect(self):
        if self.channel:
            # Ensure underlying client is still a valid open connection
            try:
                self.channel.exec_command(PING_COMMAND)
                size, data = self.channel.read()
                while size > 0:
                    print(data)
                    size, data = self.channel.read()
            except:
                # ConnectionResetError is raised when a connection was established but then broken
                # paramiko.ssh_exception.SSHException is raised if the connection was known to be broken
                self.channel = None

        if not self.channel:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.hostname, 22))
                self.session = Session()
                self.session.handshake(sock)
                if self.ssh_identity_file != None:
                    self.session.userauth_publickey_fromfile(self.ssh_username, None, self.ssh_identity_file, '')
                if self.ssh_password != None:
                    self.session.userauth_password(ssh_username, self.ssh_password)
                debug("Username : ", self.ssh_username)
                debug("Id file: ", self.ssh_identity_file)
                self.channel = self.session.open_session()
            except:
                self.channel = None
                raise BadSSHHost("Could not establish an SSH connection to host %s" % (self.hostname,))

    def run_job(self, file, jobid, timeout=None, env={}):
        try:
            self._connect()
            dir = ".cstar/remote-jobs/" + jobid
            self.run(("mkdir", "-p", dir))
            self.put_command(file, "%s/job" % (dir,))

            # Manually insert environment into script, since passing env into exec_command leads to it being
            # ignored on most ssh servers. :-(

            for key in env:
                if _alnum_re.search(key):
                    raise BadEnvironmentVariable(key)

            env_str = " ".join(key + "=" + self.escape(value) for key, value in env.items())
            wrapper = r"""#! /bin/sh

    if test -f pid; then
        # We can't wait for things that aren't our children. Loop and sleep. :-(
        while ! test -f status; do
            sleep 10s
        done
        exit
    fi

    %s ./job >stdout 2>stderr &
    echo $! >pid
    wait $!
    echo $? >status
    """ % (env_str,)
            self.write_command(wrapper, "%s/wrapper" % (dir,))

            cmd = """
    cd %s
    nohup ./wrapper
    """ % (self.escape(dir),)
            self.channel.execute(cmd, timeout=timeout)
            out, err, status = self.read_channel()
            real_output = self.read_file(dir + "/stdout")
            real_error = self.read_file(dir + "/stderr")
            real_status = int(self.read_file(dir + "/status"))
            return ExecutionResult(cmd, real_status, real_output, real_error)
        except:
            raise BadSSHHost("SSH connection to host %s was reset" % (self.hostname,))

    def get_job_status(self, jobid):
        pass

    def run(self, argv):
        try:
            self._connect()
            cmd = " ".join(self.escape(s) for s in argv)

            self.channel.execute(cmd)
            out, error, status = self.read_channel()
            if status != 0:
                err("Command %s failed with status %d on host %s" % (cmd, status, self.hostname))
            else:
                debug("Command %s succeeded on host %s, output was %s and %s" %
                      (cmd, self.hostname, str(out, 'utf-8'), str(error, 'utf-8')))
            return ExecutionResult(cmd, status, str(out, 'utf-8'), str(error, 'utf-8'))
        except:
            self.client = None
            raise BadSSHHost("SSH connection to host %s was reset" % (self.hostname,))

    # read stderr, stdout and exit code from the ssh2 channel object
    def read_channel(self):
        stdout_list = []
        stderr_list = []
        
        # read stdout
        size, stdout_part = self.channel.read()
        while size > 0:
            stdout_list.append(stdout_part)
            size, stdout_part = self.channel.read()
        
        # read stderr
        size, stderr_part = self.channel.read_stderr()
        while size > 0:
            stderr_list.append(stderr_part)
            size, stderr_part = self.channel.read_stderr()
         
        status = self.channel.get_exit_status()

        return stdout_list.join(""), stderr_list.join(""), status

    @staticmethod
    def escape(input):
        if _alnum_re.search(input):
            return "'" + input.replace("'", r"'\''") + "'"
        return input

    def read_file(self, remotepath):
        self._connect()
        content = []
        sftp = self.session.sftp_init()
        with sftp.open(remotepath, LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as remote_fh:
            for size, data in remote_fh:
                content.append(data)
        return str(content.join(""), 'utf-8')

    def put_file(self, localpath, remotepath):
        self._connect()
        sftp = self.session.sftp_init()
        with open(localpath, 'rb') as local_fh, \
            sftp.open(remotepath, SFTP_FLAGS, SFTP_MODE) as remote_fh:
            for data in local_fh:
                remote_fh.write(data)

    def put_command(self, localpath, remotepath):
        self._connect()
        self.put_file(localpath, remotepath)
        self.run("chmod 755" + remotepath)

    def write_command(self, definition, remotepath):
        self._connect()
        sftp = self.session.sftp_init()
        with sftp.open(remotepath, SFTP_FLAGS, SFTP_MODE) as remote_fh:
            remote_fh.write(definition)
            self.run("chmod 755" + remotepath)

    def mkdir(self, path):
        self.run("mkdir " + path)

    def close(self):
        if self.channel:
            self.channel.close()
        self.channel = None
        self.session = None
