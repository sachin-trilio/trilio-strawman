import os
import subprocess
from charms.reactive import when, when_not, set_flag, is_state, hook, remove_state
from charmhelpers.core.hookenv import status_set, config


@when_not('sreact.installed')
def install_sreact():
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    
    #Read config parameters TVault version, TVault IP, Horizon Path and Webserver
    tv_version = config('TVAULT_V')
    tv_ip = config('TVAULTAPP')
    horizon_path = config('HORIZON_PATH')
    webserver = config('WebServer')
    #subprocess.check_call(['files/trilio/install', tv_version, tv_ip, horizon_path, webserver])
    subprocess.check_call(['files/trilio/install', tv_version, tv_ip, horizon_path, webserver], shell=True)
    set_flag('sreact.installed')
