// Independent plain full-scan RUP replay. No cached assignments, watches,
// deletion handling or history fallback. All checked consequences are retained.
#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
using Clause=vector<int>;
static bool parse_clause(const string &s,int n,Clause &c){
 istringstream in(s);long long x;bool end=false;
 while(in>>x){if(end)return false;if(x==0){end=true;continue;}if(x>n||x< -n)return false;c.push_back(int(x));}
 if(!in.eof()||!end)return false;
 sort(c.begin(),c.end());c.erase(unique(c.begin(),c.end()),c.end());return true;
}
static bool rup(const vector<Clause>&db,const Clause&candidate,int n){
 vector<int>value(n+1);
 for(int lit:candidate){int v=abs(lit),sign=lit>0?-1:1;if(value[v]&&value[v]!=sign)return true;value[v]=sign;}
 bool changed=true;
 while(changed){changed=false;
  for(const Clause &c:db){bool satisfied=false;int open=0,unit=0;
   for(int lit:c){int x=value[abs(lit)]*(lit>0?1:-1);if(x>0){satisfied=true;break;}if(x==0){open++;unit=lit;}}
   if(satisfied)continue;
   if(open==0)return true;
   if(open==1){value[abs(unit)]=unit>0?1:-1;changed=true;}
  }
 }return false;
}
int main(int argc,char**argv){
 if(argc!=3)return 2;ifstream input(argv[1]),proof(argv[2]);if(!input||!proof)return 3;
 int n=0,expected=0;vector<Clause>db;string line;
 while(getline(input,line)){if(line.empty()||line[0]=='c')continue;
  if(line[0]=='p'){istringstream s(line);string p,cnf,extra;if(n||!(s>>p>>cnf>>n>>expected)||p!="p"||cnf!="cnf"||n<=0||expected<0||(s>>extra))return 4;continue;}
  Clause c;if(!n||!parse_clause(line,n,c))return 5;db.push_back(c);
 }
 if(int(db.size())!=expected)return 6;
 long long add=0,del=0,number=0;
 while(getline(proof,line)){number++;if(line.empty()||line[0]=='c')continue;
  bool deletion=line[0]=='d';Clause c;if(!parse_clause(deletion?line.substr(1):line,n,c))return 7;
  if(deletion){del++;continue;}
  if(!rup(db,c,n)){cerr<<"NOT_RUP line="<<number<<" addition="<<add+1<<"\n";return 1;}
  add++;if(c.empty()){cout<<"{\"valid\":true,\"final_empty_clause\":true,\"verified_additions\":"<<add<<",\"deletions_ignored\":"<<del<<"}\n";return 0;}
  db.push_back(c);
 }
 cout<<"{\"valid\":false,\"final_empty_clause\":false,\"verified_additions\":"<<add<<"}\n";return 10;
}
