import wx
import requests
import time
import paho.mqtt.client as mqtt
import event_pb2

class PerformanceTester(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Performance Tester", size=(600, 700))

        self.panel = wx.Panel(self)
        self.notebook = wx.Notebook(self.panel)
        self.create_https_page()
        self.create_mqtt_page()
        self.create_protobuf_page()
        self.notebook.AddPage(self.https_panel, "HTTPS")
        self.notebook.AddPage(self.mqtt_panel, "MQTT")
        self.notebook.AddPage(self.protobuf_panel, "Protobuf")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(sizer)

    def clear_console(self, event):
        self.console.Clear()

    def clear_console_mqtt(self, event):
        self.mqtt_console.Clear()

    def create_https_page(self):
        self.https_panel = wx.Panel(self.notebook)
        self.url_label = wx.StaticText(self.https_panel, label="URL:")
        self.url_text = wx.TextCtrl(self.https_panel)
        self.headers_label = wx.StaticText(self.https_panel, label="Headers (key:value format separated by commas):")
        self.headers_text = wx.TextCtrl(self.https_panel)
        self.params_label = wx.StaticText(self.https_panel, label="Params (key:value format separated by commas):")
        self.params_text = wx.TextCtrl(self.https_panel)
        self.body_label = wx.StaticText(self.https_panel, label="Body (JSON format):")
        self.body_text = wx.TextCtrl(self.https_panel, style=wx.TE_MULTILINE)
        self.loop_count_label = wx.StaticText(self.https_panel, label="Loop Count:")
        self.loop_count_text = wx.TextCtrl(self.https_panel, value="10")
        self.test_button = wx.Button(self.https_panel, label="Test HTTPS")
        self.test_button.Bind(wx.EVT_BUTTON, self.test_https_performance)
        self.console = wx.TextCtrl(self.https_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.clear_console_button_https = wx.Button(self.https_panel, label="Clear Console")
        self.clear_console_button_https.Bind(wx.EVT_BUTTON, self.clear_console)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.url_label, 0, wx.ALL, 5)
        sizer.Add(self.url_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.headers_label, 0, wx.ALL, 5)
        sizer.Add(self.headers_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.params_label, 0, wx.ALL, 5)
        sizer.Add(self.params_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.body_label, 0, wx.ALL, 5)
        sizer.Add(self.body_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.loop_count_label, 0, wx.ALL, 5)
        sizer.Add(self.loop_count_text, 0, wx.ALL | wx.EXPAND, 5)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.test_button, 0, wx.ALL, 5)
        btn_sizer.Add(self.clear_console_button_https, 0, wx.ALL, 5)
        sizer.Add(btn_sizer)

        sizer.Add(self.console, 1, wx.ALL | wx.EXPAND, 5)

        self.https_panel.SetSizer(sizer)

    def create_mqtt_page(self):
        self.mqtt_panel = wx.Panel(self.notebook)
        self.broker_label = wx.StaticText(self.mqtt_panel, label="MQTT Broker URL:")
        self.broker_text = wx.TextCtrl(self.mqtt_panel)
        self.port_label = wx.StaticText(self.mqtt_panel, label="Port:")
        self.port_text = wx.TextCtrl(self.mqtt_panel, value="1883")
        self.topic_label = wx.StaticText(self.mqtt_panel, label="Topic:")
        self.topic_text = wx.TextCtrl(self.mqtt_panel)
        self.test_mqtt_button = wx.Button(self.mqtt_panel, label="Test MQTT")
        self.test_mqtt_button.Bind(wx.EVT_BUTTON, self.test_mqtt_performance)
        self.mqtt_console = wx.TextCtrl(self.mqtt_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        self.clear_console_button_mqtt = wx.Button(self.mqtt_panel, label="Clear Console")
        self.clear_console_button_mqtt.Bind(wx.EVT_BUTTON, self.clear_console_mqtt)
        self.mqtt_loop_count_label = wx.StaticText(self.mqtt_panel, label="Loop Count:")
        self.mqtt_loop_count_text = wx.TextCtrl(self.mqtt_panel, value="10")
        self.payload_label = wx.StaticText(self.mqtt_panel, label="Payload:")
        self.payload_text = wx.TextCtrl(self.mqtt_panel, style=wx.TE_MULTILINE)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.broker_label, 0, wx.ALL, 5)
        sizer.Add(self.broker_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.port_label, 0, wx.ALL, 5)
        sizer.Add(self.port_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.topic_label, 0, wx.ALL, 5)
        sizer.Add(self.topic_text, 0, wx.ALL | wx.EXPAND, 5) 
        sizer.Add(self.payload_label, 0, wx.ALL, 5)  
        sizer.Add(self.payload_text, 0, wx.ALL | wx.EXPAND, 5)

        sizer.Add(self.mqtt_loop_count_label, 0, wx.ALL, 5)
        sizer.Add(self.mqtt_loop_count_text, 0, wx.ALL | wx.EXPAND, 5)     

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(self.test_mqtt_button, 0, wx.ALL, 5)
        btn_sizer.Add(self.clear_console_button_mqtt, 0, wx.ALL, 5)
        sizer.Add(btn_sizer)

        sizer.Add(self.mqtt_console, 1, wx.ALL | wx.EXPAND, 5)

        self.mqtt_panel.SetSizer(sizer)

    def create_protobuf_page(self):
        self.protobuf_panel = wx.Panel(self.notebook)

        self.json_input_label = wx.StaticText(self.protobuf_panel, label="Input JSON:")
        self.json_input_text = wx.TextCtrl(self.protobuf_panel, style=wx.TE_MULTILINE | wx.HSCROLL, size=(300, 200))

        self.convert_button = wx.Button(self.protobuf_panel, label="Convert to Protobuf")
        self.convert_button.Bind(wx.EVT_BUTTON, self.convert_json_to_protobuf)

        self.protobuf_output_label = wx.StaticText(self.protobuf_panel, label="Compressed Protobuf:")
        self.protobuf_output_text = wx.TextCtrl(self.protobuf_panel, style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY, size=(300, 200))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.json_input_label, 0, wx.ALL, 5)
        sizer.Add(self.json_input_text, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.convert_button, 0, wx.ALL, 5)
        sizer.Add(self.protobuf_output_label, 0, wx.ALL, 5)
        sizer.Add(self.protobuf_output_text, 0, wx.ALL | wx.EXPAND, 5)

        self.protobuf_panel.SetSizer(sizer)

    def convert_json_to_protobuf(self, event):
        import json

        raw_data = self.json_input_text.GetValue()

        try:
            # Parse the JSON input
            event_data = json.loads(raw_data)

            event = event_pb2.Event()

            # Populate header
            event.header.event_type = event_data["header"]["event_type"]
            event.header.pub_id = event_data["header"]["pub_id"]
            event.header.token = event_data["header"]["token"]
            event.header.pub_time = event_data["header"]["pub_time"]
            event.header.event_id = event_data["header"]["event_id"]

            # Set payload
            payload = event_data["payload"]

            event.payload = json.dumps(payload, ensure_ascii=False).encode('utf-8')

            # Serialize to bytes 
            data = event.SerializeToString()
            # print(data)

            # Convert to hex string
            hex_output = data.hex()

            # convert hex_output back to bytes
            # bytes_output = bytes.fromhex(hex_output)

            self.protobuf_output_text.SetValue(hex_output)
        except Exception as e:
            # Handle any errors in conversion and show a simple error message
            self.protobuf_output_text.SetValue(f"Error: {str(e)}")


    def test_https_performance(self, event):
        try:
            url = self.url_text.GetValue()
            headers_input = self.headers_text.GetValue()
            headers = {item.split(":")[0].strip(): item.split(":")[1].strip() for item in headers_input.split(",")} if headers_input else {}
            params_input = self.params_text.GetValue()
            params = {item.split(":")[0].strip(): item.split(":")[1].strip() for item in params_input.split(",")} if params_input else {}
            body = self.body_text.GetValue()

            try:
                loop_count = int(self.loop_count_text.GetValue())
            except ValueError:
                self.console.AppendText("Invalid loop count value. Please enter a valid integer.")
                return

            total_time = 0
            for _ in range(loop_count):
                start_time = time.time()
                response = requests.post(url, headers=headers, params=params, data=body)
                end_time = time.time()
                total_time += (end_time - start_time)

                self.console.AppendText(f"Request to {url} took {end_time - start_time:.4f} seconds\n")

                if response.status_code != 200 and response.status_code != 201:
                    self.console.AppendText(f"Request failed with status code: {response.status_code}\n")
                    return
                else:
                    self.console.AppendText(f"Response: {response.text}\n")

            average_time = total_time / loop_count
            self.console.AppendText(f"Average time taken for {loop_count} requests: {average_time:.4f} seconds\n")
        except Exception as e:
            self.console.AppendText(f"Error: {str(e)}\n")

    def test_mqtt_performance(self, event):
        try:
            broker = self.broker_text.GetValue()
            topic = self.topic_text.GetValue()
            message = bytes.fromhex(self.payload_text.GetValue())

            # event = event_pb2.Event()

            # # Populate header
            # event.header.event_type = "DEFAULT"
            # event.header.pub_id = "v_1"
            # event.header.token = "w3b_MV8xNjk1MTA5MjI5X1FOeEl8YloqWG5tZg"  
            # event.header.pub_time = 1695566547655
            # event.header.event_id = "1234abcd"

            # # Set payload
            # event.payload = b"{\"name\": \"John Doe\", \"page\": \"Home\"}" 

            # # Serialize to bytes 
            # data = event.SerializeToString()

            try:
                loop_count = int(self.mqtt_loop_count_text.GetValue())
            except ValueError:
                self.mqtt_console.AppendText("Invalid loop count value. Please enter a valid integer.\n")
                return

            try:
                port = int(self.port_text.GetValue())
            except ValueError:
                self.mqtt_console.AppendText("Invalid port number. Please enter a valid integer for the port.\n")
                return

            client = mqtt.Client()

            try:
                client.connect(broker)
            except Exception as e:
                self.mqtt_console.AppendText(f"Failed to connect to the broker: {e} \n")
                return

            total_time = 0
            for _ in range(loop_count):
                start_time = time.time()
                
                # Publish to the topic
                result = client.publish(topic, message)
                if result.rc != mqtt.MQTT_ERR_SUCCESS:
                    self.mqtt_console.AppendText(f"Failed to publish message: {mqtt.error_string(result.rc)} \n")
                    client.disconnect()
                    return

                end_time = time.time()
                total_time += (end_time - start_time)

            client.disconnect()

            average_time = total_time / loop_count
            self.mqtt_console.AppendText(f"Average time taken for {loop_count} publishes: {average_time} seconds \n")
        except Exception as e:
            self.mqtt_console.AppendText(f"Error: {str(e)}\n")

if __name__ == "__main__":
    app = wx.App()
    frame = PerformanceTester()
    frame.Show()
    app.MainLoop()

