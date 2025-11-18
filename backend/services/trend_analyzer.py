import json
from pathlib import Path


class TrendAnalyzer:
    def __init__(self):
        self.trend_file = Path("reports/trend_data.json")
        self.data = self._load_trend_data()

    def _load_trend_data(self):
        """加载趋势数据"""
        if self.trend_file.exists():
            try:
                data = json.loads(self.trend_file.read_text(encoding="utf-8"))
                # 保证始终是列表
                if isinstance(data, dict):
                    data = [data]
                return data
            except Exception as e:
                print(f"⚠️ 无法加载趋势数据: {e}")
                return []
        return []

    def add_new_record(self, record: dict):
        """添加一条新的测试记录"""
        self.data.append(record)
        # 限制最多保存最近100次记录
        self.data = self.data[-100:]
        self.trend_file.write_text(
            json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def get_chart_data(self):
        """提供给前端绘制趋势图的数据"""
        if not isinstance(self.data, list):
            print(f"⚠️ 数据类型错误: {type(self.data)}，自动重置为空列表")
            self.data = []
        # 最近20次趋势数据
        last_records = self.data[-20:] if len(self.data) > 0 else []
        x = [r.get("timestamp", "") for r in last_records]
        y_pass_rate = [r.get("pass_rate", 0) for r in last_records]
        y_failed = [r.get("failed", 0) for r in last_records]
        return {"x": x, "y_pass_rate": y_pass_rate, "y_failed": y_failed}
