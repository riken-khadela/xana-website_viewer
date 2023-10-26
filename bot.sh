

# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory


cd /home/hp20/workspace/website_viewer
# $PRJ_DIR
. env/bin/activate
pwd
pwd
python3 bot.py  
# update code
# git pull origin $(git rev-parse --abbrev-ref HEAD)

# setup database
# python manage.py setup --database

# python manage.py check_jobs 
