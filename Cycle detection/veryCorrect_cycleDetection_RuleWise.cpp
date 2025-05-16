#include <bits/stdc++.h>
using namespace std;

// Convert a decimal number to a binary string with fixed length
string toBase2(long long decimal, int length) {
    string base2 = "";
    while (decimal > 0) {
        int remainder = decimal % 2;
        base2 += to_string(remainder);
        decimal /= 2;
    }
    reverse(base2.begin(), base2.end());
    while (base2.length() < length) {
        base2 = "0" + base2;
    }
    return base2;
}

// Convert a binary string to a decimal number
long long ToDecimal(const string &str) {
    long long fact = 1;
    int n = str.length();
    long long ans = 0;
    for (int i = n - 1; i >= 0; i--) {
        ans += (str[i] - '0') * fact;
        fact *= 2;
    }
    return ans;
}

// Get the next state based on the rule and current configuration
string NextState(const string &rule, const string &str, int length) { 
    string newSt = "00" + str + "00";  // Add padding
    string nextState = "";
    for (int j = 0; j < length; j++) {
        string pqr = newSt.substr(j, 5);
        int index = ToDecimal(pqr);
        nextState += rule[31 - index];
    }
    return nextState;
}

// Check for cycles in the cellular automaton based on the rule
void CheckCycle(int length, const string &rule) {
    int SingleCycle = 0;
    vector<int> convergencePoint(pow(2, length), 0);

    for (int i = 0; i < (1 << length); i++) {
        string str = toBase2(i, length);
        vector<int> check(1 << length, 0);
        long long currCell = ToDecimal(str);
        check[currCell]++;
        long long NextCell = ToDecimal(NextState(rule, str, length));

        for (int j = 0; j < (1 << length); j++) {
            if (check[NextCell] == 0) {
                check[NextCell] = 1;
            } else {
                if (currCell == NextCell) {
                    if (convergencePoint[NextCell] == 0) {
                        SingleCycle++;
                        convergencePoint[NextCell]++;
                    }
                    break;
                } else {
                    cout << "MultiLength Cycle Detected for rule " << ToDecimal(rule) << endl;
                    return;
                }
            }
            currCell = NextCell;
            NextCell = ToDecimal(NextState(rule, toBase2(currCell, length), length));
        }
    }
    if (SingleCycle > 0) {
        cout << "SingleLength Cycle Detected with cycle count = " << SingleCycle 
             << " for the rule " << ToDecimal(rule) << endl;
    } else {
        cout << "No Such Cycle Detected" << endl;
    }
}

int main() {
    int length;
    cout << "Enter Length of CA: ";
    cin >> length;

    long long eca;
    cout << "Enter the rule in decimal: ";
    cin >> eca;
    string rule = toBase2(eca, 32);  // Convert rule to a 32-bit binary string
    cout << "The rule in binary is: " << rule << endl;

    CheckCycle(length, rule);

    return 0;
}
