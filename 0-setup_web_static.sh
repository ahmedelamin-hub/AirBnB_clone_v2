#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Install Nginx if it is not already installed
sudo apt-get update
sudo apt-get install -y nginx

# Ensure that directories exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ directory to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
config="\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "/^http {/a $config" /etc/nginx/nginx.conf

# Restart Nginx to apply the configuration changes
sudo systemctl restart nginx

# Exit successfully
exit 0
