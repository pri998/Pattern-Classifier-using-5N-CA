#include<bits/stdc++.h>
#include <string>
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

int ToDecimal(string str){
    int fact=1;
    int n=str.length();
    int ans=0;
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

int main(){
int length;
cout<<endl<<"Enter Length of CA"<<endl;
cin>>length;
long long eca;
cout<<"Enter the eca rule in decimal : "<<endl;
cin>>eca;
string rule=toBase2(eca,32);
cout<<"The eca rule in binary is : "<<rule<<endl;

string conf;
cout<<"Enter the initial configuration of entered length"<<endl;
cin>>conf;
for(int i=1;i<=10;i++){
    string x=NextState(rule,conf,length);
    cout<<"The "<<i<<"th nextState is "<<x<<endl<<endl;
    conf=x;
}
return 0;
}
