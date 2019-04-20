# YouDao Console Version

Simple wrapper for Youdao online translate (Chinese <-> English) service [API](https://ai.youdao.com/docs/doc-trans-api.s#p01), as an alternative to the StarDict Console Version(sdcv).

## 本项目终止公众服务

不出所料地，自去年底切换到按量收费API后，ydcv的API Key终于被滥用至欠费状态了。作为小众工具，平时每天API调用开支都在0.2元以内，而4月7、8、20日几天，分别突发消费了8.74、8.87、45.71元，API账户已经是欠费状态，本项目正式终止公众服务。

其他用户若要继续使用，请自行前往[有道智云](https://ai.youdao.com)开通“自然语言翻译服务-文本翻译”的应用，并把自己的API Key和Secret填入源码对应位置即可。

## 注意

[有道翻译API](http://fanyi.youdao.com/openapi?path=data-mode) 将于 2018-12-31 后停止运行，改由“有道云-有道智云文本翻译” 提供兼容的服务；目前本项目代码已经匹配升级，但是按照文档说法，有道智云API是“按量收费”，目前账户内有100元体验金，具体收费计算方式尚不明确，项目工具的用户量不明确，而又本项目开源，所用服务标识的ID/SECRET也可能被他人使用，因而此后本项目功能存在不确定性。


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

