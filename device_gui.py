from datetime import datetime
import json
import logging
from time import sleep
import tkinter as tk
from tkinter import ttk
import sys
from tkinter import messagebox

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.redis_tool.redis_helper import RedisHelper
import base64
from google.protobuf.json_format import MessageToDict, MessageToJson

REFRESH_INTERVAL = 3000  # 毫秒，3 秒刷新一次
DEVICE_ID = "d-ec037f68-qnl1k6q2"  # 设备ID

sys.path.append("d:/PytestAutoApi/protobuf/protobuf_py")
from protobuf.protobuf_py import cmdPro_pb2, deviceProp_pb2


def get_device_params(device_id: str):
    redis_helper = RedisHelper(db=5)
    res = redis_helper.get_cached_messages(f"dev:op:shadowProp:{device_id}")
    msg = deviceProp_pb2.PropDataVo()

    device_params = {}
    for k, v in res.items():
        msg.ParseFromString(base64.b64decode(v))
        device_params[k] = MessageToDict(msg)
    return device_params


# 毫秒级时间戳转时间
def format_time(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp) / 1000).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]
    except:
        return str(timestamp)


# json参数值格式化
def parse_value(value, vtype=None):
    if vtype == "JSON":
        try:
            obj = json.loads(value)
            return json.dumps(obj, indent=2, ensure_ascii=False)
        except:
            return value
    else:
        return value


# 主应用类
class DeviceMonitorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("设备参数监控")
        self.master.geometry("800x600")
        self.redis_helper = RedisHelper(db=5)
        self.device_id = "d-8d8b4768-ns6aoiho"
        self.refresh_interval = 3000  # 毫秒
        self.old_params = {}
        self.battery_history = []

        self.create_widgets()

    def create_widgets(self):
        # Top Frame: 输入和按钮
        top_frame = ttk.Frame(self.master, padding=10)
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="设备ID:").pack(side=tk.LEFT)
        self.device_id_entry = ttk.Entry(top_frame, width=40)
        self.device_id_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.device_id_entry.insert(0, "d-8d8b4768-ns6aoiho")

        ttk.Button(top_frame, text="切换设备", command=self.switch_device).pack(
            side=tk.LEFT
        )
        ttk.Button(top_frame, text="电量图表", command=self.show_battery_chart).pack(
            side=tk.LEFT
        )

        # Treeview 表格区域
        self.tree = ttk.Treeview(
            self.master, columns=("para", "value", "type", "time"), show="headings"
        )

        self.tree.heading("para", text="参数")
        self.tree.heading("value", text="值")
        self.tree.heading("type", text="类型")
        self.tree.heading("time", text="时间")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 滚动条
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.show_detail_popup)
        self.start_refresh_loop()

    def switch_device(self):
        self.device_id = self.device_id_entry.get().strip()
        if not self.device_id:
            messagebox.showwarning("提示", "请输入设备ID")
            return
        self.old_params = {}
        self.update_params()

    def start_refresh_loop(self):
        self.update_params()
        print("开始更新数据")
        self.master.after(self.refresh_interval, self.start_refresh_loop)

    def update_params(self):
        if not self.device_id:
            return
        try:
            key = f"dev:op:shadowProp:{self.device_id}"
            res = self.redis_helper.get_cached_messages(key)
            msg = deviceProp_pb2.PropDataVo()

            new_params = {}
            for k, v in res.items():
                msg.ParseFromString(base64.b64decode(v))
                new_params[k] = MessageToDict(msg)
                if k.strip('"') == "battery_quantity":
                    try:
                        self.battery_history.append(int(new_params[k].get("value", 0)))
                    except ValueError:
                        pass
            self.refresh_ui(new_params)
        except Exception as e:
            logging.error(f"设备数据更新失败: {e}")

    def refresh_ui(self, new_params):
        self.tree.delete(*self.tree.get_children())

        for key, data in new_params.items():
            value = data.get("value", "")
            type_ = data.get("type", "DEFAULT")
            time_ = data.get("time", "")

            self.tree.insert("", tk.END, values=(key, value, type_, format_time(time_)))

            if key not in self.old_params or self.old_params[key] != data:
                logging.info(f"[{self.device_id}] 参数变化: {key} -> {data}")

        self.old_params = new_params.copy()

    def show_detail_popup(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item["values"]

            detail_window = tk.Toplevel(self.master)
            detail_window.title(f"参数详情: {values[0]}")
            detail_window.geometry("400x300")

            ttk.Label(
                detail_window, text=f"参数: {values[0]}", font=("Arial", 12)
            ).pack(pady=10)
            ttk.Label(detail_window, text=f"值: {values[1]}", font=("Arial", 12)).pack(
                pady=5
            )
            ttk.Label(
                detail_window, text=f"类型: {values[2]}", font=("Arial", 12)
            ).pack(pady=10)
            ttk.Label(
                detail_window, text=f"时间: {values[3]}", font=("Arial", 12)
            ).pack(pady=10)

    def show_battery_chart(self):
        if not self.battery_history:
            messagebox.showwarning("提示", "暂无电量数据")
            return

        chart_window = tk.Toplevel(self.master)
        chart_window.title(f"电量图表: {self.device_id}")
        chart_window.geometry("600x400")

        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.plot(self.battery_history, marker="o", linestyle="-", color="green")
        ax.set_title("电量历史数据")
        ax.set_xlabel("时间(刷新次数)")
        ax.set_ylabel("电量(%)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceMonitorApp(root)
    root.mainloop()
