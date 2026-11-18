// Complete integer pricing on maximal-only degree-conditioned vertex28 histograms.
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <charconv>
#include <stdexcept>
#include <limits>
using namespace std;
using Big=__int128_t;
string number(Big x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;string s;
 while(x){s+=char('0'+x%10);x/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
int choose2(int x){return x*(x-1)/2;}
int main(int argc,char**argv){
 try {
 if(argc>2)throw runtime_error("expected zero or one query path");
 array<array<int64_t,9>,9> Q{};array<int64_t,9> bias{};
 if(argc>1){ifstream in(argv[1]);if(!in)throw runtime_error("cannot open query");
  auto read=[&](int64_t &v){string token;if(!(in>>token))throw runtime_error("expected 90 int64 tokens");
   auto end=token.data()+token.size();auto result=from_chars(token.data(),end,v);
   if(result.ec!=errc()||result.ptr!=end)throw runtime_error("invalid or out-of-range int64 token");};
  for(auto &row:Q){for(auto &v:row)read(v);}
  for(auto &v:bias)read(v);
  string extra;if(in>>extra)throw runtime_error("extra trailing token");}
 for(int i=0;i<9;i++)for(int j=0;j<9;j++)if(Q[i][j]!=Q[j][i])throw runtime_error("query must be symmetric");
 const array<vector<int>,3> groups={vector<int>{0,3,7},vector<int>{1,4,5,8},vector<int>{2,6}};
 const array<int,9> expected={0,253,22848,75504,89180,50050,13728,1848,29};
 array<int,9> x{};int total_count=0;Big global_best=Big(1)<<126;int global_degree=-1;
 cout<<"{\"scope\":\"Complete MAXIMAL-ONLY necessary histogram domain; no graph realization or density certificate\",\"degrees\":[";
 cout<<"{\"degree\":0,\"count\":0,\"minimum\":null,\"witness\":null}";
 for(int degree=1;degree<=8;degree++){
  array<int,3> sums={choose2(8-degree),(degree-1)*(8-degree),choose2(degree)};
  int count=0;Big best=Big(1)<<126;array<int,9> witness{};
  auto visit=[&](){x[8]+=8-degree;count++;Big score=bias[degree];
   for(int i=0;i<9;i++){score+=Big(Q[i][i])*x[i]*x[i];
    for(int j=i+1;j<9;j++)score+=2*Big(Q[i][j])*x[i]*x[j];}
   if(score<best){best=score;witness=x;}x[8]-=8-degree;};
  function<void(int,int,int)> assign=[&](int group,int position,int remaining){
   if(position==int(groups[group].size())-1){x[groups[group][position]]=remaining;
    if(group==2)visit();else assign(group+1,0,sums[group+1]);return;}
   for(int value=0;value<=remaining;value++){x[groups[group][position]]=value;assign(group,position+1,remaining-value);}
  };
  assign(0,0,sums[0]);if(count!=expected[degree])throw runtime_error("domain count mismatch");total_count+=count;
  if(best<global_best){global_best=best;global_degree=degree;}
  cout<<",";cout<<"{\"degree\":"<<degree<<",\"count\":"<<count<<",\"minimum\":\""<<number(best)<<"\",\"witness\":[";
  for(int i=0;i<9;i++){if(i)cout<<",";cout<<witness[i];}cout<<"]}";
 }
 if(total_count!=253440)throw runtime_error("total domain count mismatch");
 cout<<"],\"total\":"<<total_count<<",\"minimum\":\""<<number(global_best)<<"\",\"minimizing_degree\":"<<global_degree<<"}\n";
 }catch(const exception &e){cerr<<e.what()<<"\n";return 2;}
}
