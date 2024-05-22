from driver import driver_class, measure_time
from xana_app import run_xana_app_activities
from xana_net import run_xana_net_activities
from xana_insta import run_xana_insta_activities
from xana_twitter import run_xana_twitter_activities
from xana_youtube import run_xana_youtube_activities
from xana_discord import run_xana_discord_activities
from dbb import create_db_ifnot
import random
views_links = [
    "https://xana.net/app",
    "https://xana.net/",
    ]

class Xana_bot(driver_class):
    def __init__(self,vpn=False) -> None:
        self.driver =self.get_driver(vpn)
        self.driver.get(views_links[-1])
        self.random_sleep()
        pass
    
activities_func_li = [
        run_xana_app_activities,
        run_xana_net_activities,
        run_xana_insta_activities,
        run_xana_twitter_activities,
        run_xana_youtube_activities,
        run_xana_discord_activities,
    ]




import argparse
from concurrent import futures

num_threads = 5

def main(vpn=False):
    active_threads = set()

    def start_new_thread():
        while True:
            random.shuffle(activities_func_li)
            bt = Xana_bot(vpn=vpn)
            if bt.driver :
                for func in activities_func_li :
                    func(bt.driver)
    
    # Start the initial threads
    with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            future = executor.submit(start_new_thread)
            active_threads.add(future)

        # Monitor and replace completed threads
        while True:
            completed = futures.wait(active_threads, return_when=futures.FIRST_COMPLETED).done
            for thread in completed:
                active_threads.remove(thread)
                new_thread = executor.submit(start_new_thread)
                active_threads.add(new_thread)
                
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vpn", help="Connect to VPN", action="store_true", default=False)
    args = parser.parse_args()
    create_db_ifnot()
    main(vpn=args.vpn)
                
