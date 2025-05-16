#include <bits/stdc++.h>
#include <fstream>
using namespace std;

// Convert decimal to binary string with fixed length
string toBase2(long long decimal, int length) {
    string base2 = "";
    while (decimal > 0) {
        base2 = to_string(decimal % 2) + base2;
        decimal /= 2;
    }
    base2.insert(base2.begin(), length - base2.length(), '0'); // pad leading 0s
    return base2;
}

// Convert binary string to decimal
long long ToDecimal(const string& str) {
    long long result = 0, factor = 1;
    for (int i = str.length() - 1; i >= 0; --i) {
        result += (str[i] - '0') * factor;
        factor *= 2;
    }
    return result;
}

// Compute next state using periodic boundary condition
string NextState(const string& rule, const string& str, int length) {
    string nextState = "";
    for (int i = 0; i < length; ++i) {
        string neighborhood = "";
        for (int offset = -2; offset <= 2; ++offset) {
            int idx = (i + offset + length) % length; // periodic wrap
            neighborhood += str[idx];
        }
        int index = ToDecimal(neighborhood);
        nextState += rule[31 - index];
    }
    return nextState;
}

// Detect multi-length cycles under periodic boundary
void CheckCycle(int length, const string& rule, int& multiCount, ofstream& outfile) {
    for (int i = 0; i < (1 << length); ++i) {
        string state = toBase2(i, length);
        unordered_set<long long> visited;
        long long curr = ToDecimal(state);
        visited.insert(curr);

        for (int j = 0; j < (1 << length); ++j) {
            string nextStr = NextState(rule, toBase2(curr, length), length);
            long long next = ToDecimal(nextStr);
            if (visited.count(next)) {
                if (next != curr) {
                    outfile << ToDecimal(rule) << endl;
                    multiCount++;
                    return;
                } else {
                    break; // single-length cycle
                }
            }
            visited.insert(next);
            curr = next;
        }
    }
}

int main() {
    int length;
    int multiCount = 0;
    cout << "Enter Length of CA: ";
    cin >> length;

    ofstream outfile("zzz");

    string s = "10000000000000000000000000000000"; // 1 ones, 31 zero
    sort(s.begin(), s.end());

    int count = 0;
    string rule;
    do {
        rule = s;
        count++;
        CheckCycle(length, rule, multiCount, outfile);
    } while (next_permutation(s.begin(), s.end()));

    outfile << "\nTotal rule permutations checked: " << count << endl;
    outfile << "Multi-length cycle forming rules found: " << multiCount << endl;
    outfile.close();

    cout << "Process completed." << endl;
    return 0;
}
