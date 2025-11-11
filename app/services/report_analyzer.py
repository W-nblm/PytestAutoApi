
import re
import json
import statistics
from datetime import datetime
from pathlib import Path
from utils.report_util import load_test_report
from services.failure_classifier import classify_failure
from google import genai


class ReportAnalyzer:
    """AI 驱动的测试报告分析器"""

    def __init__(self, report_path: str, api_key: str = None):
        self.report_path = report_path
        self.client = genai.Client(api_key=api_key) if api_key else None
        self.report = load_test_report(report_path)
        self.summary = {}
        self.failures = []

    def analyze(self):
        """核心分析流程"""
        total, passed, failed = 0, 0, 0
        durations = []

        for case in self.report.get("tests", []):
            total += 1
            durations.append(case.get("duration", 0))
            if case.get("status") == "passed":
                passed += 1
            elif case.get("status") == "failed":
                failed += 1
                failure = self._analyze_failure(case)
                self.failures.append(failure)

        self.summary = {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": round(passed / total * 100, 2) if total else 0,
            "avg_duration": round(statistics.mean(durations), 3) if durations else 0,
        }

        ai_summary = self._ai_summary()
        return {
            "summary": self.summary,
            "failures": self.failures,
            "ai_summary": ai_summary,
        }

    def _analyze_failure(self, case):
        """提取失败信息并分类"""
        message = case.get("message", "")
        err_type = classify_failure(message)
        suggestion = self._ai_fix_suggestion(case, message)
        return {
            "name": case.get("name"),
            "error_type": err_type,
            "message": message.strip(),
            "suggestion": suggestion,
        }

    def _ai_summary(self):
        """让 LLM 总结整体质量状况"""
        if not self.client:
            return "未启用 AI 总结"
        content = json.dumps(self.summary, ensure_ascii=False)
        resp = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"请根据以下测试统计数据，总结整体质量状况，并提出改进建议：{content}",
        )
        return resp.text.strip()

    def _ai_fix_suggestion(self, case, message):
        """AI 修复建议（对单个失败）"""
        if not self.client:
            return "（建议启用 AI 生成详细修复方案）"
        prompt = f"以下是接口测试失败信息，请分析原因并提出修复建议：\n{message}\n接口信息:{case.get('name')}"
        resp = self.client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
        return resp.text.strip()
