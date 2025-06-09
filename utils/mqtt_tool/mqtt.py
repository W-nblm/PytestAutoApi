import time
import paho.mqtt.client as mqtt
from utils.logging_tool.log_control import INFO, ERROR, WARNING


class Mqtt:
    last_msg = None
    msgs = []
    send_status = []  # 消息发布状态
    callbacks = None
    last_send_status = None

    def __init__(
        self,
        username="iot",
        password="Lzy#iot",
        host="47.107.113.31",
        port=16883,
        keep_live=600,
        device_id="wyl123111",
        home_id="wykhome",
    ) -> None:
        # 创建 MQTT 客户端实例
        self.client = mqtt.Client()
        # 初始化 MQTT 连接
        self.client_connect(
            username=username,
            password=password,
            host=host,
            port=port,
            keep_live=keep_live,
        )
        self.device_id = device_id
        self.home_id = home_id
        # [05-20 15:44:49:409][INFO][ipc_mqtt.c:2219]subscribe plat/general_plat_to_dev/devices/d-f5701968-jmgm9cqp/send/+
        # [05-20 15:44:49:409][INFO][ipc_mqtt.c:2219]subscribe device/general_dev_to_plat/devices/d-f5701968-jmgm9cqp/response/+
        # [05-20 15:44:49:409][INFO][ipc_mqtt.c:2219]subscribe device/network/devices/d-f5701968-jmgm9cqp/response/+
        # [05-20 15:44:49:409][INFO][ipc_mqtt.c:2219]subscribe device/ntp/devices/d-f5701968-jmgm9cqp/response/+
        # [05-20 15:44:49:409][INFO][ipc_mqtt.c:2219]subscribe plat/commands/home/+/devices/d-f5701968-jmgm9cqp/send/+
        # [05-20 15:44:49:409][INFO][ipc_mqtt.c:2219]subscribe plat/properties_get/home/+/devices/d-f5701968-jmgm9cqp/send/+
        # 默认订阅主题
        # plant to device
        self.plant_to_device_topic = (
            f"plat/general_plat_to_dev/devices/{self.device_id}/send/+"
        )
        # device to plant
        self.device_to_plant_topic = (
            f"device/general_dev_to_plat/devices/{self.device_id}/response/+"
        )
        # device to network
        self.device_to_network_topic = (
            f"device/network/devices/{self.device_id}/response/+"
        )
        # device to ntp
        self.device_to_ntp_topic = f"device/ntp/devices/{self.device_id}/response/+"
        # plant to commands
        self.plant_to_commands_topic = (
            f"plat/commands/home/+/devices/{self.device_id}/send/+"
        )
        # plant to properties_get
        self.plant_to_properties_get_topic = (
            f"plat/properties_get/home/+/devices/{self.device_id}/send/+"
        )

        # self.client.loop_start()
        # 初始化订阅主题
        self._init_subscribe_topics()

    # 初始化订阅主题
    def _init_subscribe_topics(self):
        # 订阅平台到设备主题
        self.client_subcribe(self.plant_to_device_topic)
        # 添加设备到平台的消息回调函数
        # self.add_topic_callback(
        #     self.device_to_plant_topic, self.device_attribute_message
        # )
        # 订阅设备到网络主题
        self.client_subcribe(self.device_to_network_topic)
        # 添加设备到网络的消息回调函数
        self.add_topic_callback(self.device_to_network_topic, self.keeplive_message)
        # 订阅设备到ntp主题
        self.client_subcribe(self.device_to_ntp_topic)
        # 添加设备到ntp的消息回调函数
        self.add_topic_callback(self.device_to_ntp_topic, self.ntp_message)
        # 订阅平台到命令主题
        self.client_subcribe(self.plant_to_commands_topic)
        # 添加平台到命令的消息回调函数
        # self.add_topic_callback(self.plant_to_commands_topic, self.device_attribute_message)
        # 订阅平台到属性获取主题
        self.client_subcribe(self.plant_to_properties_get_topic)
        # 添加平台到属性获取的消息回调函数
        # self.add_topic_callback(
        #     # self.plant_to_properties_get_topic, self.device_attribute_message
        # )

    # 连接回调
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            INFO.logger.info(f"Connected Success")
        else:
            INFO.logger.info(f"Connected Fail,code:{rc}")

    # 消息回调
    def on_message(self, client, userdata, msg):
        self.last_msg = msg.payload
        self.msgs.append(msg.payload)
        INFO.logger.info(f"Received message: {msg.payload} on topic {msg.topic}")

    def ntp_message(self, client, userdata, msg):
        # topic_sub = f"device/ntp/devices/d-c5cbdd64-lyje5a62/response/+"
        # device_ntp_proto = ntpTime_pb2.NtpRequest()
        # 导入绑定设备数据结构的protobuf py模块和创建proto对象
        INFO.logger.info(
            f"接受设备ntp上报的消息: '{msg.payload}' from topic: {msg.topic}"
        )
        import time

        deviceRecvTime = int(time.time() * 1000)
        from protobuf.protobuf_py import ntpTime_pb2

        # 等待接收绑定设备的推送消息、反序列化收到推送消息
        ntpResponse = ntpTime_pb2.NtpRespose()
        ntpResponse.ParseFromString(msg.payload)
        response = {
            "deviceSendTime": ntpResponse.deviceSendTime,
            "serverRecvTime": ntpResponse.serverRecvTime,
            "serverSendTime": ntpResponse.serverSendTime,
        }
        devtime = (
            response["serverRecvTime"]
            + response["serverSendTime"]
            + deviceRecvTime
            - response["deviceSendTime"]
        ) / 2
        INFO.logger.info(f"服务器响ntp反序列化后数据:{response}")
        INFO.logger.info(f"服务端unix时间: {devtime}")

    def keeplive_message(self, client, userdata, msg):

        INFO.logger.info(
            f" 接收到设备心跳上报消息： `{msg.payload}` from主题 {msg.topic} "
        )
        from protobuf.protobuf_py import keeplive_pb2

        # 等待接收绑定设备的推送消息、反序列化收到推送消息
        response = keeplive_pb2.keeplive()
        response.ParseFromString(msg.payload)
        INFO.logger.info(f"设备的心跳：{response}")

    def device_attribute_message(self, client, userdata, msg):
        INFO.logger.info(
            f"接受设备属性上报的消息: '{msg.payload}' from topic: {msg.topic}"
        )
        from protobuf.protobuf_py import cmdPro_pb2

        response = cmdPro_pb2.CmdProResponse()
        response.ParseFromString(msg.payload)
        INFO.logger.info(f"{msg.topic}:{response}")

    # 连接到 MQTT 服务器
    def client_connect(self, username, password, host, port, keep_live):
        # 设置连接和消息回调函数
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, password)
        self.client.connect(host=host, port=port, keepalive=keep_live)

    # 订阅主题
    def client_subcribe(self, topic):
        self.client.subscribe(topic=topic)
        INFO.logger.info(f"当前subscribe主题:{topic}")

    def add_topic_callback(self, topic, callback):
        INFO.logger.info(f"add topic: {topic}")
        self.client.message_callback_add(topic, callback)

    # 发布消息
    def client_publish(self, topic, payload):
        send_result = self.client.publish(
            topic=topic, payload=payload, qos=0, retain=False, properties=None
        )
        if send_result[0] == 0:  # 值等于0表示发送成功
            result = dict()
            result[topic] = send_result[0]
            self.last_send_status = send_result[0]
            self.send_status.append(result)
            INFO.logger.info(f"Send `{payload}` to topic `{topic}`")
        else:
            INFO.logger.error(f"Failed to send message to topic {topic}")

    def client_loop_forever(self):
        # 启动 MQTT 客户端循环
        self.client.loop_forever()

    def client_disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    client = Mqtt(device_id="d-f5701968-jmgm9cqp")
    client.client_connect

    # client.client_loop_forever()
    client.client_disconnect()
