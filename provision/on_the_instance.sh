# A small NaaS (Notes as a script) about how to configure the kali image

cd ~
sudo apt-get -y update
sudo apt-get install -y git debootstrap


sudo ln -sf /usr/share/debootstrap/scripts/{wheezy,sana}

git clone https://github.com/wakaru44/kali-cloud-build

cd kali-cloud-build

echo "Esto no me mola"
exit 1

sudo ./kali-cloud-build ec2 --secret-key xxxxxxxxxxxxx --access-key xxxxxxxxxxxxx
