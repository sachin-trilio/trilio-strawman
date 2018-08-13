import os
import subprocess
from charms.reactive import when, when_not, set_flag, is_state, hook, remove_state
from charmhelpers.core.hookenv import status_set, config


@when_not('sreact.installed')
def install_sreact():

    #Push /usr/bin onto the start of $PATH from the hander for the specific subprocess call for the install script.
    #This will make pip to be called from host install rather than virtualenv.
    s_env = os.environ.copy()
    s_env['PATH'] = '/usr/bin:{}'.format(s_env['PATH'])
    
    #Read config parameters TVault version, TVault IP, Horizon Path and Webserver
    tv_version = config('TVAULT_V')
    tv_ip = config('TVAULTAPP')
    horizon_path = config('HORIZON_PATH')
    webserver = config('WebServer')

    #Call install script to install the packages
    subprocess.check_call(['files/trilio/install', tv_version, tv_ip, horizon_path, webserver], env=s_env)
    set_flag('sreact.installed')

@hook('{requires:name}-relation-{joined,changed}')
def changed_sreact(self):
    self.set_state('{relation_name}.available')

@hook('{requires:name}-relation-{broken,departed}')
def broken_sreact(self):
    self.remove_state('{relation_name}.available')
