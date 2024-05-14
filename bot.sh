
# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory

cd $PRJ_DIR
pwd
killall -9 python qemu-system-x86_64
cd /home/rk/Desktop/xana-website_viewer/
# git stash
# git pull 
. env/bin/activate
python activity/mbot.py

