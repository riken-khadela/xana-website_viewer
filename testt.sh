
killall -9 python qemu-system-x86_64
cd /home/hp20/workspace/website_viewer
. env/bin/activate
python3 shtest.py  > output.log
python3 bot.py  > output.log

