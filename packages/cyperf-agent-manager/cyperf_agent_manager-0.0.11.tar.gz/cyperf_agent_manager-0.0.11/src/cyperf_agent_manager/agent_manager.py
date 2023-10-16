import os
import click
import paramiko
import scp
from .common_constants import CyPerfDefaults

class CyPerfAgentManager (object):
    def __init__ (self,
                  agentIPs = [],
                  userName = CyPerfDefaults.DEFAULT_USER_NAME,
                  password = CyPerfDefaults.DEFAULT_PASSWORD,
                  keyFile  = None):
        self.agentIPs = agentIPs
        self.userName = userName
        self.password = password
        self.keyFile  = keyFile
        self.client   = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __connect__(self, addr = '127.0.0.1'):
        if self.keyFile:
           try: 
                self.client.connect(addr, username=self.userName, key_filename=self.keyFile)
                return
           except ValueError:
                click.echo (f'{self.keyFile} is not appropriate for {addr}, trying with password \'{self.password}\'')
           except paramiko.ssh_exception.AuthenticationException:
                click.echo (f'Key based authentication failed, trying with password \'{self.password}\'')
        self.client.connect(addr, username=self.userName, password=self.password)
        
    def __exec__(self, cmd, sudo=False):
        if sudo:
            cmd = f'sudo -S -p \'\' {cmd}' 
        for agent in self.agentIPs:
            try:
                click.echo (f'>> Connectiong to agent {agent}')
                self.__connect__(agent)
                try:
                    click.echo (f'>> Executing command {cmd}')
                    _stdin, _stdout, _ = self.client.exec_command (cmd)
                    if sudo:
                        _stdin.write(self.password + "\n")
                        _stdin.flush()
                    _stdin.close()
                    _stdout.channel.set_combine_stderr(True)
                    click.echo(_stdout.read().decode())
                except paramiko.ssh_exception.SSHException:
                    click.echo (f'Failed to execute command {cmd}')
                self.client.close()
            except paramiko.ssh_exception.NoValidConnectionsError:
                click.echo (f'Connection is refused by the server')
            except paramiko.ssh_exception.AuthenticationException:
                click.echo (f'Login failed because of invalid credentials')
            except TimeoutError:
                click.echo (f'Connection timed out')

    def __copy__(self, localPath, remotePath):
        for agent in self.agentIPs:
            try:
                click.echo (f'>> Connectiong to agent {agent}')
                self.__connect__(agent)
                try:
                    click.echo (f'>> Tranferring file {localPath} to {remotePath}')
                    with scp.SCPClient(self.client.get_transport()) as _scp:
                        _scp.put(localPath, remotePath)
                except scp.SCPException:
                    click.echo (f'Failed to transfer file {localPath} to {remotePath}')
                self.client.close()
            except paramiko.ssh_exception.NoValidConnectionsError:
                click.echo (f'Connection is refused by the server')
            except paramiko.ssh_exception.AuthenticationException:
                click.echo (f'Login failed because of invalid credentials')
            except TimeoutError:
                click.echo (f'Connection timed out')

    def ControllerSet (self, controllerIP):
        cmd = f'cyperfagent controller set {controllerIP}'
        self.__exec__(cmd)

    def Reload (self):
        cmd = f'cyperfagent configuration reload'
        self.__exec__(cmd)

    def SetTestInterface (self, iface):
        cmd = f'cyperfagent interface test set {iface}'
        self.__exec__(cmd)

    def InstallBuild (self, debFile):
        remotePath = f'~/{os.path.basename(debFile)}'
        cmd        = f'apt install -y {remotePath}'
        self.__copy__ (debFile, remotePath)
        self.__exec__ (cmd, sudo=True)

