import pandas as pd
from collections import Counter
from datetime import datetime

attck_mapping = {
    "Analysis": "T1595 (Active Scanning), T1590 (Gather Victim Information)",
    "Backdoor": "T1543 (Create or Modify System Process)",
    "DoS": "T1499 (Endpoint DoS), T1569 (Network DoS)",
    "Exploits": "T1203 (Exploitation for Privilege Escalation)",
    "Fuzzers": "T1595.002 (Scanning for Vulnerabilities)",
    "Generic": "No specific ATT&CK mapping",
    "Normal": "No malicious behavior",
    "Reconnaissance": "T1595 (Active Scanning), T1592 (Gather File Information)",
    "Shellcode": "T1055 (Process Injection)",
    "Worms": "T1072 (Replication Through Removable Media)"
}

def generate_yara_rule(category, counts, attck_mapping):
    attck_techniques = attck_mapping.get(category, "No mapping available")
    return f"""
rule {category}_Detection
{{
    meta:
        description = "Detects activity related to {category}"
        author = "Automated Script"
        category = "{category}"
        total_occurrences = "{counts}"
        ATTACK_Techniques = "{attck_techniques}"
        date = "{datetime.now().strftime('%Y-%m-%d')}"
    
    condition:
        true
}}
"""

def analyze_predictions(file_path):
    df = pd.read_csv(file_path)
    category_counts = Counter(df['predicted_category'])
    most_dominant_category, most_dominant_count = category_counts.most_common(1)[0]
    print(f"The most dominant category is: {most_dominant_category} with {most_dominant_count} occurrences.\n")
    return generate_yara_rule(most_dominant_category, most_dominant_count, attck_mapping)

def main():
    file_path = "predictions_with_categories.csv"
    yara_rule = analyze_predictions(file_path)
    print("Generated YARA Rule for the Most Dominant Category:\n")
    print(yara_rule)

if __name__ == "__main__":
    main()
