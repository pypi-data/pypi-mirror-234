'''
Copyright 2023 lcctoor.com

Author Information:
Author's Name: 许灿标
Author's Nickname: lcctoor.com
Author's Domain: lcctoor.com
Author's Email: lcctoor@outlook.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
For the detailed terms and conditions, refer to the Apache License, Version 2.0 at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import sys
from pathlib import Path

from ._envname import envname


def _parsecmd():
    kws = sys.argv[1:]
    if kws:
        kw = kws[0].lower()
        if kw == 'set' and len(kws) > 1:
            py = Path(__file__).parent / '_envname.py'
            py.write_text(f"envname = '{kws[1]}'", 'utf8')
            print('创建成功!')
        elif kw == 'read':
            print(envname)
    else:
        print('''指令集:
envname set <名称> | 创建环境名称
envname read       | 查看环境名称
''')