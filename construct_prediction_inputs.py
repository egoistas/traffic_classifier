import pandas as pd

# Load the raw data (you might need to adjust the file path)
column_names = [
    "frame.time_relative", "frame.len", "ip.src", "ip.dst", "ip.proto",
    "ip.ttl", "tcp.srcport", "tcp.dstport", "udp.srcport", "udp.dstport", "tcp.flags"
]

# Make sure you read it correctly using the appropriate encoding
raw_data = pd.read_csv("extracted_features.csv", encoding="utf-8", sep=",", names=column_names, header=None, on_bad_lines="skip")

# Protocol mapping (for translating protocol numbers to names)
protocol_mapping = {
    0: 'HOPOPT', 1: 'ICMP', 2: 'IGMP', 3: 'GGP', 4: 'IP-in-IP', 6: 'TCP', 17: 'UDP', 58: 'IPv6-ICMP', 80: 'HTTP', 443: 'HTTPS'
    # Add more protocol mappings here...
}

# Convert ip.proto into protocol names
raw_data['proto'] = raw_data['ip.proto'].map(protocol_mapping).fillna('unknown')

# Service mapping from ports
def map_service_from_ports(row):
    ports = [row['tcp.srcport'], row['tcp.dstport'], row['udp.srcport'], row['udp.dstport']]
    for port in ports:
        if pd.notna(port):
            port = int(port)
            if port == 80:
                return 'http'
            elif port == 443:
                return 'https'
            elif port == 21:
                return 'ftp'
            elif port == 25:
                return 'smtp'
            elif port == 53:
                return 'dns'
            elif port == 110:
                return 'pop3'
            elif port == 22:
                return 'ssh'
            # Add more port checks here...
    return 'unknown'

# Mapping connection state (TCP flags based)
def map_connection_state(row):
    if pd.notna(row.get('tcp.flags')):
        try:
            flags = int(row['tcp.flags'], 16)  # Convert hex string to int
            if flags & 0x01:  # FIN flag
                return 'FIN'
            elif flags & 0x02:  # SYN flag
                return 'SYN'
            elif flags & 0x04:  # RST flag
                return 'RST'
            elif flags & 0x10:  # ACK flag
                return 'ACK'
            elif flags & 0x18:  # PSH + ACK flag
                return 'PSH-ACK'
            elif flags & 0x29:  # FIN + PSH + ACK flag
                return 'FIN-PSH-ACK'
        except ValueError:
            return 'UNKNOWN'
    return 'UNKNOWN'

# Apply the mapping functions
raw_data['service'] = raw_data.apply(map_service_from_ports, axis=1)
raw_data['state'] = raw_data.apply(map_connection_state, axis=1)

# Grouping by source IP, destination IP, and protocol
grouped_data = raw_data.groupby(['ip.src', 'ip.dst', 'ip.proto'])

# Aggregating features: total duration, packet counts, byte counts, etc.
features = grouped_data.agg(
    dur=('frame.time_relative', lambda x: x.max() - x.min()),  # Duration of session
    spkts=('ip.src', 'count'),  # Source packet count
    dpkts=('ip.dst', 'count'),  # Destination packet count
    sbytes=('frame.len', lambda x: x[raw_data['ip.src'] == x.name[0]].sum()),  # Source byte count
    dbytes=('frame.len', lambda x: x[raw_data['ip.dst'] == x.name[1]].sum()),  # Destination byte count
    rate=('frame.len', lambda x: x.sum() / (x.max() - x.min() + 1e-6)),  # Rate (bytes/second)
    sttl=('ip.ttl', lambda x: x.mode()[0] if not x.mode().empty else 0),  # TTL mode
    ct_srv_src=('tcp.srcport', lambda x: x.notna().sum()),  # Count of services from source
    ct_dst_ltm=('tcp.dstport', lambda x: x.notna().sum())  # Count of services to destination
).reset_index()

# Adding string-mapped protocol, service, and state info to the features
proto_mapping = raw_data.groupby(['ip.src', 'ip.dst', 'ip.proto'])['proto'].first().reset_index()
features = features.merge(proto_mapping, on=['ip.src', 'ip.dst', 'ip.proto'], how='left')

service_mapping = raw_data.groupby(['ip.src', 'ip.dst', 'ip.proto'])['service'].first().reset_index()
state_mapping = raw_data.groupby(['ip.src', 'ip.dst', 'ip.proto'])['state'].first().reset_index()
features = features.merge(service_mapping, on=['ip.src', 'ip.dst', 'ip.proto'], how='left')
features = features.merge(state_mapping, on=['ip.src', 'ip.dst', 'ip.proto'], how='left')

# Saving the processed data to a CSV with UTF-8 encoding
features.to_csv("processed_features_with_service_and_state.csv", index=False, encoding='utf-8')

print("Processed data saved to 'processed_features_with_service_and_state.csv'")
