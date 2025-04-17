import json
import allure
from utils.other_tools.models import AllureAttachmentType


# 使用allure库记录测试步骤
def allure_step(step: str, var: str) -> None:
    """
    记录测试步骤
    :param step: 步骤名称
    :param var: 步骤变量
    """
    with allure.step(step):
        # 将变量var转换为JSON格式并附加到测试步骤中
        allure.attach(
            json.dumps(str(var), ensure_ascii=False, indent=4),
            step,
            allure.attachment_type.JSON,
        )


# 使用allure库记录测试附件
def allure_attach(source: str, name: str, extension: str):
    """
    记录测试附件
    :param source: 附件路径
    :param name: 附件名称
    :param extension: 附件类型
    """
    _name = name.split(".")[-1].upper()
    _attachment_type = getattr(AllureAttachmentType, _name, None)
    allure.attach.file(
        source=source,
        name=name,
        attachment_type=(
            _attachment_type if _attachment_type is None else _attachment_type.value
        ),
        extension=extension,
    )


def allure_step_no(step: str):
    """
    无附件的操作步骤
    :param step: 步骤名称
    :return:
    """
    with allure.step(step):
        pass
