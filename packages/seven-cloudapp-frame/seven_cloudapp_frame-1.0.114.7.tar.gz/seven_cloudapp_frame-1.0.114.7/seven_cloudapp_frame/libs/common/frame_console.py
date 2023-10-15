# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2023-02-10 09:28:07
@LastEditTime: 2023-02-10 09:28:29
@LastEditors: HuangJianYi
@Description: console引用
"""
# 框架引用
from seven_framework.console.base_console import *
from seven_cloudapp_frame.libs.common import *

# 初始化配置,执行顺序需先于调用模块导入
share_config.init_config("share_config.json")  # 全局配置,只需要配置一次