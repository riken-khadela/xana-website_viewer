from driver import driver_class, measure_time
from xana_app import run_xana_app_activities
from xana_net import run_xana_net_activities
from xana_insta import run_xana_insta_activities
from xana_twitter import run_xana_twitter_activities
from xana_youtube import run_xana_youtube_activities
from xana_discord import run_xana_discord_activities
import random
views_links = [
    "https://xana.net/app",
    "https://xana.net/",
    ]

class Xana_bot(driver_class):
    def __init__(self) -> None:
        self.driver =self.get_driver()
        self.driver.get(views_links[-1])
        self.random_sleep()
        pass
    
bt = Xana_bot()
activities_func_li = [
        run_xana_app_activities,
        run_xana_net_activities,
        run_xana_insta_activities,
        run_xana_twitter_activities,
        run_xana_youtube_activities,
        run_xana_discord_activities,
    ]

random.shuffle(activities_func_li)

for func in activities_func_li :
    breakpoint()
    func(bt.driver)
    ...