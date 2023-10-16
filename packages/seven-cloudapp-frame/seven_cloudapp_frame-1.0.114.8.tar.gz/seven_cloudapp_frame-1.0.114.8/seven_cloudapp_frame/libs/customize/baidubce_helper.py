# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2022-11-17 18:51:25
@LastEditTime: 2023-08-10 09:34:22
@LastEditors: HuangJianYi
@Description: 
"""
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *
from seven_cloudapp_frame.models.seven_model import InvokeResultData


class BaidubceHelper:
    """
    :description: 百度云帮助类
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_access_token(self):
        """
        :description:动态获取access_token
        :return: 
        :last_editors: HuangJianYi
        """
        api_key = share_config.get_value("baidubce_config", {}).get("text_censor", {}).get("api_key", "")
        secret_key = share_config.get_value("baidubce_config", {}).get("text_censor", {}).get("secret_key", "")
        request_url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'
        response = requests.get(request_url)
        if response:
            if "error" not in json.loads(response.text).keys():
                access_token = json.loads(response.text)["access_token"]
                redis_init = SevenHelper.redis_init(config_dict=config.get_value("platform_redis"))
                redis_init.set("baidu_access_token", access_token, ex=2591000)
                return access_token
            else:
                self.logger_error("【获取百度云access_token失败】" + response.text)
        return ""

    @classmethod
    def text_censor(self, text, conclusion_types = [1]):
        """
        :description: 百度云文本审核
        :param text：内容
        :param conclusion_types：允许审核通过的结果类型（1.合规，2.不合规，3.疑似，4.审核失败）
        :last_editors: HuangJianYi
        """
        invoke_result_data = InvokeResultData()
        redis_init = SevenHelper.redis_init(config_dict=config.get_value("platform_redis"))
        access_token = redis_init.get("baidu_access_token")
        if not access_token:
            access_token = self.get_access_token()
        if not access_token:
            invoke_result_data.success = False
            invoke_result_data.error_code = "fail_access_token"
            invoke_result_data.error_message = "无法进行文本审核"
            return invoke_result_data
        params = {"text": text}
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            if "error_code" not in json.loads(response.text).keys():
                conclusion_type = response.json()["conclusionType"]
                if conclusion_type not in  conclusion_types:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "fail"
                    invoke_result_data.error_message = "存在敏感词"
                    return invoke_result_data
                invoke_result_data.data = conclusion_type
                return invoke_result_data
            else:
                self.logger_error("【百度云文本审核失败】" + response.text)
        invoke_result_data.success = False
        invoke_result_data.error_code = "fail"
        invoke_result_data.error_message = "无法进行文本审核"
        return invoke_result_data
