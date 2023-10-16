import click
from .common_constants import CyPerfDefaults
from .agent_manager import CyPerfAgentManager
from .custom_types import NETADDRLIST, OptionalPassword

def agent_ips_option(f):
    def callback(ctx, param, value):
        agentMgr = ctx.ensure_object(CyPerfAgentManager)
        agentMgr.agentIPs = value
        return value
    return click.option('--agent-ips',
                        required = True,
                        type = NETADDRLIST,
                        expose_value = False,
                        help = CyPerfDefaults.AGENT_IPS_HELP_TEXT,
                        callback = callback)(f)

def user_name_option(f):
    def callback(ctx, param, value):
        agentMgr = ctx.ensure_object(CyPerfAgentManager)
        agentMgr.userName = value
        return value
    return click.option('--username',
                        required = False,
                        type = str,
                        default = CyPerfDefaults.DEFAULT_USER_NAME,
                        show_default = True,
                        expose_value = False,
                        help = 'A common username for all the agents.',
                        callback = callback)(f)

def password_option(f):
    def callback(ctx, param, value):
        agentMgr = ctx.ensure_object(CyPerfAgentManager)
        agentMgr.password = value
        return value
    return click.password_option(default = CyPerfDefaults.DEFAULT_PASSWORD,
                                 expose_value = False,
                                 help = 'A common password for all the agents.',
                                 cls = OptionalPassword,
                                 callback = callback)(f)

def key_file_option(f):
    def callback(ctx, param, value):
        agentMgr = ctx.ensure_object(CyPerfAgentManager)
        agentMgr.keyFile = value
        return value
    return click.option('--key-file',
                        type = click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, writable=False),
                        default = None,
                        required = False,
                        expose_value = False,
                        show_default = True,
                        help = 'A common key file for opening ssh connections to all the agents.',
                        callback = callback)(f)

def common_options(f):
    f = key_file_option(f)
    f = password_option (f)
    f = click.option('--override-password',
                     default = False,
                     required = False,
                     is_flag = True,
                     expose_value = False,
                     help = 'This along with --password option should be used for non default password.')(f)
    f = user_name_option (f)
    f = agent_ips_option (f)
    return f

