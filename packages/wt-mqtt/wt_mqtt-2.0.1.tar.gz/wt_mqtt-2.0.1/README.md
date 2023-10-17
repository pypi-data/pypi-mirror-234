# WaveletThings MQTT client Python SDK

WaveletThings is an open-source IoT platform for data collection, processing, visualization, and device management.

SDK supports:
* 未加密和加密（TLS v1.2）连接
* QoS 0 和 1
* 自动重连
* 所有设备的MQTT接口
* 所有网关的MQTT接口

当前的SDK基于`paho-mqtt`库

## 安装

使用pip安装：
```shell
pip3 install wt_mqtt
```

## 快速开始

初始化客户端并发布遥测数据
```python
from wt_mqtt.wt_device_mqtt import WTDeviceMqttClient, WTPublishInfo

telemetry = {"temperature": 41.9, "enabled": False, "currentFirmwareVersion": "v1.2.2"}
client = WTDeviceMqttClient(host="things.xiaobodata.com", port=1883, token="A1_TEST_TOKEN")
# Connect to WaveletThings
client.connect()
# Sending telemetry without checking the delivery status
client.send_telemetry(telemetry)
# Sending telemetry and checking the delivery status (QoS = 1 by default)
result = client.send_telemetry(telemetry)
# get is a blocking call that awaits delivery status
success = result.get() == WTPublishInfo.WT_ERR_SUCCESS
# Disconnect from WaveletThings
client.disconnect()
```

### Connection using TLS

要通过SSL上的MQTT连接到WaveletThings，首先，您应该生成一个证书，并使用如下代码：

```python
from wt_mqtt.wt_device_mqtt import WTDeviceMqttClient

client = WTDeviceMqttClient(host="things.xiaobodata.com", port=1883)
client.connect(tls=True,
               ca_certs="mqttserver.pub.pem",
               cert_file="mqttclient.nopass.pem")
client.disconnect()

```

## 使用设备API

WTDeviceMQTClient提供对Things平台的设备MQTT API的访问。
它允许发布遥测和属性更新、订阅属性更改、发送和接收RPC命令等。

### 订阅共享属性更新
如果需要接收共享属性更新，可以使用以下代码：
```python
from time import sleep
from wt_mqtt.wt_device_mqtt import WTDeviceMqttClient


def callback(client, content, *args):
    print(content)


client = WTDeviceMqttClient("things.xiaobodata.com", "A1_TEST_TOKEN")
client.connect()
client.subscribe_to_attribute("uploadFrequency", callback)
client.subscribe_to_all_attributes(callback)
while True:
    sleep(1)
```

### 发布遥测数据

为了向Things发送数据，可以使用如下代码：

```python
from time import time
from wt_mqtt.wt_device_mqtt import WTDeviceMqttClient, WTPublishInfo

telemetry_with_ts = {"ts": int(round(time() * 1000)), "values": {"temperature": 42.1, "humidity": 70}}
client = WTDeviceMqttClient("things.xiaobodata.com", "A1_TEST_TOKEN")
# we set maximum amount of messages sent to send them at the same time. it may stress memory but increases performance
client.max_inflight_messages_set(100)
client.connect()
results = []
result = True
for i in range(0, 100):
    results.append(client.send_telemetry(telemetry_with_ts))
for tmp_result in results:
    result &= tmp_result.get() == WTPublishInfo.WT_ERR_SUCCESS
print("Result", str(result))
client.disconnect()
```

### 请求属性

为了从Things请求属性值，可以使用以下示例，这个示例获取了"configuration", "targetFirmwareVersion"的值：
```python
from time import sleep
from wt_mqtt.wt_device_mqtt import WTDeviceMqttClient


def on_attributes_change(client, result, *args):
    print(result)


client = WTDeviceMqttClient("things.xiaobodata.com", "A1_TEST_TOKEN")
client.connect()
client.request_attributes(["configuration", "targetFirmwareVersion"], callback=on_attributes_change)

while True:
    sleep(1)
```

### 响应服务端的RPC回调
如果您想发送某个RPC请求的响应，可以使用下面代码中的逻辑。
下面的示例连接到Things本地实例并等待RPC请求。
当接收到RPC请求时，客户机将向Things发送响应，其中包含来自具有客户机的机器的数据。

```python
import json
from time import sleep

from psutil import cpu_percent, virtual_memory
from wt_mqtt.wt_device_mqtt import WTDeviceMqttClient


# dependently of request method we send different data back
def on_server_side_rpc_request(client, request_id, request_body):
    print(request_id, request_body)
    if request_body["method"] == "getCPULoad":
        client.send_rpc_reply(request_id, json.dumps({"CPU percent": cpu_percent()}))
    elif request_body["method"] == "getMemoryUsage":
        client.send_rpc_reply(request_id, json.dumps({"Memory": virtual_memory().percent}))


client = WTDeviceMqttClient("things.xiaobodata.com", "A1_TEST_TOKEN")
client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
client.connect()

while True:
    sleep(1)
```


## 使用网关API
WTGatewayMqttClient继承了WTDeviceMqttClient，因此可以作为常规设备访问其所有API。
此外，网关能够代表连接到它的多个设备。

### 发送遥测和属性

可以使用如下代码：
```python
from time import time
from wt_mqtt.wt_gateway_mqtt import WTGatewayMqttClient

gateway = WTGatewayMqttClient("things.xiaobodata.com", "GATEWAY_TEST_TOKEN")
gateway.connect()
gateway.gw_connect_device("Test Device A1")

gateway.gw_send_telemetry("Test Device A1", {"ts": int(round(time() * 1000)), "values": {"temperature": 42.2}})
gateway.gw_send_attributes("Test Device A1", {"firmwareVersion": "2.3.1"})

gateway.gw_disconnect_device("Test Device A1")
gateway.disconnect()
```

### 从server获取共享属性
获取`Test Device A1`的共享属性，可以使用如下代码：

```python
from time import sleep
from wt_mqtt.wt_gateway_mqtt import WTGatewayMqttClient


def callback(client, result, *args):
    print(result)


gateway = WTGatewayMqttClient("things.xiaobodata.com", "GATEWAY_TEST_TOKEN")
gateway.connect()
gateway.gw_request_shared_attributes("Test Device A1", ["temperature"], callback)

while True:
    sleep(1)

```

### 响应服务端的RPC回调
可以使用如下代码：
```python
import json
from time import sleep

from psutil import cpu_percent, virtual_memory
from wt_mqtt.wt_gateway_mqtt import WTGatewayMqttClient


def rpc_request_response(client, request_id, request_body):
    # request body contains id, method and other parameters
    print(request_body)
    method = request_body["data"]["method"]
    device = request_body["device"]
    req_id = request_body["data"]["id"]
    # dependently of request method we send different data back
    if method == 'getCPULoad':
        client.send_rpc_reply(request_id, json.dumps({"CPU percent": cpu_percent()}))
    elif method == 'getMemoryLoad':
        client.send_rpc_reply(request_id, json.dumps({"Memory": virtual_memory().percent}))
    else:
        print('Unknown method: ' + method)


gateway = WTGatewayMqttClient("things.xiaobodata.com", "GATEWAY_TEST_TOKEN")
gateway.connect()
# now rpc_request_response will process rpc requests from servers
gateway.gw_set_server_side_rpc_request_handler(rpc_request_response)
# without device connection it is impossible to get any messages
gateway.gw_connect_device("Test Device A1")

while True:
    sleep(1)

```