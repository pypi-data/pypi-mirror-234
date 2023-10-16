# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_apexranklookup']

package_data = \
{'': ['*'],
 'nonebot_plugin_apexranklookup': ['data/*', 'data/font/*', 'data/image/*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'loguru>=0.6.0,<0.7.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'pydantic>=1.10.6,<2.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-apexranklookup',
    'version': '0.1.7',
    'description': '',
    'long_description': '## nonebot_plugin_apexranklookup\n\n一个基于nonebot的插件，用于查询Apex英雄的\n\n> 地图轮换\n> \n> 玩家信息\n> \n> 复制器\n> \n> 猎杀门槛\n\n## api key申请\n在https://apexlegendsapi.com/ 获取APIkey填入.env 或者config.py中\n`apex_api_token`\n\n## 使用\n#### .map/.地图\n查看当前大逃杀、竞技场模式轮换地图，以及地图剩余时间。\n![](./image/map.png)\n#### .stat/.查询 origin_id (平台)\n根据origin_id查询玩家信息（id、等级、段位、当前状态）\n\n可查询多平台(PC、PS4、X1)，不添加默认PC\n![](./image/stat.png)\n\n#### .crafting/.复制器\n查询当前复制器轮换物品。\n![](./image/crafting.png)\n\n#### .pd/.猎杀\n查询全平台大逃杀、竞技场猎杀最低分和大师段位以上的人数。\n![](./image/pd.png)\n\n#### .bind/.绑定\norigin id 与qq绑定，实现更方便的查询。\n![](./image/bind.png)\n\n#### .unbind/.解绑\n解除绑定\n\n### 图片自定义\n/data/image/base.png 为玩家信息的背景底色，可以660*750大小替换。\n\n/data/font/SourceHanSansCN-Normal.ttf 为默认字体，也可替换，之后去draw.py修改路径。\n\n更多样式修改详见draw.py\n\n## TODO\n> 中文文本翻译\n> \n> ~~输出美化~~\n> \n> ~~追踪器输出优化~~\n> \n> ~~添加绑定功能~~\n> \n> 添加订阅功能\n\n## 致谢\n\nhttps://apexlegendsapi.com/\n\nhttps://github.com/Shennoter/ApexRankLookUp\n',
    'author': 'Windylh',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
