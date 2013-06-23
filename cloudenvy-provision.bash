#!/bin/bash

sudo apt-get update
sudo apt-get install -y git supervisor gunicorn

# Github's host key
echo "|1|KetpgischwnE2APMGKK6y9MK0v8=|JgiZdJOvO5BYamlkfRSO0lm/hIs= ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAq2A7hRGmdnm9tUDbO9IDSwBK6TbQa+PXYPCPy6rbTrTtw7PHkccKrpp0yVhp5HdEIcKr6pLlVDBfOLX9QUsyCOV0wzfjIJNlGEYsdlLJizHhbn2mUjvSAHQqZETYP81eFzLQNnPHt4EVVUh7VfDESU84KezmD5QlWpXLmvU31/yMf+Se8xhHTvKSCZIFImWwoG6mbUoWf9nzpIoaSjB+weqqUUmpaaasXVal72J+UX2B+2RPW3RcT0eOzQgqlJL3RKrTJvdsjE3JEAvGq3lGHSZXy28G3skua2SmVi/w4yCE6gbODqnTWlg7+wC604ydGXA8VJiS5ap43JXiUFFAaQ==" >> ~/.ssh/known_hosts

git clone git@github.com:bcwaldon/changeling.git
cd changeling/
sudo python setup.py install

external_ip=`curl http://169.254.169.254/latest/meta-data/local-ipv4`
echo "bind='$external_ip:80'" | sudo tee -a /home/ubuntu/changeling-gunicorn.conf.py

sudo ln -s /home/ubuntu/changeling.yaml /etc/changeling.yaml
sudo ln -s /home/ubuntu/changeling-gunicorn.conf.py /etc/gunicorn.d/changeling.conf.py
sudo ln -s /home/ubuntu/changeling-supervisor.conf /etc/supervisor/conf.d/changeling.conf

sudo supervisorctl reload
