//checking the reversibility by entering the rule randomly as input:
#include<bits/stdc++.h>
using namespace std;

string toBase2(long long decimal, int length) {
    string base2 = "";
    while (decimal > 0) {
        int remainder = decimal % 2;
        base2 +=to_string(remainder);
        decimal /= 2;
    }
    reverse(base2.begin(), base2.end());  // Reverse to correct order
    while (base2.length() < length) {
        base2 = "0" + base2;
        }
    return base2;
}

long long ToDecimal(string str){
    long long fact=1;
    int n=str.length();
    long long ans=0;
    for(int i=n-1;i>=0;i--){
        ans+=(str[i]-'0')*fact;
        fact*=2;
    }
    return ans;
}

string NextState(string rule,string str,int length){ 
 string newSt="00"+str+"00"; 
 string nextState="";
 for(int j=0;j<length;j++){
 string pqr=newSt.substr(j,5);
 int index=ToDecimal(pqr);
 nextState+=rule[31-index];
 }
 return nextState;
}

void CheckCycle(int length , string rule){
    int SingleCycle = 0;
    vector<int> convergencePoint(pow(2, length), 0);
    for(int i = 0 ; i < pow(2 , length) ; i++){
        string str =toBase2(i,length);
        vector<int> check(pow(2, length), 0);  //creating a vector named check of size 2^length all initialised with 0
        long long currCell = ToDecimal(str);  //
        check[currCell]++; //
        long long NextCell = ToDecimal(NextState(rule , str , length)); //

        for(int j = 0 ; j < pow(2 , length) ; j++){
            if(check[NextCell] == 0){  //
                check[NextCell] = 1;   //
            }
            else{
                if(currCell == NextCell){
                    if(convergencePoint[NextCell]==0){
                    SingleCycle++;
                    convergencePoint[NextCell]++;
                    }
                    break; //
                }
                else{
                    cout<<"MultiLength Cycle Detected for rule "<<ToDecimal(rule)<<endl;
                    return;
                }
            }
            currCell = NextCell;

            NextCell = ToDecimal(NextState(rule , toBase2(currCell,length) , length)); //./.
        }
    }
    if(SingleCycle > 0){
        cout <<"SingleLength Cycle Detected with cycle count = "<<SingleCycle<<" for the rule "<< ToDecimal(rule)<<endl;
    }
    else{
        cout<<"No Such Cycle Detected"<<endl;
    }  
}

int main(){
int length;
cout<<endl<<"Enter Length of CA"<<endl;
cin>>length;

long long eca;
cout<<"Enter the eca rule in decimal : "<<endl;
cin>>eca;
string rule=toBase2(eca,32);
cout<<"The eca rule in binary is : "<<rule<<endl;
CheckCycle(length,rule);
return 0;
}
