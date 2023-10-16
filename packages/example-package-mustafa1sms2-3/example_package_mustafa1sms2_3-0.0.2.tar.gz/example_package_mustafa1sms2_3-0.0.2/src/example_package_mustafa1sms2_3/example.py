from datetime import datetime, timedelta
import pytz

def add_one(number):
    return number + 1

def get_current_readable_timestamp():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return str(datetime.now(ist_timezone).strftime('%Y-%m-%d %H:%M:%S'))      