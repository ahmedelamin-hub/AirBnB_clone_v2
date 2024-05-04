#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py
"""

from fabric.api import env, run, put
from os.path import exists

env.hosts = ['35.153.93.185', '35.153.255.51']


def do_deploy(archive_path):
    """
    Deploys the archive to web servers.
    - Uploads the archive to the /tmp/ directory of the web server
    - Uncompresses the archive to the folder
    - Deletes the archive from the web server
    - Deletes the symbolic link
    - Creates a new symbolic link /data/web_static/curren
    Returns True or False
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        current_path = "/data/web_static/releases/"
        tmp_path = "/tmp/" + file_name

        # Upload the archive to the /tmp/ directory
        put(archive_path, tmp_path)

        # Create directory path in releases
        run(f"mkdir -p {current_path}{no_ext}")

        # Uncompress
        run(f"tar -xzf {tmp_path} -C {current_path}{no_ext}/")

        # Delete arch from the web server
        run(f"rm {tmp_path}")

        # Move ntentsthe web_static folder
        run(f"mv {current_path}{no_ext}/web_static/* {current_path}{no_ext}/")

        # Remove empty web_static folder
        run(f"rm -rf {current_path}{no_ext}/web_static")

        # Del curr symbolic link
        run("rm -rf /data/web_static/current")

        # new symbolic link
        run(f"ln -s {current_path}{no_ext}/ /data/web_static/current")

        print("New version deployed!")
        return True
    except (NetworkError, CommandTimeout) as e:
        print(f"Deployment failed: {e}")
        return False
