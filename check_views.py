from dbb import get_views_per_day
views_per_day = get_views_per_day()
body = ''
for date, count in views_per_day.items():
    print(f"Date: {date}, Total Views: {count}")