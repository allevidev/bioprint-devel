#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
cd ../bioprint
sudo python setup.py install
sudo -- sh -c "echo '127.0.0.1 bioprint' >> /etc/hosts"

