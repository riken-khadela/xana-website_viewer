# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
cd $PRJ_DIR

. env/bin/activate

python cmd/cmds.py
