// Counterexample search for 2m+#{d>=6}<=608 on C4-free Q7.
#include <array>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>
using namespace std;
int main(int argc,char**argv){
 if(argc!=7)return 2;
 int lo=stoi(argv[3]),hi=stoi(argv[4]);double seconds=stod(argv[5]);
 mt19937_64 rng(stoull(argv[6]));
 vector<array<int,2>> edge;array<array<int,7>,128> id{};
 for(int u=0;u<128;u++)for(int i=0;i<7;i++)if(!(u>>i&1)){
  int v=u^(1<<i);id[u][i]=id[v][i]=edge.size();edge.push_back({u,v});
 }
 vector<array<int,4>> sq;array<vector<int>,448> inc;
 for(int i=0;i<7;i++)for(int j=i+1;j<7;j++)for(int u=0;u<128;u++)if(!(u&((1<<i)|(1<<j)))){
  array<int,4>s={id[u][i],id[u][j],id[u^(1<<i)][j],id[u^(1<<j)][i]};
  for(int e:s)inc[e].push_back(sq.size());sq.push_back(s);
 }
 array<int,448> seed{},x{},bestx{};ifstream in(argv[1]);for(int &v:seed)if(!(in>>v))return 3;
 array<int,128>d{};vector<int>cnt(sq.size());
 auto pen=[&](int k){return max(0,lo-k)+max(0,k-hi);};
 auto rnd=[&](){return double(rng()>>11)*0x1.0p-53;};
 auto start=chrono::steady_clock::now();long long steps=0,restarts=0;int best=608;
 bool found=false;
 while(chrono::duration<double>(chrono::steady_clock::now()-start).count()<seconds&&!found){
  x=seed;d.fill(0);int m=0,bad=0,high=0,invalid=0;
  for(int e=0;e<448;e++)if(x[e]){m++;for(int v:edge[e])d[v]++;}
  for(int v=0;v<128;v++){high+=d[v]>=6;invalid+=pen(d[v]);}
  for(int s=0;s<int(sq.size());s++){cnt[s]=0;for(int e:sq[s])cnt[s]+=x[e];bad+=cnt[s]==4;}
  restarts++;
  for(int it=0;it<2000000;it++,steps++){
   if(bad==0&&invalid==0&&2*m+high>best){best=2*m+high;bestx=x;cerr<<"best="<<best<<" m="<<m<<" high="<<high<<'\n';found=true;break;}
   int e=rng()%448,delta=x[e]?-1:1,u=edge[e][0],v=edge[e][1];
   int dh=(d[u]+delta>=6)+(d[v]+delta>=6)-(d[u]>=6)-(d[v]>=6);
   int dp=pen(d[u]+delta)+pen(d[v]+delta)-pen(d[u])-pen(d[v]);
   int db=0;for(int s:inc[e])db+=(cnt[s]+delta==4)-(cnt[s]==4);
   double gain=2*delta+dh-3.0*db-4.0*dp;
   double T=1.2*pow(.01/1.2,double(it)/2000000);
   if(gain>=0||rnd()<exp(gain/T)){
    x[e]+=delta;d[u]+=delta;d[v]+=delta;m+=delta;bad+=db;high+=dh;invalid+=dp;for(int s:inc[e])cnt[s]+=delta;
   }
   if((it&65535)==0&&chrono::duration<double>(chrono::steady_clock::now()-start).count()>=seconds)break;
  }
 }
 ofstream out(argv[2]);out<<"{\"found\":"<<(found?"true":"false")<<",\"best_weighted\":"<<best<<",\"steps\":"<<steps<<",\"restarts\":"<<restarts<<",\"edges\":[";
 if(found){bool first=true;for(int e=0;e<448;e++)if(bestx[e]){if(!first)out<<',';first=false;out<<'['<<edge[e][0]<<','<<edge[e][1]<<']';}}
 out<<"]}\n";cerr<<"finished best="<<best<<" steps="<<steps<<'\n';
}
