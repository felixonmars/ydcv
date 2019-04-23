#!/usr/bin/env python
# coding=UTF-8
from __future__ import unicode_literals
from __future__ import print_function
from argparse import ArgumentParser
import subprocess
from subprocess import check_output, call, Popen
from time import sleep
from distutils import spawn
from tempfile import NamedTemporaryFile
import json
import re
import sys
import platform
import hashlib
import random
import os
import configparser

try:
    # Py3
    from urllib.parse import quote
    from urllib.request import urlopen
except ImportError:
    # Py 2.7
    from urllib import quote
    from urllib2 import urlopen
    reload(sys)
    sys.setdefaultencoding('utf8')
    input = raw_input

YDAPPID = os.getenv('YDCV_YOUDAO_APPID', '')
YDAPPSEC = os.getenv('YDCV_YOUDAO_APPSEC', '')

class GlobalOptions(object):
    def __init__(self, options=None):
        self._options = options

    def __getitem__(self, name):
        return self._options.__dict__.get(name)

    def __getattr__(self, name):
        if name in dir(GlobalOptions) or name in self.__dict__:
            return getattr(self, name)
        elif name in self._options.__dict__:
            return getattr(self._options, name)
        else:
            raise AttributeError("'%s' has no attribute '%s'" % (
                self.__class__.__name__, name))

options = GlobalOptions()


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


_re_non_english = re.compile(r'[^\w]', re.ASCII)
_re_english = re.compile('^[a-z]+$', re.IGNORECASE)
_re_chinese = re.compile('^[\u4e00-\u9fff]+$', re.UNICODE)

def online_resources(query):

    res_list = [
        (_re_english, 'http://www.ldoceonline.com/search/?q={0}'),
        (_re_english, 'http://dictionary.reference.com/browse/{0}'),
        (_re_english, 'http://www.urbandictionary.com/define.php?term={0}'),
        (_re_chinese, 'http://www.zdic.net/sousuo/?q={0}')
    ]

    return [url.format(quote(query.encode('utf-8')))
            for lang, url in res_list if lang.match(query) is not None]


