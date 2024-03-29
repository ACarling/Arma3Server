import os
import re
import subprocess
import urllib.request

import keys

WORKSHOP = "steamapps/workshop/content/107410/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"  # noqa: E501

# check keys through download - if no key found retry up to maxretries (1000 or something high)
def download(mods):
    #retries=os.environ["MAX_RETRIES"]

    steamcmd = [os.environ["STEAMCMDDIR"] + "/steamcmd.sh"]
    steamcmd.extend(["+force_install_dir", "/arma3"])
    steamcmd.extend(["+login", os.environ["STEAM_USER"]])
        
    for id in mods:
        steamcmd.extend(["+workshop_download_item", "107410", id])
        steamcmd.extend(["validate"])

    steamcmd.extend(["+quit"])
    res = ""
    while res != 0:
        res = subprocess.call(steamcmd)
        subprocess.call(["/bin/cp","-a","/arma3/steamapps/workshop/downloads/107410/.","/arma3/steamapps/workshop/content/107410/"])




def preset(mod_file):
    if mod_file.startswith("http"):
        req = urllib.request.Request(
            mod_file,
            headers={"User-Agent": USER_AGENT},
        )
        remote = urllib.request.urlopen(req)
        with open("preset.html", "wb") as f:
            f.write(remote.read())
        mod_file = "preset.html"
    mods = []
    moddirs = []
    with open(mod_file) as f:
        html = f.read()
        regex = r"filedetails\/\?id=(\d+)\""
        matches = re.finditer(regex, html, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            mods.append(match.group(1))
            moddir = WORKSHOP + match.group(1)
            moddirs.append(moddir)
        download(mods)
        for moddir in moddirs:
            keys.copy(moddir)
    return moddirs
