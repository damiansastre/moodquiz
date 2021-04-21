import re
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def pad_line(line):
    return (12 * ' ') + line

def parse_test_body(data):
    res = []
    string_started = False
    for d in data.split('\n'):
        if d.startswith('"""') and d.endswith('"""') and d != '"""':
            res.append(pad_line(d))
        elif '"""' in d and not string_started:
            string_started = True
            res.append(pad_line(d))
        elif '"""' in d and string_started:
            string_started = False
            res.append(d)
        elif string_started:
            res.append(d)
        else:
            res.append(pad_line(d))
    return '\n'.join(res)


def valid_url(url):
    return re.match(regex, url) is not None

