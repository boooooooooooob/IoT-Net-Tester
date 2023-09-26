# IoTex Performance Tester Tool

A cross-platform tool that enables performance testing for HTTPS and MQTT protocols and provides an interactive GUI to convert JSON data to Protocol Buffers (protobuf).

The Performance Tester Tool is a lightweight, purpose-built application designed to facilitate testing of IoT devices that communicate via HTTP and MQTT protocols. The motivation behind the creation of this tool emerged from a few key needs:

1. `IoT Device Testing`: A primary objective was to evaluate IoT devices' communication capabilities, especially those interacting through HTTP and MQTT.
2. `Simplicity & Lightweight`: While tools like Postman offer robust functionality, they often come with a complexity and heft that might be overwhelming for simple testing needs. This tool aims to bridge the gap by providing essential testing functions without the overhead of more extensive platforms.
3. `Compatibility with w3bstream IoTex`: w3bstream IoTex is a specialized platform that offers custom HTTP and MQTT services. A unique challenge faced was the specific message format constraints imposed by w3bstream, especially for MQTT communications. This tool seamlessly integrates a converter that transforms user-inputted JSON data into the Protocol Buffers (protobuf) format, ensuring compatibility with the w3bstream's requirements.

## Features

- `HTTPS Testing`: Perform POST requests and measure the average response time.
- `MQTT Testing`: Publish messages to specified MQTT topics and measure the average response time.
- `Protobuf Conversion`: Convert user-inputted JSON data to compressed Protocol Buffers format.

## Prerequisites

- Python 3.x
- wxPython
- MQTT
- Protocol Buffers (protobuf)

## Installation

### Clone the repository:

```bash
git clone git@github.com:boooooooooooob/IoT-Net-Tester.git
cd IoT-Net-Tester
```

### Set up a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
```

### Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

Choose the appropriate tab for the operation you wish to perform:

- `HTTPS Tab`: Enter the desired URL, headers, params, and body payload, set the loop count, and click "Test" to measure the average response time of POST requests.
- `MQTT Tab`: Enter the broker details, topic, payload, and set the loop count. Click "Test" to publish messages to the MQTT broker and measure the average response time.
- `JSON to Protobuf Tab`: Input your JSON data, and click "Convert" to get the compressed protobuf representation.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.
