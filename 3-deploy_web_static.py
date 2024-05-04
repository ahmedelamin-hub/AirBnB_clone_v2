#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers.
This script combines the functionalities of packing web static files into an archive
and deploying that archive to specified servers.

Usage: fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['35.153.93.185', '35.153.255.51']  # Example IP addresses

def do_pack():
    """
    Packs all files in the 'web_static' directory into a .tgz archive.
    The archive is stored in the 'versions' folder with a timestamp in its name.
    Returns the path to the archive if successful, None otherwise.
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None

def do_deploy(archive_path):
    """
    Deploys the archive to the web servers.
    Steps include uploading, uncompressing, and setting up the web directory.
    Returns True if all operations succeed, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = os.path.basename(archive_path)
        no_ext = file_name.split(".")[0]
        release_folder = "/data/web_static/releases/{}/".format(no_ext)
        current_link = "/data/web_static/current"
        tmp_archive = "/tmp/{}".format(file_name)

        put(archive_path, tmp_archive)
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf {} -C {}".format(tmp_archive, release_folder))
        run("rm {}".format(tmp_archive))
        run("mv {}web_static/* {}".format(release_folder, release_folder))
        run("rm -rf {}web_static".format(release_folder))
        run("rm -rf {}".format(current_link))
        run("ln -s {} {}".format(release_folder, current_link))
        return True
    except Exception as e:
        return False

def deploy():
    """
    Full deployment routine: packs and deploys web static files.
    Calls do_pack() to create an archive and do_deploy() to distribute it.
    Returns the result of the deployment process.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
