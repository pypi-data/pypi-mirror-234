# WaveletThings MQTT client Python SDK

WaveletThings is an open-source IoT platform for data collection, processing, visualization, and device management.

SDK supports:
* δ���ܺͼ��ܣ�TLS v1.2������
* QoS 0 �� 1
* �Զ�����
* �����豸��MQTT�ӿ�
* �������ص�MQTT�ӿ�

��ǰ��SDK����`paho-mqtt`��

## ��װ

ʹ��pip��װ��
```shell
pip3 install wt_mqtt
```

## ���ٿ�ʼ

��ʼ���ͻ��˲�����ң������
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

Ҫͨ��SSL�ϵ�MQTT���ӵ�WaveletThings�����ȣ���Ӧ������һ��֤�飬��ʹ�����´��룺

```python
from wt_mqtt.wt_device_mqtt import WTDeviceMqttClient

client = WTDeviceMqttClient(host="things.xiaobodata.com", port=1883)
client.connect(tls=True,
               ca_certs="mqttserver.pub.pem",
               cert_file="mqttclient.nopass.pem")
client.disconnect()

```

## ʹ���豸API

WTDeviceMQTClient�ṩ��Thingsƽ̨���豸MQTT API�ķ��ʡ�
��������ң������Ը��¡��������Ը��ġ����ͺͽ���RPC����ȡ�

### ���Ĺ������Ը���
�����Ҫ���չ������Ը��£�����ʹ�����´��룺
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

### ����ң������

Ϊ����Things�������ݣ�����ʹ�����´��룺

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

### ��������

Ϊ�˴�Things��������ֵ������ʹ������ʾ�������ʾ����ȡ��"configuration", "targetFirmwareVersion"��ֵ��
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

### ��Ӧ����˵�RPC�ص�
������뷢��ĳ��RPC�������Ӧ������ʹ����������е��߼���
�����ʾ�����ӵ�Things����ʵ�����ȴ�RPC����
�����յ�RPC����ʱ���ͻ�������Things������Ӧ�����а������Ծ��пͻ����Ļ��������ݡ�

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


## ʹ������API
WTGatewayMqttClient�̳���WTDeviceMqttClient����˿�����Ϊ�����豸����������API��
���⣬�����ܹ��������ӵ����Ķ���豸��

### ����ң�������

����ʹ�����´��룺
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

### ��server��ȡ��������
��ȡ`Test Device A1`�Ĺ������ԣ�����ʹ�����´��룺

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

### ��Ӧ����˵�RPC�ص�
����ʹ�����´��룺
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