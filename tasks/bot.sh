# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory
cd $PRJ_DIR
# . tasks/environment.sh

# Kill python and AVD process
killall -9 python qemu-system-x86_64

# activate the virtual environment for python
#. env/bin/activate
pwd
. env/bin/activate

# update code
# git checkout old-insta-rk
git stash
git pull
python activity/mbot.py
