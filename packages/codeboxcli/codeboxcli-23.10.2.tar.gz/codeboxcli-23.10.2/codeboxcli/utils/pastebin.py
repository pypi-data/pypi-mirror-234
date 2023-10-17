# -*- coding: utf-8 -*-
import locale

import requests

from codeboxcli.utils import messages

# Extract the language code part
language_code = locale.getlocale()
if language_code:
    language_code = language_code[0].split('_')[0]


def post(name, content, expire_date, dev_key):
    global language_code

    expire_date_options = ["N", "10M", "1H",
                           "1D", "1W", "2W", "1M", "6M", "1Y"]

    if not (expire_date in expire_date_options):
        expire_date = "1W"

    data = {
        'api_dev_key': dev_key,
        'api_paste_code': content.replace("'", ""),
        'api_option': 'paste',
        'api_paste_name': name.replace("'", ""),
        'api_paste_expire_date': expire_date
    }

    response = requests.post(
        'https://pastebin.com/api/api_post.php', data=data)

    if response.status_code == 200:
        print(messages.share_url(response.content.decode("utf-8"), language_code))
    else:
        print(messages.share_error(response.content.decode("utf-8"), language_code))
