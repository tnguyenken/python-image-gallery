#!/usr/bin/bash

# Install packages
yum -y update
amazon-linux-extras install -y java-openjdk11
yum install -y emacs-nox nano tree python3 java-11-openjdk-devel git
amazon-linux-extras install -y nginx1
su ec2-user -l -c 'curl -s "https://get.sdkman.io" | bash && source .bashrc && sdk install gradle'

# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/tnguyenken/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
su ec2-user -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"

# Start/enable services
systemctl stop postfix
systemctl disable postfix
systemctl start nginx
systemctl enable nginx
