#!/usr/bin/bash

export IMAGE_GALLERY_SCRIPT_VERSION="1.1"
CONFIG_BUCKET="edu.au.cc.image-gallery-config1"

# Install packages
sudo yum -y update
sudo amazon-linux-extras install -y java-openjdk11
sudo yum install -y git postgresql postgresql-devel gcc
sudo yum install -y nano tree python3 java-11-openjdk-devel
sudo amazon-linux-extras install -y nginx1
su ec2-user -l -c 'curl -s "https://get.sdkman.io" | bash && source .bashrc && sdk install gradle'

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/tnguyenken/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
su ec2-user -l -c "cd ~/python-image-gallery && pip3 install -r

aws s3 cp s3://${CONFIG_BUCKET}/nginx/nginx.conf/etc/nginx
aws s3 cp s3://${CONFIG_BUCKET}/default.d/image_gallery.conf/etc/nginx/default.d


# Start/enable services
systemctl stop postfix
systemctl disable postfix
systemctl start nginx
systemctl enable nginx

su ec2-user -l -c "cd ~/python-image-gallery && ./start" >/var/log/image_gallery.log 2>&l &
