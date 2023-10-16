from datetime import date, timedelta


def get_monday(the_date: date):
    return the_date - timedelta(days=(the_date.isoweekday() - 1))


def format_header_date(the_date: date):
    return the_date.strftime("%A %d %B %Y")


def format_file_date(the_date: date):
    return the_date.strftime("%Y-%m-%d")


def get_time_delta_from_options(options):
    if options.thisWeek:
        delta = timedelta(0)
    elif options.lastWeek:
        delta = timedelta(-7)
    elif options.nextWeek:
        delta = timedelta(7)
    else:
        raise ValueError("No week option supplied.")

    return delta
