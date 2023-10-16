import click
from .agent_manager import CyPerfAgentManager
from .common_options import common_options
from .custom_types import NETADDR

pass_agent_manager = click.make_pass_decorator(CyPerfAgentManager)

@click.group()
def agent_manager():
    pass

@agent_manager.command()
@common_options
@pass_agent_manager
@click.option('--controller-ip',
              required = True,
              help     = 'The IP/Hostname of the CyPerf controller.',
              type     = NETADDR,
              prompt   = True)
def set_controller(agentManager, controller_ip):
    agentManager.ControllerSet (controller_ip)

@agent_manager.command()
@common_options
@pass_agent_manager
def reload(agentManager):
    agentManager.Reload ()

@agent_manager.command()
@common_options
@pass_agent_manager
@click.option('--test-interface',
              required = True,
              help     = 'The name of the interface on the agents which will be used for test traffic.',
              type     = str,
              prompt   = True)
def set_test_interface(agentManager, test_interface):
    agentManager.SetTestInterface (test_interface)

@agent_manager.command()
@common_options
@pass_agent_manager
@click.option('--debian-file-path',
              required = True,
              help     = 'Path to the .deb file to be installed.',
              type     = click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
              prompt   = True)
def install_build(agentManager, debian_file_path):
    agentManager.InstallBuild (debian_file_path)

def main():
    agent_manager()
