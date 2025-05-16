#print(f"{accuracy:.2f}%")
        #print(f"{precision:.2f}%")
        #print(f"{recall:.2f}%")
        #print(f"{f_measure:.2f}%")

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
    next_state_result = ''
    for j in range(length):
        pqr = new_state[j:j + 5]
        index = to_decimal(pqr)
        next_state_result += rule[31 - index]
    return next_state_result

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
    training_filename = r"C:\Users\PRIYA DIVYA\Desktop\rice dataset\riceTraining.xlsx"  # Training Excel file path
    training_data = load_data(training_filename)

    # Load test data
    test_filename = r"C:\Users\PRIYA DIVYA\Desktop\rice dataset\riceTesting.xlsx"  # Testing Excel file path
    test_data = load_data(test_filename)

    # Load rules
    rules_filename = r"C:\Users\PRIYA DIVYA\Downloads\RulesToCheck(few).xlsx"  # Rules Excel file path
    rules = load_rules(rules_filename)

    length = 21  # Length of encoded data

    for eca in rules:
        rule = to_base2(eca, 32)  # Ensure the rule is 32 bits long

        attractor_counts = {}  # Attractor -> (class0 count, class1 count)

        # Process each entry in the training data
        for encoded_data, class_info in training_data:
            attractor = find_attractor(encoded_data, rule, length)

            if attractor not in attractor_counts:
                attractor_counts[attractor] = [0, 0]

            if class_info == 0:
                attractor_counts[attractor][0] += 1
            elif class_info == 1:
                attractor_counts[attractor][1] += 1

        # Determine predicted class based on majority voting or tie handling
        attractor_to_class = {}  # Attractor -> Predicted class
        previous_predicted_class = 0  # Start with class 0

        for attractor, counts in attractor_counts.items():
            class0_count, class1_count = counts
            if class0_count > class1_count:
                predicted_class = 0
            elif class1_count > class0_count:
                predicted_class = 1
            else:
                # Handle the tie case by alternating the class
                if previous_predicted_class == 1:
                    predicted_class = 0
                else:
                    predicted_class = 1

            attractor_to_class[attractor] = predicted_class
            previous_predicted_class = predicted_class  # Update previous prediction

        # Initialize counters for evaluation metrics
        TP = {0: 0, 1: 0}
        FP = {0: 0, 1: 0}
        FN = {0: 0, 1: 0}

        # Testing phase
        correct_predictions = 0
        for encoded_data, actual_class in test_data:
            attractor = find_attractor(encoded_data, rule, length)
            predicted_class = attractor_to_class.get(attractor, -1)

            if predicted_class != -1:
                if predicted_class == actual_class:
                    correct_predictions += 1
                    TP[actual_class] += 1
                else:
                    FP[predicted_class] += 1
                    FN[actual_class] += 1

        accuracy = (correct_predictions / len(test_data)) * 100
        #print(f"Testing Accuracy for ECA rule {eca}: {accuracy:.2f}%")
        #print(f"{accuracy:.2f}%")

        # Calculate precision, recall, and F-measure for each class
        for cls in [0, 1]:
            precision = (TP[cls] / (TP[cls] + FP[cls])) * 100 if (TP[cls] + FP[cls]) > 0 else 0
            recall = (TP[cls] / (TP[cls] + FN[cls])) * 100 if (TP[cls] + FN[cls]) > 0 else 0
            f_measure = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
            #print(f"Class {cls} - Precision: {precision:.2f}%, Recall: {recall:.2f}%, F-measure: {f_measure:.2f}%")
            # Uncomment the line corresponding to the metric you want to print
            #if cls == 0:
                #print(f"{precision:.2f}%")
                #print(f"{recall:.2f}%")
                #print(f"{f_measure:.2f}%")
            if cls == 1:
                #print(f"{precision:.2f}%")
                #print(f"{recall:.2f}%")
                print(f"{f_measure:.2f}%")
if __name__ == "__main__":
    main()