def print_explanation(orig_word, data, options):
    _c = Colorizing.colorize
    _d = data
    has_result = False
    _accent_urls = dict()

    # query	text	源语言	查询正确时，一定存在(并不)
    # 当FROM和TO的值有在{zh-CHS, EN}范围外的时候，小语种翻译不带词汇结构以及'query'字段
    query = _d.get('query', orig_word)
    print(_c(query, 'underline'), end='')

    # basic	text	词义	基本词典,查词时才有
    if 'basic' in _d and _d['basic'] is not None:
        has_result = True
        _b = _d['basic']

        try:
            # us-phonetic	美式音标，英文查词成功，一定存在
            # uk-phonetic	英式音标，英文查词成功，一定存在
            # phonetic	默认音标，默认是英式音标，英文查词成功，一定存在
            if 'uk-phonetic' in _b and 'us-phonetic' in _b:
                print(" UK: [{0}]".format(_c(_b['uk-phonetic'], 'yellow')), end=',')
                print(" US: [{0}]".format(_c(_b['us-phonetic'], 'yellow')))
            elif 'phonetic' in _b:
                print(" [{0}]".format(_c(_b['phonetic'], 'yellow')))
            else:
                print()
        except UnicodeEncodeError:
            print(" [ ---- ] ")

        # uk-speech	英式发音，英文查词成功，一定存在
        # us-speech	美式发音，英文查词成功，一定存在
        if options.speech and 'speech' in _b:
            print(_c('  Text to Speech:', 'cyan'))
            if 'us-speech' in _b and 'uk-speech' in _b:
                print("     * UK:", _b['uk-speech'])
                print("     * US:", _b['us-speech'])
            elif 'speech' in _b:
                print("     *", _b['speech'])
            for _accent in ('speech', 'uk-speech', 'us-speech'):
                if _accent in _b:
                    _accent_urls.update({_accent.split('-')[0]: _b[_accent]})
            print()

        # explains	基本释义
        # 中文查词的basic字段只包含explains字段。
        if 'explains' in _b:
            print(_c('  Word Explanation:', 'cyan'))
            print(*map("     * {0}".format, _b['explains']), sep='\n')
        else:
            print()

    # translation	text	翻译结果	查询正确时一定存在
    elif 'translation' in _d:
        has_result = True
        print(_c('\n  Translation:', 'cyan'))
        print(*map("     * {0}".format, _d['translation']), sep='\n')
    else:
        print()

    if options.simple is False:
        # Web reference
        # web	text	词义	网络释义，该结果不一定存在
        if 'web' in _d:
            has_result = True
            print(_c('\n  Web Reference:', 'cyan'))

            web = _d['web'] if options.full else _d['web'][:3]
            print(*[
                '     * {0}\n       {1}'.format(
                    _c(ref['key'], 'yellow'),
                    '; '.join(map(_c('{0}', 'magenta').format, ref['value']))
                ) for ref in web], sep='\n')

        # Online resources
        ol_res = online_resources(query)

        if len(ol_res) > 0:
            print(_c('\n  Online Resource:', 'cyan'))
            res = ol_res if options.full else ol_res[:1]
            print(*map(('     * ' + _c('{0}', 'underline')).format, res), sep='\n')

        # read out the word
        if options.read:
            print()
            sys_name = platform.system()
            if 'Darwin' == sys_name:
                call(['say', query])
            elif 'Linux' == sys_name:
                if not spawn.find_executable(options.player):
                    print(_c(' -- Player ' + options.player + ' is not found in system, ', 'red'))
                    print(_c('    acceptable players are: festival, mpg123, sox and mpv', 'red'))
                    print(_c(' -- Please install your favourite player: ', 'blue'))
                    print(_c('    - festival (http://www.cstr.ed.ac.uk/projects/festival/),'))
                    print(_c('    - mpg123 (http://www.mpg123.de/),'))
                    print(_c('    - SoX (http://sox.sourceforge.net/),'))
                    print(_c('    - mpv (https://mpv.io).'))
                else:
                    if options.player == 'festival':
                        p = Popen(['festival', '--tts'], stdin=subprocess.PIPE)
                        p.communicate(query.encode('utf-8'))
                        p.wait()
                    else:
                        accent = options.accent if options.accent != 'auto' else 'speech'
                        accent_url = _accent_urls.get(accent, '')
                        if not accent_url:
                            print(_c(' -- URL to speech audio for accent {} not found.'.format(options.accent), 'red'))
                            if not options.speech:
                                print(_c(' -- Maybe you forgot to add -S option?'), 'red')
                        elif options.player == 'mpv':
                            call(['mpv', '--really-quiet', accent_url])
                        else:
                            with NamedTemporaryFile(suffix=".mp3") as accent_file:
                                if call(['curl', '-s', accent_url, '-o', accent_file.name]) != 0:
                                    print(_c('Network unavailable or permission error to write file: {}'.format(accent_file), 'red'))
                                else:
                                    if options.player == 'mpg123':
                                        call(['mpg123', '-q', accent_file.name])
                                    elif options.player == 'sox':
                                        call(['play', '-q', accent_file.name])

    if not has_result:
        print(_c(' -- No result for this query.', 'red'))

    print()


def lookup_word(word):
    if word == '\q' or word == ':q':
        sys.exit("Thanks for using, goodbye!")

    # 输入语言非英语词汇，使用auto模式。
    _lang_from = options["from"]
    _lang_to = options["to"]

    if _re_non_english.match(word) is not None and _lang_from == 'EN':
        _lang_from = 'auto'

    if _re_chinese.match(word) is not None:
        _lang_to = 'EN'

    salt = str(random.randint(1, 65536))
    md5 = hashlib.md5()
    md5.update("{}{}{}{}".format(YDAPPID,word,salt,YDAPPSEC).encode('utf-8'))
    sign = md5.hexdigest()
    yd_api = "https://openapi.youdao.com/api?" \
            "appKey={}&q={}&from={}&to={}&salt={}&sign={}".format(
            YDAPPID, quote(word), _lang_from, _lang_to, salt, sign)

    try:
        data = urlopen(yd_api).read().decode("utf-8")
    except IOError:
        print("Network is unavailable")
    else:
        try:
            formatted = json.loads(data)
            err_code = formatted["errorCode"]
            if err_code != "0":
                print("Req: {}\n ErrorCode {}".format(yd_api, err_code))
                print("Please refer to: http://ai.youdao.com/docs/doc-trans-api.s#p08")
                return

            print_explanation(word, formatted, options)
        except ValueError:
            print("Cannot parse response data, original response: \n{}".format(data))


