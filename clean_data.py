import pandas as pd

def clean_extracted_data(input_file, output_file):
    """
    Cleans the extracted data from TShark output and ensures all required features are included.

    Parameters:
        input_file (str): Path to the extracted raw CSV file.
        output_file (str): Path to save the cleaned CSV file.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Define the columns extracted from TShark, matching the columns in your dataset
    column_names = [
        "frame.time_relative", "frame.len", "ip.src", "ip.dst", "ip.proto",
        "ip.ttl", "tcp.srcport", "tcp.dstport", "udp.srcport", "udp.dstport"
    ]
    
    # Load the raw data with correct encoding (assuming ascii based on previous output)
    try:
        data = pd.read_csv(input_file, encoding='ascii', delimiter='\t', names=column_names, header=None)
        print(f"File '{input_file}' loaded successfully!")
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

    # Convert 'frame.time_relative' to numeric (float)
    data['frame.time_relative'] = pd.to_numeric(data['frame.time_relative'], errors='coerce')

    # Now let's create the necessary features from the raw data
    # Example: 'dur', 'spkts', 'dpkts', 'sbytes', 'dbytes', etc.
    # These will be computed based on the raw data we just loaded.
    
    data['dur'] = data['frame.time_relative'].max() - data['frame.time_relative'].min()  # Duration
    data['spkts'] = data['ip.src'].count()  # Source packet count
    data['dpkts'] = data['ip.dst'].count()  # Destination packet count
    data['sbytes'] = data['frame.len'].sum()  # Source bytes
    data['dbytes'] = data['frame.len'].sum()  # Destination bytes (just as an example)
    data['rate'] = data['frame.len'].sum() / (data['dur'] + 1e-6)  # Rate

    # Handle TTL column safely
    sttl_mode = data['ip.ttl'].mode()
    if not sttl_mode.empty:
        data['sttl'] = sttl_mode[0]  # Use the most frequent TTL value
    else:
        data['sttl'] = 0  # Default value if mode() returns empty
    
    data['ct_srv_src'] = data['tcp.srcport'].count()  # Connection service source count
    data['ct_dst_ltm'] = data['tcp.dstport'].count()  # Connection destination count
    
    # Now save the cleaned data to a new CSV
    data.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Cleaned data saved to '{output_file}'.")

    return data


# Example usage:
input_file = "extracted_features.csv"  # Path to the extracted raw data
output_file = "cleaned_features.csv"   # Path to save the cleaned data
cleaned_data = clean_extracted_data(input_file, output_file)
