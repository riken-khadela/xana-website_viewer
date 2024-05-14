# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
cd $PRJ_DIR

killall -9 python qemu-system-x86_64
pwd
. env/bin/activate

python activity/mbot.py
