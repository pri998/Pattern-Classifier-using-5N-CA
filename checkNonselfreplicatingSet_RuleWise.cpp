#include <bits/stdc++.h>
using namespace std;

// Function to convert a decimal number to a binary string of length 32
string toBase2(long long decimal, int length = 32) {
    string base2 = "";
    while (decimal > 0) {
        base2 = to_string(decimal % 2) + base2;
        decimal /= 2;
    }
    base2.insert(base2.begin(), length - base2.length(), '0'); // Pad with leading zeros
    return base2;
}

// Function to get the middle bit of a 5-bit RMT (index from 0 to 31)
int getMiddleBit(int rmt) {
    return (rmt >> 2) & 1;  // Extract the 3rd bit from the left
}

// Function to check which set all non-self-replicating RMTs of a rule belong to
string CheckNonSelfReplicatingRMTsSet(const string& rule) {
    int belongsToSet = -1; // -1 = undefined, 0 = Set A, 1 = Set B
    vector<int> nonSelfReplicating;

    // Set A and Set B definitions (according to your given RMTs)
    set<int> SetA = {0, 1, 2, 3, 8, 9, 10, 11, 16, 17, 18, 19, 24, 25, 26, 27};
    set<int> SetB = {4, 5, 6, 7, 12, 13, 14, 15, 20, 21, 22, 23, 28, 29, 30, 31};

    // Check each RMT (0 to 31)
    for (int rmt = 0; rmt < 32; ++rmt) {
        int middleBit = getMiddleBit(rmt);
        int ruleBit = rule[31 - rmt] - '0';

        if (ruleBit != middleBit) { // Non-self-replicating
            nonSelfReplicating.push_back(rmt);
            int currentSet = (middleBit == 0) ? 0 : 1;

            // Set if undefined or check for inconsistency across sets
            if (belongsToSet == -1)
                belongsToSet = currentSet;
            else if (belongsToSet != currentSet)
                return "Non-self-replicating RMTs belong to both sets";
        }
    }

    if (nonSelfReplicating.empty()) return "No non-self-replicating RMTs";

    return (belongsToSet == 0) ? "All non-self-replicating RMTs are in Set A"
                               : "All non-self-replicating RMTs are in Set B";
}

int main() {
    long long ruleDecimal;
    
    // Take user input for the rule in decimal format
    cout << "Enter the rule in decimal: ";
    cin >> ruleDecimal;

    // Convert decimal rule to a 32-bit binary string
    string rule = toBase2(ruleDecimal);
    cout << "Rule in binary: " << rule << endl;

    // Validate the binary string (it should be 32 bits)
    if (rule.length() != 32) {
        cout << "Invalid input. Rule must be a valid 32-bit decimal." << endl;
        return 1;
    }

    // Call the function to check the non-self-replicating RMTs and the set they belong to
    string result = CheckNonSelfReplicatingRMTsSet(rule);
    
    // Display the result
    cout << "Result: " << result << endl;

    return 0;
}
