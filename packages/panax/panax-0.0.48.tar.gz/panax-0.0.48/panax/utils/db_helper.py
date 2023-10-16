import datetime


def row_to_dict(cursor, row):
    """将返回结果转换为dict"""
    d = {}
    for idx, col in enumerate(cursor.description):
        if str(col[0]).startswith('_'):
            continue

        d[col[0]] = row[idx]
        if isinstance(row[idx], datetime.datetime):
            d[col[0]] = row[idx].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(row[idx], datetime.date):
            d[col[0]] = row[idx].strftime('%Y-%m-%d')
        else:
            d[col[0]] = row[idx]
    return d