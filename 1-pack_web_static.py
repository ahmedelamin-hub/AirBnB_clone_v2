#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive for AirBnB Clone repo.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Packs all files in the 'web_static' directory
    The archive is stored in timestamp in its name.
    Returns the path to the archive if successful
    """
    try:
        # Ensure the 'versions' directory exists
        local("mkdir -p versions")

        # Create the archive
        date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date_str)
        local("tar -cvzf {} web_static".format(archive_path))

        # Print information about the packed files
        print("web_static packed: {} -> Bytes".format(archive_path))
        return archive_path
    except Exception as e:
        print(e)
        return None
