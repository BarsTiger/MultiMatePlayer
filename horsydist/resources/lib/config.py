import os
import json

configfile = "resources/cfg.cfg"

if not os.path.isfile(configfile):
    cfgwrite = open(configfile, 'w+')
    empty = {}
    json.dump(empty, cfgwrite, indent=3)
    cfgwrite.close()

with open(configfile) as cfgread:
    config = json.load(cfgread)

try:
    config['mainbuild']
except:
    if "MultiMate_Player.py" in os.listdir(os.getcwd()):
        config['mainbuild'] = 'MultiMate_Player.py'
    elif "MultiMate_Player.pyw" in os.listdir(os.getcwd()):
        config['mainbuild'] = 'MultiMate_Player.pyw'
    elif "MultiMate_Player.exe" in os.listdir(os.getcwd()):
        config['mainbuild'] = 'MultiMate_Player.exe'
    with open(configfile, 'w+') as cfgwrite:
        json.dump(config, cfgwrite, indent=3)

try:
    config['showrpc']
except:
    config['showrpc'] = True
    with open(configfile, 'w+') as cfgwrite:
        json.dump(config, cfgwrite, indent=3)
