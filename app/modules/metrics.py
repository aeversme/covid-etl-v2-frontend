def get_date(column):
    return column.iat[-1].date().strftime('%b %d, %Y')


def get_latest_data(column):
    data = column.iat[-1]
    return '{:,}'.format(data)


def get_delta(column, metric_type=None):
    delta = column.iat[-1] - column.iat[-2]
    if metric_type == 'rolling':
        return '{:.2f}'.format(delta)
    return '{:,}'.format(delta)
