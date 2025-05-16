#include <bits/stdc++.h>
#include <fstream>
using namespace std;

// Convert a decimal number to a binary string of a given length
string toBase2(long long decimal, int length) {
    string base2 = "";
    while (decimal > 0) {
        base2 = to_string(decimal % 2) + base2;
        decimal /= 2;
    }
    base2.insert(base2.begin(), length - base2.length(), '0'); // Pad with leading zeros
    return base2;
}

// Convert a binary string to a decimal number
long long ToDecimal(const string& str) {
    long long result = 0;
    long long factor = 1;
    for (int i = str.length() - 1; i >= 0; --i) {
        result += (str[i] - '0') * factor;
        factor *= 2;
    }
    return result;
}

// Compute the next state of the cellular automaton given the current state and rule
string NextState(const string& rule, const string& str, int length) {
    string nextState = "";
    for (int i = 0; i < length; ++i) {
        // Determine the 5-neighborhood with periodic boundaries
        string neighborhood = "";
        for (int offset = -2; offset <= 2; ++offset) {
            int neighborIndex = (i + offset + length) % length;
            neighborhood += str[neighborIndex];
        }
        // Convert the neighborhood to a decimal index
        int index = ToDecimal(neighborhood);
        // Apply the rule to determine the next state
        nextState += rule[31 - index];
    }
    return nextState;
}

/*alternate NextState function for periodic boundary:
string NextState(string rule, string str, int length) {
    // Create a padded string with periodic boundary conditions
    string paddedStr = str.substr(length - 2, 2) + str + str.substr(0, 2);
    string nextState = "";
    
    for (int j = 0; j < length; j++) {
        string pqr = paddedStr.substr(j, 5);
        int index = ToDecimal(pqr);
        nextState += rule[31 - index];
    }
    return nextState;
}*/

// Detect cycles in the cellular automaton's evolution
void CheckCycle(int length, const string& rule, int& multiCount, ofstream& outfile) {
    int singleCycle = 0;
    vector<int> convergencePoint(pow(2, length), 0);

    for (int i = 0; i < pow(2, length); ++i) {
        string str = toBase2(i, length);
        vector<int> check(pow(2, length), 0); //creating a vector named check of size 2^length all initialised with 0
        long long currCell = ToDecimal(str);
        check[currCell]++;

        long long nextCell = ToDecimal(NextState(rule, str, length));

        for (int j = 0; j < pow(2, length); ++j) {
            if (check[nextCell] == 0) {
                check[nextCell] = 1;
            } else {
                if (currCell == nextCell) {
                    if (convergencePoint[nextCell] == 0) {
                        singleCycle++;
                        convergencePoint[nextCell]++;
                    }
                    break;
                } else {
                    //cout<<"MultiLength Cycle Detected for rule "<<ToDecimal(rule)<<endl;
                    multiCount++;
                    return;
                }
            }
            currCell = nextCell;
            nextCell = ToDecimal(NextState(rule, toBase2(currCell, length), length));
        }
    }
    if (singleCycle > 0) {
        if(singleCycle>0){
            //outfile<<ToDecimal(rule)<<endl;
            outfile<<singleCycle<<endl;
            //outfile<<"SingleLength Cycle Detected with cycle count = "<<SingleCycle<<" for the rule "<< ToDecimal(rule)<<endl;
            }
        }
    else {
        outfile << "No Cycle Detected" << endl;
    }
}

int main() {
    int length;
    int multiCount = 0;
    cout << "Enter Length of CA: ";
    cin >> length;

    ofstream outfile("zz.txt");

    //............for checking rules in loop..........:->
    string s = "01111111111111111111111111111111";
    string rule;
    sort(s.begin(), s.end());
    int count = 0;
    do {
        rule = s;
        count++;
        if (count > 100000) {
            break;
        }
        CheckCycle(length, rule, multiCount, outfile);
    } while (next_permutation(s.begin(), s.end()));

    outfile << "Total rule permutations checked: " << count << endl;
    outfile << "Multi-length cycles detected: " << multiCount << endl;
    outfile << "Single-length cycles detected: " << (count - multiCount) << endl;

    cout << "Process completed." << endl;

    outfile.close();
    return 0;
}
