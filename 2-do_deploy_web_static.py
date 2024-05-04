#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an archive
to your web servers using the function do_deploy.

Usage: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=<path> -i my_ssh_private_key -u ubuntu
"""

from fabric.api import env, run, put
from os.path import exists

env.hosts = ['35.153.93.185', '35.153.255.51']

def do_deploy(archive_path):
    """
    Deploys the archive to web servers.
    - Uploads the archive to the /tmp/ directory of the web server
    - Uncompresses the archive to the folder /data/web_static/releases/<archive name without extension> on the web server
    - Deletes the archive from the web server
    - Deletes the symbolic link /data/web_static/current from the web server
    - Creates a new symbolic link /data/web_static/current on the web server, linked to the new version of your code
    Returns True if all operations are successful, otherwise returns False.
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        current_path = "/data/web_static/releases/"
        tmp_path = "/tmp/" + file_name

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, tmp_path)

        # Create directory path in releases
        run(f"mkdir -p {current_path}{no_ext}")

        # Uncompress the archive to the folder on the web server
        run(f"tar -xzf {tmp_path} -C {current_path}{no_ext}/")

        # Delete the archive from the web server
        run(f"rm {tmp_path}")

        # Move contents out of the web_static folder to the base folder
        run(f"mv {current_path}{no_ext}/web_static/* {current_path}{no_ext}/")

        # Remove the now empty web_static folder
        run(f"rm -rf {current_path}{no_ext}/web_static")

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version folder
        run(f"ln -s {current_path}{no_ext}/ /data/web_static/current")

        print("New version deployed!")
        return True
    except:
        return False

