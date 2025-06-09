import serial.tools.list_ports
import serial
import time
import threading
# 获取所有可用的串口
ports = serial.tools.list_ports.comports()

# 遍历并打印每个串口的信息
for port in ports:
    print(f"设备名称: {port.device}")
    print(f"描述信息: {port.description}")
    print(f"硬件ID: {port.hwid}")
    print(f"厂商ID: {port.vid}")
    print(f"产品ID: {port.pid}")
    print(f"序列号: {port.serial_number}")
    print(f"制造商: {port.manufacturer}")
    print(f"产品: {port.product}")
    print(f"接口: {port.interface}")
    print("-" * 40)


def read_from_serial(ser):
    """读取串口数据并打印"""
    while True:
        try:
            data = ser.readline()
            if data:
                print(f"[收到] {data.decode('utf-8', errors='replace')}")
        except Exception as e:
            print(f"[错误] 读取串口数据时发生异常: {e}")
            break


def write_to_serial(ser):
    """从用户输入读取数据并发送到串口"""
    while True:
        try:
            user_input = input("[发送] 输入内容: ")
            if user_input.lower() in ("exit", "quit"):
                print("[信息] 退出发送线程。")
                break
            ser.write((user_input + "\n").encode("utf-8"))
        except Exception as e:
            print(f"[错误] 发送数据时发生异常: {e}")
            break


def main():
    # 初始化串口连接
    try:
        ser = serial.Serial(port="COM8", baudrate=115200, timeout=1)  # 根据实际情况修改
    except serial.SerialException as e:
        print(f"[错误] 无法打开串口: {e}")
        return

    print(f"[信息] 已连接到串口 {ser.port}，波特率 {ser.baudrate}")

    # 创建并启动读取线程
    read_thread = threading.Thread(target=read_from_serial, args=(ser,), daemon=True)
    read_thread.start()

    # 创建并启动写入线程
    write_thread = threading.Thread(target=write_to_serial, args=(ser,), daemon=True)
    write_thread.start()

    # 等待写入线程结束
    write_thread.join()
    ser.close()
    print("[信息] 串口已关闭。")


if __name__ == "__main__":
    main()
