#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function
from argparse import ArgumentParser
import json
import re
import sys

try:
    #Py3
    from urllib.parse import quote
    from urllib.request import urlopen
except ImportError:
    #Py 2.7
    from urllib import quote
    from urllib2 import urlopen
    reload(sys)
    sys.setdefaultencoding('utf8')


API = "YouDaoCV"
API_KEY = "659600698"


class Colorizing(object):
    colors = {
        'none': "",
        'default': "\033[0m",
        'bold': "\033[1m",
        'underline': "\033[4m",
        'blink': "\033[5m",
        'reverse': "\033[7m",
        'concealed': "\033[8m",

        'black': "\033[30m",
        'red': "\033[31m",
        'green': "\033[32m",
        'yellow': "\033[33m",
        'blue': "\033[34m",
        'magenta': "\033[35m",
        'cyan': "\033[36m",
        'white': "\033[37m",

        'on_black': "\033[40m",
        'on_red': "\033[41m",
        'on_green': "\033[42m",
        'on_yellow': "\033[43m",
        'on_blue': "\033[44m",
        'on_magenta': "\033[45m",
        'on_cyan': "\033[46m",
        'on_white': "\033[47m",

        'beep': "\007",
    }

    @classmethod
    def colorize(cls, s, color=None):
        if options.color == 'never':
            return s
        if options.color == 'auto' and not sys.stdout.isatty():
            return s
        if color in cls.colors:
            return "{0}{1}{2}".format(
                cls.colors[color], s, cls.colors['default'])
        else:
            return s


def online_resources(query):

    english = re.compile('^[a-z]+$', re.IGNORECASE)
    chinese = re.compile('^[\u4e00-\u9fff]+$', re.UNICODE)

    res_list = [
        (english, 'http://www.ldoceonline.com/search/?q={0}'),
        (english, 'http://dictionary.reference.com/browse/{0}'),
        (english, 'http://www.urbandictionary.com/define.php?term={0}'),
        (chinese, 'http://www.zdic.net/sousuo/?q={0}')
    ]

    return [url.format(quote(query.encode('utf-8')))
            for lang, url in res_list if lang.match(query) is not None]


def print_explanation(data, options):
    _c = Colorizing.colorize
    _d = data
    has_result = False

    query = _d['query']
    print(_c(query, 'underline'), end='')

    if 'basic' in _d:
        has_result = True
        _b = _d['basic']

        if 'phonetic' in _b:
            print(" [{0}]".format(_c(_b['phonetic'], 'yellow')))
        else:
            print()

        if 'explains' in _b:
            print(_c('  Word Explanation:', 'cyan'))
            print(*map("     * {0}".format, _b['explains']), sep='\n')
        else:
            print()

    elif 'translation' in _d:
        has_result = True
        print(_c('\n  Translation:', 'cyan'))
        print(*map("     * {0}".format, _d['translation']), sep='\n')

    else:
        print()
    if options.simple == False:
        if 'web' in _d:
            has_result = True
            print(_c('\n  Web Reference:', 'cyan'))

            web = _d['web'] if options.full else _d['web'][:3]
            print(*['     * ' + _c(ref['key'], 'yellow') +
                '\n       ' + '; '.join(map(_c('{0}', 'magenta').format, ref['value']))
                for ref in web], sep='\n')

        if not has_result:
            print(_c(' -- No result for this query.', 'red'))

        ol_res = online_resources(query)
        if len(ol_res) > 0:
            print(_c('\n  Online Resource:', 'cyan'))
            res = ol_res if options.full else ol_res[:1]
            print(*map(('     * ' + _c('{0}', 'underline')).format, res), sep='\n')

        print()

if __name__ == "__main__":
    parser = ArgumentParser(description="Youdao Console Version")
    parser.add_argument('-f', '--full',
                        action="store_true",
                        default=False,
                        help="print full web reference, only the first 3 "
                             "results will be printed without this flag.")
    parser.add_argument('-s','--simple',
                        action="store_true",
                        default=False,
                        help="only show explainations. "
                            "argument \"-f\" will not take effect")
    parser.add_argument('--color',
                        choices=['always', 'auto', 'never'],
                        default='auto',
                        help="colorize the output. "
                             "Default to 'auto' or can be 'never' or 'always'.")
    parser.add_argument('words', nargs='+', help=
                        "words to lookup, or quoted sentences to translate.")

    options = parser.parse_args()

    for word in options.words:
        word = quote(word)
        data = urlopen(
            "http://fanyi.youdao.com/openapi.do?keyfrom={0}&"
            "key={1}&type=data&doctype=json&version=1.1&q={2}"
            .format(API, API_KEY, word)).read().decode("utf-8")
        print_explanation(json.loads(data), options)
