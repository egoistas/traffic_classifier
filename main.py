import subprocess
import time
import pandas as pd

# Define file paths
pcap_file = "capture.pcap"
csv_file = "extracted_features.csv"
processed_csv = "processed_features_with_service_and_state.csv"
final_csv = "final_features_for_prediction.csv"

# Function to capture packets
def capture_packets():
    print("Capturing packets...")
    capture_command = [
        "tshark", "-i", "WiFi", "-T", "fields", "-e", "frame.time_relative", "-e", "frame.len", 
        "-e", "ip.src", "-e", "ip.dst", "-e", "ip.proto", "-e", "ip.ttl", "-e", "tcp.srcport", 
        "-e", "tcp.dstport", "-e", "udp.srcport", "-e", "udp.dstport", "-w", pcap_file
    ]
    # Start capturing in a background process
    capture_process = subprocess.Popen(capture_command)
    time.sleep(3)  # Capture for 10 seconds (adjust as needed)
    capture_process.terminate()  # Stop the capture after 45 seconds

# Function to extract features from pcap
def extract_features():
    print("Extracting features from pcap...")

    # Define the tshark command with proper field delimiters
    extract_command = [
        "tshark", "-r", pcap_file, "-T", "fields", "-E", "separator=,", 
        "-e", "frame.time_relative", "-e", "frame.len", "-e", "ip.src", "-e", "ip.dst", "-e", "ip.proto",
        "-e", "ip.ttl", "-e", "tcp.srcport", "-e", "tcp.dstport", "-e", "udp.srcport", "-e", "udp.dstport"
    ]
    
    # Open the output file and ensure data is written with a comma separator (CSV)
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        subprocess.run(extract_command, stdout=f)

    # Check if file is created and contents look correct
    with open(csv_file, 'r', encoding="utf-8") as f:
        print(f.read())  # Debug print to verify if the data is correctly formatted

# Function to preprocess data
def preprocess_data():
    print("Preprocessing data...")
    subprocess.run(["python", "construct_prediction_inputs.py"])

# Function for final preprocessing and prediction
def final_preprocess_and_predict():
    print("Making predictions...")
    subprocess.run(["python", "predict_attack.py"])

# Function to display predictions
def make_prediction():
    print("Final prediction results:")
    subprocess.run(["python", "fire_prediction.py"])

def rules_creating():
    print("Creating rules based on the prediction:")
    subprocess.run(["python", "create_rules.py"])    

# Infinite loop to run the process continuously
while True:
    # Capture packets
    capture_packets()
    time.sleep(2)

    # Extract features
    extract_features()
    time.sleep(5)

    # Preprocess the data
    preprocess_data()
    time.sleep(2)

    # Final preprocessing and prediction
    final_preprocess_and_predict()
    time.sleep(2)

    # Make prediction
    make_prediction()
    time.sleep(2)

    rules_creating()
    time.sleep(2)

    print("Continue the pipeline")
    time.sleep(2)
