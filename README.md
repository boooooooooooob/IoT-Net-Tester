# IoTex Performance Tester Tool

A cross-platform tool that enables performance testing for HTTPS and MQTT protocols and provides an interactive GUI to convert JSON data to Protocol Buffers (protobuf).

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
