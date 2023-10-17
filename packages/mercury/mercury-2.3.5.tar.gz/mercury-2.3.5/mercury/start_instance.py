import os
import boto3


session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)
ec2 = session.resource('ec2')
for instance in ec2.instances.all():
     print(
         "Id: {0}\nPlatform: {1}\nType: {2}\nPublic IPv4: {3}\nAMI: {4}\nState: {5}\n{6}".format(
         instance.id, instance.platform, instance.instance_type, instance.public_ip_address, instance.image.id, instance.state, instance.tags
         )
     )

print("I need GITHUB_TOKEN and MACHINE_SPELL")


user_data = """#!/bin/bash
cd /home/ubuntu

git clone https://github.com/mljar/mercury.git
export GITHUB_TOKEN=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
git clone https://${GITHUB_TOKEN}@github.com/mljar/mercury-cloud

cd mercury-cloud

cp .env.worker .env

./prepare.sh

sudo apt-get update
sudo apt install docker.io -y
sudo docker --version

sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo docker-compose version

sudo docker build -f docker/server/Dockerfile . -t wrk:latest

sudo apt install python3-pip -y
sudo pip3 install bottle requests

#curl http://checkip.amazonaws.com
#sudo python3 worker-server/wrksrv.py 

sudo apt-get install supervisor -y

sudo bash -c 'echo "[program:wrk]" >> /etc/supervisor/supervisord.conf'
sudo bash -c 'echo "command=/bin/bash -c '"'"'cd /home/ubuntu/mercury-cloud && sudo MACHINE_SPELL=smingus-dyngus-123 python3 worker-server/wrksrv.py'"'"' " >> /etc/supervisor/supervisord.conf'
sudo service supervisor force-reload

"""
# instances = ec2.create_instances(
#         MinCount=1,
#         MaxCount=1,
#         LaunchTemplate={
#             "LaunchTemplateId": "lt-011465d25b126dfed"
#         },
#         TagSpecifications=[
#             {
#                 "ResourceType": "instance",
#                 "Tags": [ 
#                     {
#                         "Key": "Name",
#                         "Value": "wrk-1"
#                     }
#                 ]
#             }
#         ],
#         BlockDeviceMappings=[
#         {
#             'DeviceName': '/dev/sda1',
#             'Ebs': {
#                 'DeleteOnTermination': True,
#                 'VolumeSize': 20,
#                 'VolumeType': 'gp3',
#                 'Encrypted': True
#             }
#         },
#     ],
#     )
