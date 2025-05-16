import pandas as pd
import numpy as np

# Function to perform interval encoding
def interval_encode(series, n_bins):
    # Replace missing values with mean
    series = series.fillna(series.mean())
    # Create bins
    bins = np.linspace(series.min(), series.max(), n_bins + 1)
    # Digitize the series into bins
    bin_indices = np.digitize(series, bins) - 1
    # Create a dictionary for interval encoding
    interval_dict = {i: (bins[i], bins[i+1]) for i in range(n_bins)}
    return bin_indices, interval_dict, bins

# Function to perform binary encoding for categorical attributes
def binary_encode(series, unique_values):
    # Create a dictionary to map unique values to binary strings
    num_bits = len(bin(len(unique_values) - 1)) - 2  # Calculate bit length needed
    value_to_binary = {val: format(i, f'0{num_bits}b') for i, val in enumerate(unique_values)}
    # Map the series values to binary strings
    encoded_series = series.map(value_to_binary)
    return encoded_series, value_to_binary, num_bits

# Function to encode all attributes in the DataFrame
def encode_attributes(df, continuous_attributes, categorical_attributes, bin_counts, cat_values_dict):
    encoding_info = {}
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
    
    # Encode categorical attributes with binary encoding
    for attr in categorical_attributes:
        all_values = cat_values_dict[attr]
        encoded_series, value_to_binary, num_bits = binary_encode(df[attr], all_values)
        df[f'{attr}_binary'] = encoded_series
        binary_cols.append(f'{attr}_binary')
        encoding_info[attr] = {
            'encoding_type': 'binary',
            'value_to_binary': value_to_binary,
            'num_bits': num_bits
        }
    
    # Combine all encoded attributes into a single column for each instance
    encoded_df = df[binary_cols].astype(str).apply(lambda row: ''.join(row), axis=1)
    df['combined_encoded'] = encoded_df
    
    return df, encoding_info

# File paths
input_path = r"C:\Users\PRIYA DIVYA\Desktop\Adult dataset\adult raw datafile.xlsx"
output_path = r"C:\Users\PRIYA DIVYA\Desktop\Adult dataset\adult encoded.xlsx"

# Load the Excel file
df = pd.read_excel(input_path)

# Define lists of continuous and categorical attributes
continuous_attributes = ['age', 'fnlwgt', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
categorical_attributes = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'sex', 'native-country']

# Define possible values for categorical attributes
cat_values_dict = {
    'workclass': ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'],
    'education': ['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'],
    'marital-status': ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'],
    'occupation': ['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'],
    'relationship': ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'],
    'race': ['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'],
    'sex': ['Female', 'Male'],
    'native-country': ['United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong']
}

# Modifying the number of bins for continuous attributes
bin_counts = {
    'age': 3,
    'fnlwgt': 3,
    'education-num': 3,
    'capital-gain': 3,
    'capital-loss': 3,
    'hours-per-week': 3,
}

# Encode attributes
encoded_df, encoding_info = encode_attributes(df, continuous_attributes, categorical_attributes, bin_counts, cat_values_dict)

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
    elif info['encoding_type'] == 'binary':
        print(f"Binary Encoding Dictionary: {info['value_to_binary']}")
        print(f"Number of Bits Used: {info['num_bits']}")

# Display the encoded DataFrame
print(encoded_df.head())
