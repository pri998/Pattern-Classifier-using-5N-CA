#include <bits/stdc++.h>
#include <fstream>
using namespace std;

// Convert decimal to binary string of fixed length
string toBase2(long long decimal, int length) {
    string base2 = "";
    while (decimal > 0) {
        base2 += to_string(decimal % 2);
        decimal /= 2;
    }
    reverse(base2.begin(), base2.end());
    while (base2.length() < length) {
        base2 = "0" + base2;
    }
    return base2;
}

// Convert binary string to decimal
long long ToDecimal(string str) {
    long long fact = 1, ans = 0;
    for (int i = str.length() - 1; i >= 0; i--) {
        ans += (str[i] - '0') * fact;
        fact *= 2;
    }
    return ans;
}

// Generate next state using null boundary (padded with 00 on both sides)
string NextState(string rule, string str, int length) {
    string padded = "00" + str + "00";
    string next = "";
    for (int j = 0; j < length; j++) {
        string pqr = padded.substr(j, 5);
        int index = ToDecimal(pqr);
        next += rule[31 - index];
    }
    return next;
}

// Check whether the rule forms a multi-length cycle under null boundary
bool IsMultiLengthCycle(int length, string rule) {
    vector<int> visited(pow(2, length), 0);
    for (int i = 0; i < pow(2, length); i++) {
        string str = toBase2(i, length);
        vector<int> seen(pow(2, length), 0);
        long long curr = ToDecimal(str);
        seen[curr] = 1;
        long long next = ToDecimal(NextState(rule, str, length));

        for (int j = 0; j < pow(2, length); j++) {
            if (seen[next] == 0) {
                seen[next] = 1;
            } else {
                if (curr == next) {
                    break;
                } else {
                    return true;  // Multi-length cycle detected
                }
            }
            curr = next;
            next = ToDecimal(NextState(rule, toBase2(curr, length), length));
        }
    }
    return false;
}

int main() {
    int length;
    cout << "Enter Length of CA: ";
    cin >> length;

    // 🟡 Manually define the binary rule pattern here (as done in your code)
    //string s = "01111111111111111111111111111111"; 
      string s = "10000000000000000000000000000000";
    sort(s.begin(), s.end()); // Generates permutations

    ofstream outfile("zz");
    int total_checked = 0, multi_cycle_count = 0;

    do {
        string rule = s;
        total_checked++;
        if (IsMultiLengthCycle(length, rule)) {
            multi_cycle_count++;
            outfile << ToDecimal(rule) << endl;
        }
    } while (next_permutation(s.begin(), s.end()));

    outfile << "\nTotal rules checked: " << total_checked << endl;
    outfile << "Rules with multi-length cycles: " << multi_cycle_count << endl;
    outfile.close();

    cout << "Done. Results saved to multi_length_rules.txt" << endl;
    return 0;
}
