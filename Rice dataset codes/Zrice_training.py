import pandas as pd

# Function to convert decimal to binary string
def to_base2(decimal, length):
    base2 = bin(decimal)[2:]  # Convert decimal to binary and remove '0b'
    return base2.zfill(length)  # Pad with leading zeros

# Function to convert binary string to decimal
def to_decimal(binary_str):
    try:
        return int(binary_str, 2)
    except ValueError as e:
        print(f"Error converting binary_str to decimal: {binary_str}")
        raise e

# Function to compute the next state based on the given rule
def next_state(rule, state, length):
    new_state = "00" + state + "00"
    next_state_result = ""
    for i in range(length):
        pqr = new_state[i:i + 5]
        if len(pqr) < 5:
            continue  # Skip if pqr is not of length 5
        # Ensure pqr is a valid binary string
        if not set(pqr).issubset({'0', '1'}):
            print(f"Invalid binary substring: {pqr}")
            continue
        index = to_decimal(pqr)
        next_state_result += rule[31 - index]
    return next_state_result

# Function to find the attractor
def find_attractor(initial_state, rule, length):
    current_state = initial_state
    while True:
        next_state_value = next_state(rule, current_state, length)
        if next_state_value == current_state:
            return current_state
        current_state = next_state_value

# Load data and rules from Excel file
def load_data_and_rules(data_filename, rules_filename):
    df_data = pd.read_excel(data_filename, dtype={'encodedData': str, 'classInfo': int})
    df_rules = pd.read_excel(rules_filename)

    data = []
    for _, row in df_data.iterrows():
        encoded_data = row['encodedData'].strip()  # Ensure it is a string and strip spaces
        encoded_data = ''.join(filter(lambda x: x in '01', encoded_data))  # Remove any non-binary characters
        class_info = row['classInfo']
        data.append((encoded_data, class_info))

    rules = df_rules['rule'].tolist()

    return data, rules

def main():
    data_filename = r"C:\Users\PRIYA DIVYA\Desktop\rice dataset\riceTraining.xlsx"  # Excel file path for data
    rules_filename = r"C:\Users\PRIYA DIVYA\Downloads\RulesToCheck(few).xlsx"  # Excel file path for rules
    data, rules = load_data_and_rules(data_filename, rules_filename)

    length = 21  # Length of encoded data

    for eca in rules:
        rule = to_base2(eca, 32)
        
        attractor_counts = {}  # Attractor -> (class0 count, class1 count)
        attractor_to_class = {}  # Attractor -> Predicted class

        # Process each entry in the data
        for encoded_data, class_info in data:
            attractor = find_attractor(encoded_data, rule, length)
            
            if attractor not in attractor_counts:
                attractor_counts[attractor] = [0, 0]

            if class_info == 0:
                attractor_counts[attractor][0] += 1
            elif class_info == 1:
                attractor_counts[attractor][1] += 1

        previous_predicted_class = 0  # Start with class 0

        # Determine predicted class
        for attractor, counts in attractor_counts.items():
            class0_count, class1_count = counts
            if class0_count > class1_count:
                predicted_class = 0
            elif class1_count > class0_count:
                predicted_class = 1
            else:
                # Handle the tie case by alternating the class
                predicted_class = 1 - previous_predicted_class
            attractor_to_class[attractor] = predicted_class
            previous_predicted_class = predicted_class  # Update previous prediction

        # Calculate the efficiency
        n = len(data)  # Total number of patterns in the training set
        k = len(attractor_counts)  # Number of useful attractors
        sum_Ai = sum(max(counts) for counts in attractor_counts.values())  # Maximum count over classes for each attractor

        training_efficiency = (sum_Ai / n) * 100
        #print(f"Training Efficiency for ECA rule {eca}: {training_efficiency:.2f}%")
        print(f"{training_efficiency:.2f}%")

if __name__ == "__main__":
    main()


