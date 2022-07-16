import time

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']


def custom_epoch(days):
    """

    :param days:
    :return:
    """
    current_time = time.time()
    seconds_in_day = days * (24 * 60 * 60)
    required_time = current_time - seconds_in_day
    return int(required_time)


def custom_date(days):
    epoch_time = custom_epoch(days)
    year = time.localtime(epoch_time)[0]
    month = time.localtime(epoch_time)[1]
    date = time.localtime(epoch_time)[2]
    months_in_name = MONTHS[month - 1]
    return f"{date} {months_in_name}, {year}"



