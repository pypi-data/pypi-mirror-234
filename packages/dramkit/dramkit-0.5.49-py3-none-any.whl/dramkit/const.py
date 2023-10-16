# -*- coding: utf-8 -*-

import sys
import platform

#%%
SYSTEM = platform.system().lower()
WIN_SYS = 'windows' in SYSTEM
LINUX_SYS = 'linux' in SYSTEM

PY_VERSION = sys.version.split(' ')[0]
PY_VERSION2 = '.'.join([x.zfill(2) for x in sys.version.split(' ')[0].split('.')])

#%%
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}

#%%
