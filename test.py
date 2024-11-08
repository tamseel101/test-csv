import pandas as pd
from faker import Faker
from datetime import datetime

import random

# Initialize Faker instance
fake = Faker()

# Comprehend output with PII entities and their column numbers
comprehend_entities = [
    {'Entity': 'NAME', 'ColumnNumber': 1},
    {'Entity': 'NAME', 'ColumnNumber': 2},
    {'Entity': 'DATE_TIME', 'ColumnNumber': 3},
    {'Entity': 'CREDIT_DEBIT_NUMBER', 'ColumnNumber': 4},
    {'Entity': 'CREDIT_DEBIT_EXPIRY', 'ColumnNumber': 5},
    {'Entity': 'CREDIT_DEBIT_CVV', 'ColumnNumber': 7},
    {'Entity': 'MONEY', 'ColumnNumber': 8},
    {'Entity': 'USER_AGENT', 'ColumnNumber': 9}
    
]


# Helper functions to generate fake data for each PII type
def generate_fake_name():
    return fake.name()

def generate_fake_first_name():
    return fake.first_name()

def generate_fake_last_name():
    return fake.last_name()

def generate_fake_date():
    # Generate a fake date between January 1st and today’s date
    start_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()
    fake_date = fake.date_between(start_date=start_date, end_date=end_date)
    return fake_date


def generate_fake_credit_card_number():
    return fake.credit_card_number(card_type="amex")

def generate_fake_cvv(original_cvv):
    # Determine the length of the original CVV
    length_of_cvv = len(original_cvv)
    # Generate a random number with the same number of digits
    fake_cvv = ''.join(str(random.randint(0, 9)) for _ in range(length_of_cvv))
    return fake_cvv

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

def generate_fake_amount(original_amount):
    # Check if there is a decimal point
    if '.' in original_amount:
        # Split the amount into integer and decimal parts
        integer_part, decimal_part = original_amount.split('.')
        integer_part = ''.join(filter(str.isdigit, integer_part))  # Remove any commas from integer part
        decimal_length = len(decimal_part)
    else:
        # If no decimal part, process only the integer part
        integer_part = ''.join(filter(str.isdigit, original_amount))
        decimal_length = 0

    # Generate a random integer with the same number of digits as the integer part
    length_of_integer_part = len(integer_part)
    lower_bound = 10**(length_of_integer_part - 1)
    upper_bound = (10**length_of_integer_part) - 1
    fake_integer_part = random.randint(lower_bound, upper_bound)

    # Format the integer part with commas
    formatted_integer_part = f"{fake_integer_part:,}"

    # Generate a random decimal part if needed
    if decimal_length > 0:
        fake_decimal_part = ''.join(str(random.randint(0, 9)) for _ in range(decimal_length))
        fake_amount = f"${formatted_integer_part}.{fake_decimal_part}"
    else:
        fake_amount = f"${formatted_integer_part}"

    return fake_amount

def generate_fake_user_agent():
    return fake.user_agent()

# Dictionary to map each PII type to its corresponding fake data generator
pii_generators = {
    'NAME': generate_fake_name,
    'MONEY': generate_fake_amount,
    'USER_AGENT': generate_fake_user_agent,
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
        col_index = entity_info['ColumnNumber']
        col_name = row.index[col_index]  # Map column number to column name
        
        # Replace data based on the entity type
        entity_type = entity_info['Entity']
        if entity_type in pii_generators:
            # For 'MONEY', pass the original value to preserve length
            if entity_type == 'MONEY':
                row[col_name] = pii_generators[entity_type](row[col_name])
            # elif entity_type == 'NAME' and col_name == 'name':
            #     row[col_name] = generate_fake_name()
            elif entity_type == 'NAME' and col_name == 'first_name':
                row[col_name] = generate_fake_first_name()
            elif entity_type == 'NAME' and col_name == 'last_name':
                row[col_name] = generate_fake_last_name()
            elif entity_type == 'CREDIT_DEBIT_CVV':
                row[col_name] = generate_fake_cvv(row[col_name])
            else:
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
