#!/usr/bin/env python
# coding=UTF-8
from __future__ import unicode_literals
from __future__ import print_function
from argparse import ArgumentParser
import subprocess
from subprocess import check_output, call, Popen
from time import sleep
from tempfile import NamedTemporaryFile
import json
import re
import shutil
from shutil import which
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
# https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
ERROR = {
    "101": "缺少必填的参数,首先确保必填参数齐全，然后确认参数书写是否正确。",
    "102": "不支持的语言类型",
    "103": "翻译文本过长",
    "104": "不支持的API类型",
    "105": "不支持的签名类型",
    "106": "不支持的响应类型",
    "107": "不支持的传输加密类型",
    "108": "应用ID无效，注册账号，登录后台创建应用并完成绑定，可获得应用ID和应用密钥等信息",
    "109": "batchLog格式不正确",
    "110": "无相关服务的有效应用,应用没有绑定服务应用，可以新建服务应用。注：某些服务的翻译结果发音需要tts服务，需要在控制台创建语音合成服务绑定应用后方能使用。",
    "111": "开发者账号无效",
    "112": "请求服务无效",
    "113": "翻译文本不能为空",
    "114": "不支持的图片传输方式",
    "116": "strict字段取值无效，请参考文档填写正确参数值",
    "201": "解密失败，可能为DES,BASE64,URLDecode的错误",
    "202": "签名检验失败,如果确认应用ID和应用密钥的正确性，仍返回202，一般是编码问题。请确保翻译文本为UTF-8编码.",
    "203": "访问IP地址不在可访问IP列表",
    "205": "请求的接口与应用的平台类型不一致，确保接入方式（Android SDK、IOS SDK、API）与创建的应用平台类型一致。如有疑问请参考入门指南",
    "206": "因为时间戳无效导致签名校验失败",
    "207": "重放请求",
    "301": "辞典查询失败",
    "302": "翻译查询失败",
    "303": "服务端的其它异常",
    "304": "会话闲置太久超时",
    "401": "账户已经欠费，请进行账户充值",
    "402": "offlinesdk不可用",
    "411": "访问频率受限,请稍后访问",
    "412": "长请求过于频繁，请稍后访问",
    "1001": "无效的OCR类型",
    "1002": "不支持的OCR image类型",
    "1003": "不支持的OCR Language类型",
    "1004": "识别图片过大",
    "1201": "图片base64解密失败",
    "1301": "OCR段落识别失败",
    "1411": "访问频率受限",
    "1412": "超过最大识别字节数",
    "2003": "不支持的语言识别Language类型",
    "2004": "合成字符过长",
    "2005": "不支持的音频文件类型",
    "2006": "不支持的发音类型",
    "2201": "解密失败",
    "2301": "服务的异常",
    "2411": "访问频率受限,请稍后访问",
    "2412": "超过最大请求字符数",
    "3001": "不支持的语音格式",
    "3002": "不支持的语音采样率",
    "3003": "不支持的语音声道",
    "3004": "不支持的语音上传类型",
    "3005": "不支持的语言类型",
    "3006": "不支持的识别类型",
    "3007": "识别音频文件过大",
    "3008": "识别音频时长过长",
    "3009": "不支持的音频文件类型",
    "3010": "不支持的发音类型",
    "3201": "解密失败",
    "3301": "语音识别失败",
    "3302": "语音翻译失败",
    "3303": "服务的异常",
    "3411": "访问频率受限,请稍后访问",
    "3412": "超过最大请求字符数",
    "4001": "不支持的语音识别格式",
    "4002": "不支持的语音识别采样率",
    "4003": "不支持的语音识别声道",
    "4004": "不支持的语音上传类型",
    "4005": "不支持的语言类型",
    "4006": "识别音频文件过大",
    "4007": "识别音频时长过长",
    "4201": "解密失败",
    "4301": "语音识别失败",
    "4303": "服务的异常",
    "4411": "访问频率受限,请稍后访问",
    "4412": "超过最大请求时长",
    "5001": "无效的OCR类型",
    "5002": "不支持的OCR image类型",
    "5003": "不支持的语言类型",
    "5004": "识别图片过大",
    "5005": "不支持的图片类型",
    "5006": "文件为空",
    "5201": "解密错误，图片base64解密失败",
    "5301": "OCR段落识别失败",
    "5411": "访问频率受限",
    "5412": "超过最大识别流量",
    "9001": "不支持的语音格式",
    "9002": "不支持的语音采样率",
    "9003": "不支持的语音声道",
    "9004": "不支持的语音上传类型",
    "9005": "不支持的语音识别 Language类型",
    "9301": "ASR识别失败",
    "9303": "服务器内部错误",
    "9411": "访问频率受限（超过最大调用次数）",
    "9412": "超过最大处理语音长度",
    "10001": "无效的OCR类型",
    "10002": "不支持的OCR image类型",
    "10004": "识别图片过大",
    "10201": "图片base64解密失败",
    "10301": "OCR段落识别失败",
    "10411": "访问频率受限",
    "10412": "超过最大识别流量",
    "11001": "不支持的语音识别格式",
    "11002": "不支持的语音识别采样率",
    "11003": "不支持的语音识别声道",
    "11004": "不支持的语音上传类型",
    "11005": "不支持的语言类型",
    "11006": "识别音频文件过大",
    "11007": "识别音频时长过长，最大支持30s",
    "11201": "解密失败",
    "11301": "语音识别失败",
    "11303": "服务的异常",
    "11411": "访问频率受限,请稍后访问",
    "11412": "超过最大请求时长",
    "12001": "图片尺寸过大",
    "12002": "图片base64解密失败",
    "12003": "引擎服务器返回错误",
    "12004": "图片为空",
    "12005": "不支持的识别图片类型",
    "12006": "图片无匹配结果",
    "13001": "不支持的角度类型",
    "13002": "不支持的文件类型",
    "13003": "表格识别图片过大",
    "13004": "文件为空",
    "13301": "表格识别失败",
    "15001": "需要图片",
    "15002": "图片过大（1M）",
    "15003": "服务调用失败",
    "17001": "需要图片",
    "17002": "图片过大（1M）",
    "17003": "识别类型未找到",
    "17004": "不支持的识别类型",
    "17005": "服务调用失败",
}

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
                if not shutil.which(options.player):
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
                _c = Colorizing.colorize
                print(_c(ERROR.get(err_code, "Unknown error!"), 'red'))
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
                        help="only show explanations. "
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
                        help="show explanation of current selection.")
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
        try:
            sec = config["YDCV"]
        except KeyError:
            print("Cannot find the API key.")
            print("Please refer to: https://github.com/felixonmars/ydcv#%E6%B3%A8%E6%84%8F")
            sys.exit()
        YDAPPID = sec["YDAPPID"]
        YDAPPSEC = sec["YDAPPSEC"]

    if options.words:
        for word in options.words:
            lookup_word(word)
    else:
        if options.selection:
            from shutil import which
            from shlex import split
            # don't use try/catch to call these program, it will cost more time
            # than judge existence of these program by `which()`
            if options._options.cmd:
                cmd = split(options._options.cmd)
            elif which("xsel"):
                cmd = split("xsel -o")
            elif which("xclip"):
                cmd = split("xclip -o")
                # TODO: add more clipboard tool: windows' clip, cygwin's
                # putclip, nvim's win32yank, etc
            else:
                sys.exit("Please install xsel/xclip first!")
            last = check_output(cmd, universal_newlines=True)
            print("Waiting for selection>")
            while True:
                try:
                    sleep(0.1)
                    curr = check_output(cmd, universal_newlines=True)
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
