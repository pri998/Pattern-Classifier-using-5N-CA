import pandas as pd

# Function to convert decimal to binary string
def to_base2(decimal, length):
    base2 = bin(decimal)[2:]
    return base2.zfill(length)

# Function to convert binary string to decimal
def to_decimal(binary_str):
    return int(binary_str, 2)

# Function to compute the next state based on the given rule
def next_state(rule, state, length):
    new_state = '00' + state + '00'
    next_state = ''
    for j in range(length):
        pqr = new_state[j:j + 5]
        index = to_decimal(pqr)
        next_state += rule[31 - index]
    return next_state

# Function to find the attractor
def find_attractor(initial_state, rule, length):
    current_state = initial_state
    seen_states = set()  # To detect cycles
    while current_state not in seen_states:
        seen_states.add(current_state)
        next_state_value = next_state(rule, current_state, length)
        if next_state_value == current_state:
            break
        current_state = next_state_value
    return current_state

# Function to load data from Excel file
def load_data(filename):
    df = pd.read_excel(filename, dtype={'encodedData': str, 'classInfo': int})
    data = list(df.itertuples(index=False, name=None))
    return data

# Function to load rules from Excel file
def load_rules(filename):
    df = pd.read_excel(filename, dtype={'rule': int})
    rules = df['rule'].tolist()
    return rules

def main():
    # Load training data
    training_filename = r"C:\Users\PRIYA DIVYA\Downloads\Breast_encoded_forTraining.xlsx"  # Training Excel file path
    training_data = load_data(training_filename)

    # Load test data
    test_filename = r"C:\Users\PRIYA DIVYA\Downloads\Breast_encoded_forTesting.xlsx"  # Testing Excel file path
    test_data = load_data(test_filename)

    # Load rules
    rules_filename = r"C:\Users\PRIYA DIVYA\Downloads\RulesToCheck(few).xlsx"  # Rules Excel file path
    rules = load_rules(rules_filename)

    length = 18  # Length of encoded data for Breast Cancer dataset

    for eca in rules:
        rule = to_base2(eca, 32)  # Ensure the rule is 32 bits long

        attractor_counts = {}  # Attractor -> (class1 count, class2 count)

        # Process each entry in the training data
        for encoded_data, class_info in training_data:
            attractor = find_attractor(encoded_data, rule, length)

            if attractor not in attractor_counts:
                attractor_counts[attractor] = [0, 0]

            if class_info == 1:
                attractor_counts[attractor][0] += 1
            elif class_info == 2:
                attractor_counts[attractor][1] += 1

        # Determine predicted class based on majority voting or tie handling
        attractor_to_class = {}  # Attractor -> Predicted class
        previous_predicted_class = 1  # Start with class 1

        for attractor, counts in attractor_counts.items():
            class1_count, class2_count = counts
            if class1_count > class2_count:
                predicted_class = 1
            elif class2_count > class1_count:
                predicted_class = 2
            else:
                # Handle the tie case by alternating the class
                if previous_predicted_class == 2:
                    predicted_class = 1
                else:
                    predicted_class = 2

            attractor_to_class[attractor] = predicted_class
            previous_predicted_class = predicted_class  # Update previous prediction

        # Testing phase
        correct_predictions = 0
        for encoded_data, actual_class in test_data:
            attractor = find_attractor(encoded_data, rule, length)
            predicted_class = attractor_to_class.get(attractor, -1)

            if predicted_class == actual_class:
                correct_predictions += 1

        accuracy = (correct_predictions / len(test_data)) * 100
        #print(f"Testing Accuracy for ECA rule {eca}: {accuracy:.2f}%")
        print(f"{accuracy:.2f}%")

if __name__ == "__main__":
    main()
