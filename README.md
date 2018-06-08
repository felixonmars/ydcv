# YouDao Console Version

Simple wrapper for Youdao online translate (Chinese <-> English) service [API](http://fanyi.youdao.com/openapi?path=data-mode), as an alternative to the StarDict Console Version(sdcv).


## Record
Each word you query will be logged under the `.ydcv_history` in your home directory, and records the number of times each word was queried in descending order.
For example:
```
hello : 5
你好 : 3
world : 2
...
```

## Environment:
 * Python ( >=2.7, 3.x )
