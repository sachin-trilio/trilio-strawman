import os
import subprocess
from charms.reactive import when, when_not, set_flag, is_state, hook, remove_state, set_state
from charmhelpers.core.hookenv import status_set, config

@hook('install')
def install_handler():

    # Set the user defined "installing" state when this hook event occurs.
    set_state('sreact.installing')

@when('sreact.installing')
def install_sreact():

    status_set('maintenance', 'Installing...')

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

    status_set('active', 'TVM Horizon Plugin installed...')

    #Remove the state "installing" since it's done
    remove_state('sreact.installing')

@hook('start')
def start_handler():

    # Set the user defined "starting" state when this hook event occurs.
    set_state('sreact.starting')

@when('sreact.starting')
def start_sreact():

    status_set('maintenance', 'Starting...')

    #Call the script to re-start webserver
    subprocess.check_call(['files/trilio/webserver-restart'])

    status_set('active', 'Ready...')

    #Remove the state "starting" since it's done
    remove_state('sreact.starting')

@hook('stop')
def stop_handler():

    # Set the user defined "stopping" state when this hook event occurs.
    set_state('sreact.stopping')

@when('sreact.stopping')
def stop_sreact():

    status_set('maintenance', 'Stopping...')

    #Push /usr/bin onto the start of $PATH from the hander for the specific subprocess call for the install script.
    #This will make pip to be called from host install rather than virtualenv.
    s_env = os.environ.copy()
    s_env['PATH'] = '/usr/bin:{}'.format(s_env['PATH'])
    
    #Call the script to stop and uninstll TVM Horizon Plugin
    subprocess.check_call(['files/trilio/stop'], env=s_env)

    #Remove the state "stopping" since it's done
    remove_state('sreact.stopping')


@hook('{requires:name}-relation-{joined,changed}')
def changed_sreact(self):
    self.set_state('{relation_name}.available')

@hook('{requires:name}-relation-{broken,departed}')
def broken_sreact(self):
    self.remove_state('{relation_name}.available')
