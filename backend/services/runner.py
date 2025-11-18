import yaml
import requests
from pathlib import Path
import pytest
def run_yaml_cases(file_path: str):
    """通过pytest执行yaml测试用例文件"""
    
    pytest_args = [
        file_path,
        "--alluredir=reports/allure_reports",
        "--clean-alluredir",
    ]
    return_code = pytest.main(pytest_args)
    report_path = "reports/allure_reports"
    return report_path