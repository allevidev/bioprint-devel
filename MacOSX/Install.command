#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd /System/Library/Extensions/IOUSBFamily.kext/Contents/PlugIns 
sudo mv AppleUSBFTDI.kext AppleUSBFTDI.disabled 
sudo touch /System/Library/Extensions

cd $DIR
cd ../bioprint
sudo python setup.py install
sudo -- sh -c "echo '127.0.0.1 bioprint' >> /etc/hosts"

sudo reboot

