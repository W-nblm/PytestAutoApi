import re
import datetime
import random
from datetime import date, timedelta, datetime
from jsonpath import jsonpath
from faker import Faker
from utils.logging_tool.log_control import ERROR, INFO
from utils.captcha.vcode import fix_img, cut_img, train_model, rek_img
from common.setting import ensure_path_sep
from io import BytesIO
from PIL import Image
import base64


class Context:
    def __init__(self):
        self.faker = Faker(locale="zh_CN")

    @classmethod
    def random_int(cls):
        """
        随机整数
        :return:
        """
        return random.randint(0, 10000)

    def random_phone(self):
        """
        随机手机号
        :return:
        """
        return self.faker.phone_number()

    def random_email(self):
        """
        随机邮箱
        :return:
        """
        return self.faker.email()

    def random_male_name(self):
        """
        随机男性姓名
        :return:
        """
        return self.faker.name_male()

    def random_female_name(self):
        """
        随机女性姓名
        :return:
        """
        return self.faker.name_female()

    def random_female_name(self):
        """
        随机地址
        :return:
        """
        return self.faker.address()

    @classmethod
    def now_time(cls):
        """
        当前时间
        :return:
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def today_zero_time(cls):
        """
        当天零点时间
        :return:
        """
        return (
            datetime.now()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .strftime("%Y-%m-%d %H:%M:%S")
        )

    @classmethod
    def before_week_time(cls):
        """
        一周后的0点时间
        :param days:
        :return:
        """
        return (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d 00:00:00")

    @classmethod
    def host(cls) -> str:
        """获取接口域名
        :return:
        """
        from utils import config

        return config.host

    @classmethod
    def app_host(cls) -> str:
        """获取app host
        :return:
        """
        from utils import config

        return config.app_host

    def generate_vcode(self, img: str):
        try:
            INFO.logger.info({"img": img})
            image_data = base64.b64decode(img)
            image_file = BytesIO(image_data)
            image = Image.open(image_file)
            image.save(ensure_path_sep(rf"\utils\captcha\vcode\test\code.png"))
            model_dict = train_model(
                ensure_path_sep(r"\utils\captcha\vcode\cut_dir"), ["png"]
            )
            code = rek_img(
                model_dict, ensure_path_sep(r"\utils\captcha\vcode\test"), ["png"]
            )

            if len(code) != 3:
                raise ValueError(
                    f"验证码识别失败, 请检查验证码图片是否正确,code:{code}"
                )
            first_name, operator, second_name = code[0], code[1], code[2]
            if not (first_name.isdigit() and second_name.isdigit()):
                raise ValueError(
                    f"验证码识别失败, 请检查验证码图片是否正确,code:{code}"
                )

            # 如果x在列表中则为乘法,单独计算
            if operator == "x":
                return int(first_name) * int(second_name)
            else:
                return eval(f"{first_name}{operator}{second_name}")
        except Exception as e:
            ERROR.logger.error(f"验证码识别失败, {e}")
            raise


def extract_json_data(js_path, res):
    """
    提取sql中的json数据
    :param js_path:
    :param res:
    :return:
    """
    _json_data = jsonpath(res, js_path)[0]
    if _json_data is False:
        raise ValueError(f"sql中的jsonpath获取失败{res}, {js_path}")
    return jsonpath(res, js_path)[0]


# 处理sql中的依赖数据，通过获取接口响应的jsonpath的值进行替换
def sql_regular(value, res=None):
    """
    处理sql中的依赖数据,通过获取接口响应的jsonpath的值进行替换
    :param value:
    :param res:
    :return:
    """
    sql_json_list = re.findall(r"\$json\((.*?)\)\$", value)
    for i in sql_json_list:
        pattern = re.compile(
            r"\$json\(" + i.replace("$", "\$").replace("[", "\[") + r"\)\$"
        )
        key = str(extract_json_data(i, res))
        value = re.sub(pattern, key, value, count=1)
    return value


# 通过正则表达式获取缓存中的内容
def cache_regular(value):
    """
    通过正则表达式获取缓存中的内容
    列:$cache{login_token}
    :param value:
    :return:
    """
    from utils.cache_process.cache_control import CacheHandler

    # 获取$cache{login_token}中的login_token
    regular_data = re.findall(r"\$cache\{(.*?)\}", value)
    for data in regular_data:
        value_types = ["int:", "bool:", "list:", "dict:", "tuple:", "float:"]
        if any(i in data for i in value_types) is True:
            # 处理缓存中存储的类型
            value_types = data.split(":")[0]
            data = data.split(":")[1]

            pattern = re.compile(
                r"\'\$cache\{" + value_types.split(":")[0] + ":" + data + r"\}\'"
            )
        else:
            pattern = re.compile(
                r"\$cache\{" + data.replace("$", "\$").replace("[", "\[") + r"\}"
            )
        try:
            cache_value = CacheHandler.get_cache(data)
            value = re.sub(pattern, str(cache_value), value)
        except Exception as e:
            ERROR.logger.error(f"缓存中没有{data}的值, 请检查缓存是否存在, {e}")
            pass
    return value


def regular(target: str):
    """
    新版本
    使用正则替换请求数据
    :return:
    """
    try:
        regular_pattern = r"\${{(.*?)}}"
        while re.findall(regular_pattern, target):
            key = re.search(regular_pattern, target).group(1)
            value_types = ["int:", "bool:", "list:", "dict:", "tuple:", "float:"]
            if any(i in key for i in value_types) is True:
                func_name = key.split(":")[1].split("(")[0]
                value_name = key.split(":")[1].split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                regular_int_pattern = r"\'\${{(.*?)}}\'"
                target = re.sub(regular_int_pattern, str(value_data), target, 1)
            else:
                func_name = key.split("(")[0]
                value_name = key.split("(")[1][:-1]
                if value_name == "":
                    value_data = getattr(Context(), func_name)()
                else:
                    value_data = getattr(Context(), func_name)(*value_name.split(","))
                target = re.sub(regular_pattern, str(value_data), target, 1)
        return target

    except AttributeError:
        ERROR.logger.error("未找到对应的替换的数据, 请检查数据是否正确 %s", target)
        raise


if __name__ == "__main__":
    a = "${{generate_vcode($img)}} aaa"
    b = regular(a)
