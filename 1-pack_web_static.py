#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
of your AirBnB Clone repo. It uses the function do_pack to pack all contents into an archive
and stores it in the 'versions' folder with a timestamped filename.

Usage: fab -f 1-pack_web_static.py do_pack
"""

from fabric.api import local
from datetime import datetime

def do_pack():
    """
    Packs all files in the 'web_static' directory into a .tgz archive.
    The archive is stored in the 'versions' folder with a timestamp in its name.
    Returns the path to the archive if successful, None otherwise.
    """
    try:
        # Ensure the 'versions' directory exists
        local("mkdir -p versions")

        # Create the archive
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date_str)
        local("tar -cvzf {} web_static".format(archive_path))

        # Print information about the packed files and return the archive path
        print("web_static packed: {} -> Bytes".format(archive_path))
        return archive_path
    except Exception as e:
        print(e)
        return None
