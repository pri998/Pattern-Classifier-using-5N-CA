import pandas as pd
import os
import numpy as np

# Function to perform interval encoding
def interval_encode(series, n_bins):
    # Create bins
    bins = np.linspace(series.min(), series.max(), n_bins + 1)
    # Digitize the series into bins
    bin_indices = np.digitize(series, bins) - 1
    # Create a dictionary for interval encoding
    interval_dict = {i: (bins[i], bins[i+1]) for i in range(n_bins)}
    return bin_indices, interval_dict, bins

'''# Function to perform one-hot encoding for categorical attributes
def one_hot_encode(df, attribute):
    encoded_columns = pd.get_dummies(df[attribute], prefix=attribute)
    # Convert boolean values to integers (0 and 1)
    encoded_columns = encoded_columns.astype(int)
    return encoded_columns'''

# Function to encode all attributes in the DataFrame
def encode_attributes(df, continuous_attributes, bin_counts):
    encoding_info = {}
    encoded_dfs = []
    binary_cols = []
    
    # Encode continuous attributes with interval encoding
    for attr in continuous_attributes:
        n_bins = bin_counts.get(attr, 4)  # Default to 4 bins if not specified
        encoded_series, attr_interval_dict, bins = interval_encode(df[attr], n_bins)
        max_value = encoded_series.max()
        max_bit_length = len(bin(max_value)) - 2  # Calculate bit length based on binary representation
        df[f'{attr}_encoded'] = encoded_series
        df[f'{attr}_binary'] = df[f'{attr}_encoded'].apply(lambda x: format(int(x), f'0{max_bit_length}b'))
        binary_cols.append(f'{attr}_binary')
        encoding_info[attr] = {
            'encoding_type': 'interval',
            'interval_dict': attr_interval_dict,
            'max_bit_length': max_bit_length,
            'n_bins_used': n_bins,
            'attribute_range': (df[attr].min(), df[attr].max()),
            'bins': bins
        }
    
    '''# Encode categorical attributes with one-hot encoding
    for attr in categorical_attributes:
        encoded_columns = one_hot_encode(df, attr)
        encoded_dfs.append(encoded_columns)
        binary_cols.extend(encoded_columns.columns.tolist())
        encoding_info[attr] = {
            'encoding_type': 'one-hot'
        }'''
    
    # Combine all encoded DataFrames
    encoded_df = pd.concat([df] + encoded_dfs, axis=1)
    
    # Combine all encoded attributes into a single column for each instance
    encoded_df['combined_encoded'] = encoded_df[binary_cols].astype(str).apply(lambda row: ''.join(row), axis=1)
    
    return encoded_df, encoding_info

# File paths
input_path = r"C:\Users\PRIYA DIVYA\Desktop\Pattern classif using CA\breastCancer dataset\BreastCancer raw dataset.xlsx"
output_path = os.path.expanduser(r"C:\Users\PRIYA DIVYA\Downloads\raisinEncode_CSV.xlsx")

# Load the CSV file
df = pd.read_excel(input_path)

# Define lists of continuous attributes
continuous_attributes = ['Age', 'BMI', 'Glucose', 'Insulin', 'HOMA','Leptin','Adiponectin','Resistin','MCP']

# Modifying the number of bins for continuous attributes
bin_counts = {
    'Age':3,
    'BMI':3,
    'Glucose':3,
    'Insulin':3,
    'HOMA':3,
    'Leptin':3,
    'Adiponectin':3,
    'Resistin':3,
    'MCP':3,
}

# Encode attributes
encoded_df, encoding_info = encode_attributes(df, continuous_attributes, bin_counts)

# Save the encoded DataFrame to a new Excel file
encoded_df.to_excel(output_path, index=False)

# Display encoding details
for attr, info in encoding_info.items():
    print(f"{attr} Encoding Type: {info['encoding_type']}")
    if info['encoding_type'] == 'interval':
        print(f"Interval Encoding Dictionary: {info['interval_dict']}")
        print(f"Maximum Bit Length Used: {info['max_bit_length']} bits")
        print(f"Number of Bins Used: {info['n_bins_used']}")
        print(f"Attribute Range: {info['attribute_range']}")
    elif info['encoding_type'] == 'one-hot':
        print(f"One-Hot Encoded Columns: {list(encoded_df.filter(regex=f'^{attr}_'))}")

# Display the encoded DataFrame
print(encoded_df.head())