import os
import re
import subprocess
import urllib.request

import keys

WORKSHOP = "steamapps/workshop/content/107410/"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"  # noqa: E501

# check keys through download - if no key found retry up to maxretries (1000 or something high)
def download(mods):
    steamcmd = ["/steamcmd/steamcmd.sh"]
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


#https://github.com/ValveSoftware/steam-for-linux/issues/6321#issuecomment-1301395966
def downloadMod(ids):
    steamcmd = ["/steamcmd/steamcmd.sh"]
    steamcmd.extend(["+force_install_dir", "/arma3"])
    steamcmd.extend(["+login", os.environ["STEAM_USER"]])
    for id in ids:
        steamcmd.extend(["+workshop_download_item", "107410", id])
        steamcmd.extend(["validate"])
    steamcmd.extend(["+quit"])
    try:
        subprocess.run(steamcmd, check=True)
    except subprocess.CalledProcessError:
        # If this is triggered, steamcmd ran into an issue, most likely a server side timeout
        # Retrying the download with the timeout set in .env, without +quit
        steamcmd.pop(-1)
        if "WORKSHOP_TIMEOUT" in os.environ and len(os.environ["WORKSHOP_TIMEOUT"]) > 0:
            timeout = int(os.environ["WORKSHOP_TIMEOUT"])*60
        else:
            timeout = 600
        subprocess.run(steamcmd, timeout=timeout, check=True)







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
        downloadMod(mods)
        for moddir in moddirs:
            keys.copy(moddir)

    sp=[]
    sp.extend(["find", "/arma3/steamapps/workshop/content/107410/", "-depth", "-exec", "rename", 's/(.*)\/([^\/]*)/$1\/\L$2/', "{}", "/"])



    subprocess.run(sp, check=True)
    return moddirs
