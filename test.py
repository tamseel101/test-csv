import pandas as pd
from faker import Faker

# Initialize Faker instance
fake = Faker()

# Comprehend output with PII entities and their column numbers
comprehend_entities = [
    {'Entity': 'NAME', 'ColumnNumber': 1},
    {'Entity': 'DATE_TIME', 'ColumnNumber': 3},
    {'Entity': 'CREDIT_DEBIT_NUMBER', 'ColumnNumber': 4},
    # Add all PII entities here as per Amazon Comprehend output
]

# Helper functions to generate fake data for each PII type
def generate_fake_name():
    return fake.name()

def generate_fake_date():
    return fake.date_this_century()

def generate_fake_credit_card_number():
    return fake.credit_card_number(card_type="amex")

def generate_fake_cvv():
    return fake.credit_card_security_code()

def generate_fake_expiry():
    return fake.credit_card_expire()

def generate_fake_address():
    return fake.address()

def generate_fake_age():
    return fake.random_int(min=18, max=99)

def generate_fake_aws_key():
    return fake.uuid4()

def generate_fake_email():
    return fake.email()

def generate_fake_ip():
    return fake.ipv4()

def generate_fake_license_plate():
    return fake.license_plate()

def generate_fake_mac():
    return fake.mac_address()

def generate_fake_password():
    return fake.password()

def generate_fake_phone():
    return fake.phone_number()

def generate_fake_url():
    return fake.url()

def generate_fake_username():
    return fake.user_name()

def generate_fake_vehicle_id():
    return fake.bothify("???-####-???")

def generate_fake_bank_account():
    return fake.bban()

def generate_fake_routing_number():
    return fake.random_number(digits=9, fix_len=True)

def generate_fake_passport():
    return fake.passport_number()

def generate_fake_ssn():
    return fake.ssn()

# Dictionary to map each PII type to its corresponding fake data generator
pii_generators = {
    'NAME': generate_fake_name,
    'DATE_TIME': generate_fake_date,
    'CREDIT_DEBIT_NUMBER': generate_fake_credit_card_number,
    'CREDIT_DEBIT_CVV': generate_fake_cvv,
    'CREDIT_DEBIT_EXPIRY': generate_fake_expiry,
    'ADDRESS': generate_fake_address,
    'AGE': generate_fake_age,
    'AWS_ACCESS_KEY': generate_fake_aws_key,
    'AWS_SECRET_KEY': generate_fake_aws_key,
    'EMAIL': generate_fake_email,
    'IP_ADDRESS': generate_fake_ip,
    'LICENSE_PLATE': generate_fake_license_plate,
    'MAC_ADDRESS': generate_fake_mac,
    'PASSWORD': generate_fake_password,
    'PHONE': generate_fake_phone,
    'PIN': generate_fake_cvv,
    'SWIFT_CODE': generate_fake_aws_key,
    'URL': generate_fake_url,
    'USERNAME': generate_fake_username,
    'VEHICLE_IDENTIFICATION_NUMBER': generate_fake_vehicle_id,
    'BANK_ACCOUNT_NUMBER': generate_fake_bank_account,
    'BANK_ROUTING': generate_fake_routing_number,
    'PASSPORT_NUMBER': generate_fake_passport,
    'SSN': generate_fake_ssn,
}

# Function to replace PII in each row based on the entity type
def replace_pii_data(row, pii_mappings):
    for entity_info in pii_mappings:
        col_index = entity_info['ColumnNumber'] - 1  # Adjust to zero-based index
        col_name = row.index[col_index]  # Map column number to column name
        
        # Replace data based on the entity type
        entity_type = entity_info['Entity']
        if entity_type in pii_generators:
            row[col_name] = pii_generators[entity_type]()
    
    return row

# Main function to process the CSV, replace PII, and save to a new CSV
def anonymize_pii_in_csv(input_csv_path, output_csv_path):
    # Read the CSV and extract column names
    original_data = pd.read_csv(input_csv_path)
    
    # Generate anonymized data for each row
    anonymized_rows = []
    for _, row in original_data.iterrows():
        row = replace_pii_data(row, comprehend_entities)
        anonymized_rows.append(row)
    
    # Create new DataFrame and save to CSV
    anonymized_data = pd.DataFrame(anonymized_rows, columns=original_data.columns)
    anonymized_data.to_csv(output_csv_path, index=False)

# Define file paths for input and output
input_csv = "test_data.csv"
output_csv = "anonymized_data.csv"

# Run the anonymization process
anonymize_pii_in_csv(input_csv, output_csv)
print(f"Anonymized CSV saved as '{output_csv}'")
