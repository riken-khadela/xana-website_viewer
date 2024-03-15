from dbb import get_views_per_day, add_data_with_view, create_db_ifnot
from datetime import datetime
create_db_ifnot()
# add_data_with_view(datetime.now().strftime("%d/%m/%Y"), True)
views_per_day = get_views_per_day()
body = ''
for date, count in views_per_day.items():
    print(f"Date: {date}, Total Views: {count}")