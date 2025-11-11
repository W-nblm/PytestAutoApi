import os
import subprocess
from datetime import datetime
from pathlib import Path


def run_tests():
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"report_{timestamp}.json"
    latest_path = report_dir / "latest_report.json"

    print("🚀 开始执行测试用例...")
    cmd = [
        "pytest",
        "tests",
        "--maxfail=3",
        "--disable-warnings",
        "-q",
        f"--json-report",
        f"--json-report-file={report_path}",
    ]
    subprocess.run(cmd, check=False)

    # 更新 latest_report.json
    if report_path.exists():
        latest_path.write_text(report_path.read_text(), encoding="utf-8")
        print(f"✅ 测试完成，报告已生成：{latest_path}")
    else:
        print("❌ 未生成报告，请检查 pytest-json-report 插件是否安装")


if __name__ == "__main__":
    run_tests()
