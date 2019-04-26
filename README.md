# YouDao Console Version

Simple wrapper for Youdao online translate (Chinese <-> English) service [API](https://ai.youdao.com/docs/doc-trans-api.s#p01), as an alternative to the StarDict Console Version(sdcv).

## 注意

本工具已经停止公共服务。用户若要继续使用，需申请一个私人的[有道智云](https://ai.youdao.com) API Key配置使用。
大致步骤为： 翻译实例-创建实例-选"文本翻译"， 我的应用-创建应用-接入方式：API-选择绑定刚才创建的`自然语言翻译服务-文本翻译`实例。
得到的`应用ID` / `应用密钥`即为本工具的`YDAPPID`/`YDAPPSEC`。

本工具可通过环境变量`YDCV_YOUDAO_APPID`和`YDCV_YOUDAO_APPSEC`和ini文件方式配置key。配置文件默认为`~/.ydcv`，也可用`--config`指定。
配置文件例子：
```
[YDCV]
YDAPPID=123456
YDAPPSEC=abcd1234
```

## Usage
```
$ ydcv --help
usage: ydcv.py [-h] [-f] [-s] [-S] [-r] [-p {festival,mpg123,sox,mpv}]
               [-a {auto,uk,us}] [-x] [--color {always,auto,never}]
               [-F {zh-CHS,ja,EN,ko,fr,ru,pt,es,vi,de,ar,id}]
               [-t {zh-CHS,ja,EN,ko,fr,ru,pt,es,vi,de,ar,id}]
               [words [words ...]]

Youdao Console Version

positional arguments:
  words                 words to lookup, or quoted sentences to translate.

optional arguments:
  -h, --help            show this help message and exit
  -f, --full            print full web reference, only the first 3 results
                        will be printed without this flag.
  -s, --simple          only show explainations. argument "-f" will not take
                        effect.
  -S, --speech          print URL to speech audio.
  -r, --read            read out the word with player provided by "-p" option.
  -p {festival,mpg123,sox,mpv}, --player {festival,mpg123,sox,mpv}
                        read out the word with this play.Default to 'festival'
                        or can be 'mpg123', 'sox', 'mpv'.-S option is required
                        if player is not festival.
  -a {auto,uk,us}, --accent {auto,uk,us}
                        set default accent to read the word in. Default to
                        'auto' or can be 'uk', or 'us'.
  -x, --selection       show explaination of current selection.
  --color {always,auto,never}
                        colorize the output. Default to 'auto' or can be
                        'never' or 'always'.
  -F {zh-CHS,ja,EN,ko,fr,ru,pt,es,vi,de,ar,id}, --from {zh-CHS,ja,EN,ko,fr,ru,pt,es,vi,de,ar,id}
                        Translate from specific language. Default: EN
  -t {zh-CHS,ja,EN,ko,fr,ru,pt,es,vi,de,ar,id}, --to {zh-CHS,ja,EN,ko,fr,ru,pt,es,vi,de,ar,id}
                        Translate to specific language. Default: zh-CHS
  -c CONFIG, --config CONFIG
                        Config file contains API AppKey / SecKey. Default: ~/.ydcv
          
```

## 翻译支持的语言列表

`--from` 和 `--to`参数可以指定特定语言之间相互翻译，但只有中文结果有词典内容

|语言|代码|语言|代码|语言|代码|语言|代码|
|----|----|----|----|----|----|----|----|
中文|zh-CHS|葡萄牙文|pt  |韩文|ko|德文    |de
日文|ja    |西班牙文|es  |法文|fr|阿拉伯文|ar
英文|EN    |越南文  |vi  |俄文|ru|印尼文  |id

## Installation
```
pip install ydcv
```

## Environment
 * Python ( >=2.7, 3.x )

## Similar Projects on github
|Lang|Project|Author|
|----|----|----|
|Go|[ydgo](https://github.com/boypt/ydgo)|boypt|
|RUST|[ydcv-rs](https://github.com/farseerfc/ydcv-rs)|farseerfc|
|RUST|[ydcv-rust](https://github.com/passchaos/ydcv-rust)|passchaos|
|Powershell|[ydcv.ps1](https://github.com/atupal/ydcv.ps1)|atupal|
|BASH|[ydcv-bash-version](https://github.com/MasterCsquare/ydcv-bash-version)|MasterCsquare|
|Perl|[ydcv](https://github.com/JaHIY/ydcv)|JaHIY|
|C|[cydcv](https://github.com/proudzhu/cydcv)|proudzhu|
|C++|[ydcv-cpp](https://github.com/proudzhu/ydcv-cpp)|proudzhu|
|Vim|[ydcv.vim](https://github.com/bennyyip/ydcv.vim)|bennyyip|
|Erlang|[ydcv-el](https://github.com/zhenglinj/ydcv-el)|zhenglinj|
|Haskell|[ydcv-hs](https://github.com/proudzhu/ydcv-hs)|proudzhu|

