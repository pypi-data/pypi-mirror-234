# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-10-22 13:32:07
@LastEditTime: 2023-06-07 16:30:11
@LastEditors: HuangJianYi
@Description: 风险控制帮助类
"""
from seven_framework import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.enum import PlatType
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.models.app_base_model import AppBaseModel
from seven_cloudapp_frame.models.mp_base_model import MPBaseModel
import re

class RiskManageHelper:
    """
    :description:风险控制帮助类
    """

    #sql关键字
    _sql_pattern_key = r"\b(and|like|exec|execute|insert|create|select|drop|grant|alter|delete|update|asc|count|chr|mid|limit|union|substring|declare|master|truncate|char|delclare|or)\b|(\*|;)"
    #Url攻击正则
    _url_attack_key = r"\b(alert|xp_cmdshell|xp_|sp_|restore|backup|administrators|localgroup)\b"

    @classmethod
    def is_contain_sql(self, str):
        """
        :description: 是否包含sql关键字
        :param str:参数值
        :return:
        :last_editors: HuangJianYi
        """
        result = re.search(self._sql_pattern_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def is_attack(self, str):
        """
        :description: 是否攻击请求
        :param str:当前请求地址
        :return:True是 False否
        :last_editors: HuangJianYi
        """
        if ":" in str:
            return True
        result = re.search(self._url_attack_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def filter_routine_key(self, key):
        """
        :description: 过滤常规字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        routine_key_list = ["\u200b"]
        if not isinstance(key, str):
            return key
        for item in routine_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def filter_sql(self, key):
        """
        :description: 过滤sql关键字
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        result = re.findall(self._sql_pattern_key, key.lower())
        for item in result:
            key = key.replace(item[0], "")
            key = key.replace(item[0].upper(), "")
        return key

    @classmethod
    def filter_special_key(self, key):
        """
        :description: 过滤sql特殊字符
        :param key:参数值
        :return:
        :last_editors: HuangJianYi
        """
        if not isinstance(key, str):
            return key
        special_key_list = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@","!"]
        for item in special_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def check_attack_request(self, context):
        """
        :description: 校验是否攻击请求和是否包含非法参数值
        :param context:context
        :return:True满足条件直接拦截 False不拦截
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        safe_config = share_config.get_value("safe_config",{})
        if safe_config.get("is_check_referer", False) == True:
            if not context.request.headers or not context.request.headers.get("Referer", ""):
                invoke_result_data.success = False
                invoke_result_data.error_code = "referer_error"
                invoke_result_data.error_message = f"请求不合法"
                return invoke_result_data
            if share_config.get_value("plat_type", PlatType.tb.value) == PlatType.wx.value:
                result = re.search(r"https://servicewechat.com/(\w+)/\d+", context.request.headers.get("Referer", ""))
                check_app_id = result.group(1)
                if check_app_id != share_config.get_value("app_id"):
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "referer_error"
                    invoke_result_data.error_message = f"请求不合法"
                    return invoke_result_data

        is_filter_attack = safe_config.get("is_filter_attack", False)
        if is_filter_attack == True and context.request_params:
            for key in context.request_params.keys():
                if self.is_contain_sql(context.request_params[key]) or self.is_attack(context.request_params[key]):
                    invoke_result_data.success = False
                    invoke_result_data.error_code="attack_error"
                    invoke_result_data.error_message = f"参数{key}:值不合法"
                    break
        return invoke_result_data

    @classmethod
    def check_params(self, must_params):
        """
        :description: 校验必传参数
        :return:InvokeResultData
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        must_array = []
        if type(must_params) == str:
            must_array = must_params.split(",")
        if type(must_params) == list:
            must_array = must_params
        for must_param in must_array:
            if not must_param in self.request_params or self.request_params[must_param] == "":
                invoke_result_data.success = False
                invoke_result_data.error_code="param_error"
                invoke_result_data.error_message = f"参数错误,缺少必传参数{must_param}"
                break
        return invoke_result_data

    @classmethod
    def check_current_limit(self, app_id, current_limit_count, current_limit_minute=1):
        """
        :description: 流量限流校验
        :param app_id: 应用标识
        :param current_limit_count: 流量限制数
        :param current_limit_minute: 流量限制时间，默认1分钟
        :return: True代表满足限制条件进行拦截
        :last_editors: HuangJianYi
        """
        if current_limit_count == 0:
            return False
        redis_init = SevenHelper.redis_init()
        if current_limit_minute == 1:
            cache_key = f"request_user_list_{app_id}:{str(SevenHelper.get_now_int(fmt='%Y%m%d%H%M'))}"
        else:
            key_list = []
            for i in range(current_limit_minute):
                now_minute_int = int((datetime.datetime.now() + datetime.timedelta(minutes=-i)).strftime('%Y%m%d%H%M'))
                key = f"request_user_list_{app_id}:{str(now_minute_int)}"
                key_list.append(key)
            cache_key = f"request_user_list_{app_id}"
            redis_init.sinterstore(cache_key, key_list)
            redis_init.expire(cache_key, 3600)

        if int(redis_init.scard(cache_key)) >= current_limit_count:
            return True
        else:
            return False

    @classmethod
    def check_handler_power(self, request_params, uri, handler_name, request_prefix="server"):
        """
        :description: 校验是否有权限访问接口
        :param request_params: 请求参数
        :param uri: 请求uri
        :param handler_name: handler_name
        :param request_prefix: 请求前缀(server或client)
        :return:True有False没有
        :last_editors: HuangJianYi
        """
        result = True
        if request_params and request_params.get("app_id", "") and f"/{request_prefix}/" in uri:
            server_power_config = config.get_value(f"{request_prefix}_power_config", {})
            power_codes = server_power_config.get(handler_name, "")
            if power_codes:
                app_base_model = AppBaseModel(context=self.context)
                app_info_dict = app_base_model.get_app_info_dict(request_params.get("app_id", ""))
                if app_info_dict:
                    mp_base_model = MPBaseModel(context=self.context)
                    result = mp_base_model.check_high_power(store_user_nick=app_info_dict["store_user_nick"], project_code=app_info_dict["project_code"], key_names=power_codes)
        return result

    @classmethod
    def add_current_limit_count(self, app_id, object_id):
        """
        :description: 流量限流计数,用于登录接口限制登录
        :param app_id: 应用标识
        :param object_id: 用户唯一标识
        :return:
        :last_editors: HuangJianYi
        """
        redis_init = SevenHelper.redis_init()
        cache_key = f"request_user_list_{app_id}:{str(SevenHelper.get_now_int(fmt='%Y%m%d%H%M'))}"
        redis_init.sadd(cache_key, object_id)
        redis_init.expire(cache_key, 3600)

    @classmethod
    def desensitize_word(self, word):
        """
        :description: 脱敏文字,变成*号
        :param word 文字
        :return:
        :last_editors: HuangJianYi
        """
        if len(word) == 0:
            return ""
        elif len(word) == 1:
            return "*"
        elif len(word) == 2:
            return word[0:1] + "*"
        elif len(word) == 3:
            return word[0:1] + "*" + word[2:3]
        else:
            num = 3 if len(word) - 3 > 3 else len(word) - 3
            star = '*' * num
            return word[0:2] + star + word[len(word) - 1:len(word)]
