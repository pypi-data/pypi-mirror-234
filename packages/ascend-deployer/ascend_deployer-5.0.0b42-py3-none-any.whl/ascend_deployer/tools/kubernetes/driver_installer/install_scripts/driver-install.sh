#!/bin/bash

ping -c 1 172.17.0.1 > /dev/null

if [ $? -eq 0 ];then
  hostIp=172.17.0.1
else
  hostIp=$(ip route|awk '/default/ {print $3}')
fi


mkdir -p /root/.ssh /mnt/.ssh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
cat ~/.ssh/id_rsa.pub >> /mnt/.ssh/authorized_keys

cd /root
cp *-driver*.run /mnt
cp *firmware*.run /mnt
cp install.sh /mnt

mkdir -p /mnt/pkgs
cp *.deb /mnt/pkgs
cp *.rpm /mnt/pkgs

ssh -o "StrictHostKeyChecking=no" root@$hostIp groupadd -g 1000 HwHiAiUser
ssh root@$hostIp useradd -g HwHiAiUser -u 1000 -d /home/HwHiAiUser -m HwHiAiUser -s /bin/bash

if ssh root@$hostIp command -v dpkg >/dev/null 2>&1; then
  ssh root@$hostIp dpkg --force-all -i /root/pkgs/*.deb
elif ssh root@$hostIp command -v rpm >/dev/null 2>&1; then
  ssh root@$hostIp rpm -iUv /root/pkgs/*.rpm --nodeps --force
else
  echo "Unknown package manager"
fi

installed=$(ssh root@$hostIp find /usr/local/Ascend/driver -name "upgrade-tool"|wc -l)
if [ $installed -eq 0 ];then
  ssh root@$hostIp bash /root/*-driver*.run --nox11 --full --install-for-all --quiet
  ssh root@$hostIp bash /root/*firmware*.run --nox11 --full --quiet
else
  ssh root@$hostIp bash /root/*firmware*.run --nox11 --upgrade --quiet
  ssh root@$hostIp bash /root/*-driver*.run --nox11 --upgrade --quiet
fi

interval=5

while (true); do
  ssh root@$hostIp npu-smi info > /dev/null
  if [ $? -eq 0 ];then
    sleep $interval
  else
    exit 1
  fi
done
