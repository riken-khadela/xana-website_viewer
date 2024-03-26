
# project path
export CURRENT_DIR=`dirname $(readlink -f $0)`
export PRJ_DIR=`dirname $CURRENT_DIR`
# go to project root directory
cd $PRJ_DIR

# Check if variable.sh file exists
if [ ! -f "tasks/variable.sh" ]; then
    echo "Variable file not found. Running python3 create_task.py..."
    python3 create_task.py
fi

# python3 cron_scheduler.py
# Replace the line in environment.sh
sed -i '/export LESSCLOSE=\/usr\/bin\/lesspipe %s %s/d' tasks/environment.sh


#. ./tasks/environment.sh

. tasks/environment.sh
. env/bin/activate
chmod +x tasks/variable.sh
. tasks/variable.sh

killall -9 python qemu-system-x86_64
# Kill python and AVD process
# export SENDER_PASSWORD='hfac mvld ecjx clru'
# export RECEIVER_MAIL="rikenkhadela22@gmail.com"
# export SENDER_MAIL='rikenkhadela777@gmail.com'
# export SYSTEM_NO='RK'
# activate the virtual environment for python
#. env/bin/activate

# echo "1234" | sudo -S systemctl restart systemd-resolved

# update code
git checkout old-insta-rk
git stash
git pull 
python3 bot.py  
# update code
# git pull origin $(git rev-parse --abbrev-ref HEAD)

# setup database
# python manage.py setup --database

# python manage.py check_jobs 
