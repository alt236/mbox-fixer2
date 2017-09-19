### mbox_fixer

A python script that will attempt to repair a Thunderbird mbox file.
It does two things:
1. It looks for unescaped lines starting with "From " (this great and _completely_ unambiguous delimiter) and escapes them.
2. it will, optionally, try to fix encoding issues in the file.

The original file will be untouched, and a new one will be created in the same directory.

```
usage: mbox_fixer.py [-h] -i INPUT [-e]

Read an mbox file and try to escape runaway "From " lines. The original file
is NOT altered, but new file, suffixed with '_fixed', will be created in the
same directory. If the new file is the same as the old one, it will be
transparently deleted.


optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The mbox file to read
  -e, --encoding-fallback
                        If reading a line using utf-8 fails, try to recover
                        using windows-1252
```

#### License
    Copyright (C) 2016 Alexandros Schillings

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