def arg_parse():
    parser = ArgumentParser(description="Youdao Console Version")
    parser.add_argument('-f', '--full',
                        action="store_true",
                        default=False,
                        help="print full web reference, only the first 3 "
                             "results will be printed without this flag.")
    parser.add_argument('-s', '--simple',
                        action="store_true",
                        default=False,
                        help="only show explainations. "
                             "argument \"-f\" will not take effect.")
    parser.add_argument('-S', '--speech',
                        action="store_true",
                        default=False,
                        help="print URL to speech audio.")
    parser.add_argument('-r', '--read',
                        action="store_true",
                        default=False,
                        help="read out the word with player provided by \"-p\" option.")
    parser.add_argument('-p', '--player',
                        choices=['festival', 'mpg123', 'sox', 'mpv'],
                        default='festival',
                        help="read out the word with this play."
                             "Default to 'festival' or can be 'mpg123', 'sox', 'mpv'."
                             "-S option is required if player is not festival."
                        )
    parser.add_argument('-a', '--accent',
                        choices=['auto', 'uk', 'us'],
                        default='auto',
                        help="set default accent to read the word in. "
                             "Default to 'auto' or can be 'uk', or 'us'."
                        )
    parser.add_argument('-x', '--selection',
                        action="store_true",
                        default=False,
                        help="show explaination of current selection.")
    parser.add_argument('--color',
                        choices=['always', 'auto', 'never'],
                        default='auto',
                        help="colorize the output. "
                             "Default to 'auto' or can be 'never' or 'always'.")
    parser.add_argument('-F', '--from',
                        action="store",
                        choices=["zh-CHS", "ja", "EN", "ko", "fr", "ru", "pt", "es", "vi", "de", "ar", "id"],
                        default='EN',
                        help="Translate from specific language. Default: 'EN' for ascii only lookup, 'auto' for non-ascii characters.")

    parser.add_argument('-t', '--to',
                        action="store",
                        choices=["zh-CHS", "ja", "EN", "ko", "fr", "ru", "pt", "es", "vi", "de", "ar", "id"],
                        default='zh-CHS',
                        help="Translate to specific language. "
                        "Default: zh-CHS for non-chinese characters, EN if Chinese character queried.")
    parser.add_argument('-c', '--config',
                        action="store",
                        default="~/.ydcv",
                        help="Config file contains API AppKey / SecKey. Default: ~/.ydcv")
    parser.add_argument('words',
                        nargs='*',
                        help="words to lookup, or quoted sentences to translate.")
    return parser.parse_args()


def main():
    global YDAPPID, YDAPPSEC
    options._options = arg_parse()

    if YDAPPID == "" or YDAPPSEC == "":
        config = configparser.ConfigParser()
        config.read(os.path.expanduser(options.config))
        sec = config["YDCV"]
        YDAPPID = sec["YDAPPID"]
        YDAPPSEC = sec["YDAPPSEC"]

    if options.words:
        for word in options.words:
            lookup_word(word)
    else:
        if options.selection:
            last = check_output(["xclip", "-o"], universal_newlines=True)
            print("Waiting for selection>")
            while True:
                try:
                    sleep(0.1)
                    curr = check_output(["xclip", "-o"], universal_newlines=True)
                    if curr != last:
                        last = curr
                        if last.strip():
                            lookup_word(last)
                        print("Waiting for selection>")
                except (KeyboardInterrupt, EOFError):
                    break
        else:
            try:
                import readline
            except ImportError:
                pass
            while True:
                try:
                    words = input('> ')
                    if words.strip():
                        lookup_word(words)
                except KeyboardInterrupt:
                    print()
                    continue
                except EOFError:
                    break
        print("\nBye")

if __name__ == "__main__":
    main()
