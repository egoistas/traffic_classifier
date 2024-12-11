# Network Traffic Analysis for Exploit Detection

## Overview

This project leverages network traffic data to detect potential exploit-based attacks in networks. The approach involves capturing network traffic using Wireshark (or TShark) and analyzing the data with machine learning techniques. The goal is to automatically detect exploits and provide predictive results in real-time.

---

## Process

### 1. Packet Capture
Network traffic data is captured using TShark and saved in `.pcap` format.

### 2. Feature Extraction
The captured network traffic data is converted into a CSV file using TShark. The following fields are extracted:

- `frame.time_relative`: Time since the previous packet.
- `frame.len`: Packet length.
- `ip.src`: Source IP address.
- `ip.dst`: Destination IP address.
- `ip.proto`: Protocol (e.g., TCP, UDP).
- `ip.ttl`: Packet's "Time to Live."
- `tcp.srcport`, `tcp.dstport`: Source and destination TCP ports.
- `udp.srcport`, `udp.dstport`: Source and destination UDP ports.

### 3. Data Processing for the Model
Once features are extracted, the following steps are applied:

- Mapping protocols and services to their respective fields.
- Creating new features and applying one-hot encoding for model training.

### 4. Prediction
The processed data is fed into a machine learning model, which predicts whether the traffic data contains exploits. The output categorizes the traffic as either an attack or benign, and identifies exploit types.

### 5. Continuous Monitoring
The entire process can run in a loop, capturing new traffic data every 45 seconds, extracting features, processing the data, and predicting potential attacks.

---

## Key Components

- **Network Packet Capture with TShark:** Traffic data is captured and stored in `.pcap` files.
- **Feature Extraction:** Extracts features like timestamps, packet lengths, ports, IP addresses, etc., from `.pcap` files.
- **Data Processing and Normalization:** Prepares data for the machine learning model (e.g., one-hot encoding, feature scaling).
- **Machine Learning Model:** Trained to predict the presence of exploits in the data.
- **Continuous Data Flow:** An infinite loop for data capture, processing, and attack prediction.

---

## Requirements

To run this project, you need:

- Python 3.x
- TShark (packet capturing tool)
- Python Libraries:
  - `pandas`
  - `scikit-learn`
  - `joblib`

Install the required libraries with:

```bash
pip install -r requirements.txt
```

---

## Usage

To execute the project:

1. Run `capture_and_process.ps1` to start capturing network traffic.
2. The script will collect data, process it, and run the model to predict attacks.
3. Prediction results will be displayed in the console.

---

## Notes

- Captured data must adhere to the specified feature extraction format.
- The model is trained using data based on `processed_features.csv`, which must be available in the same directory.

---
