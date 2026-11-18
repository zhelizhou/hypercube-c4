// Exhaust Q6 automorphic pairs; optimally stack them into Q7 using min-cut.
// This tests a Q7 weighted inequality. No Q8 input is read.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <vector>
using namespace std;
struct Dinic{
 struct E{int to,rev,cap;};vector<vector<E>>g;vector<int>level,ptr;
 Dinic(int n):g(n),level(n),ptr(n){}
 void add(int u,int v,int c){E a{v,int(g[v].size()),c},b{u,int(g[u].size()),0};g[u].push_back(a);g[v].push_back(b);}
 bool bfs(){fill(level.begin(),level.end(),-1);queue<int>q;q.push(64);level[64]=0;while(!q.empty()){int u=q.front();q.pop();for(auto e:g[u])if(e.cap&&level[e.to]<0){level[e.to]=level[u]+1;q.push(e.to);}}return level[65]>=0;}
 int dfs(int u,int f){if(u==65)return f;for(int &i=ptr[u];i<int(g[u].size());i++){auto &e=g[u][i];if(e.cap&&level[e.to]==level[u]+1){int t=dfs(e.to,min(f,e.cap));if(t){e.cap-=t;g[e.to][e.rev].cap+=t;return t;}}}return 0;}
 int flow(){int f=0;while(bfs()){fill(ptr.begin(),ptr.end(),0);while(int t=dfs(64,10000))f+=t;}return f;}
 vector<int> reach(){vector<int>r(66);queue<int>q;q.push(64);r[64]=1;while(!q.empty()){int u=q.front();q.pop();for(auto e:g[u])if(e.cap&&!r[e.to]){r[e.to]=1;q.push(e.to);}}return r;}
};
int main(int argc,char**argv){
 if(argc!=3)return 2;
 vector<array<int,2>>es;int id[64][64];fill(&id[0][0],&id[0][0]+4096,-1);
 for(int u=0;u<64;u++)for(int i=0;i<6;i++)if(!(u>>i&1)){int v=u^(1<<i);id[u][v]=id[v][u]=es.size();es.push_back({u,v});}
 array<int,192>base{};array<int,64>d0{};ifstream in(argv[1]);int m0=0;
 for(int e=0;e<192;e++){in>>base[e];if(base[e]){m0++;for(int v:es[e])d0[v]++;}}
 if(m0<=0)return 3;
 int basehigh=0;for(int v=0;v<64;v++)basehigh+=d0[v]>=6;
 array<int,6>p={0,1,2,3,4,5},bestp=p;int bestt=0,best=0,total=0;vector<int>bestS;array<int,192>bestg{};
 do{
  array<int,64>pm{};for(int v=0;v<64;v++)for(int i=0;i<6;i++)if(v>>i&1)pm[v]|=1<<p[i];
  for(int t=0;t<64;t++){
   array<int,192>other{};array<int,64>d1{};
   for(int e=0;e<192;e++)if(base[e]){int u=pm[es[e][0]]^t,v=pm[es[e][1]]^t;other[id[u][v]]=1;d1[u]++;d1[v]++;}
   Dinic cut(66);int weight=0;
   for(int v=0;v<64;v++){int w=2+(d0[v]==5)+(d1[v]==5);weight+=w;if(__builtin_popcount(unsigned(v))%2==0)cut.add(64,v,w);else cut.add(v,65,w);}
   for(int e=0;e<192;e++)if(base[e]&&other[e]){int u=es[e][0],v=es[e][1];if(__builtin_popcount(unsigned(u))%2)swap(u,v);cut.add(u,v,1000);}
   int score=4*m0+2*basehigh+weight-cut.flow();total++;
   if(score>best){best=score;bestp=p;bestt=t;bestg=other;auto r=cut.reach();bestS.clear();for(int v=0;v<64;v++)if((__builtin_popcount(unsigned(v))%2==0&&r[v])||(__builtin_popcount(unsigned(v))%2==1&&!r[v]))bestS.push_back(v);cerr<<"checked="<<total<<" best="<<best<<'\n';}
   if(best>608)break;
  }
  if(best>608)break;
 }while(next_permutation(p.begin(),p.end()));
 ofstream out(argv[2]);out<<"{\"automorphisms_checked\":"<<total<<",\"best_weighted\":"<<best<<",\"counterexample\":"<<(best>608?"true":"false")<<",\"translation\":"<<bestt<<",\"permutation\":[";
 for(int i=0;i<6;i++){if(i)out<<',';out<<bestp[i];}out<<"],\"edges\":[";bool first=true;
 auto emit=[&](int u,int v){if(!first)out<<',';first=false;out<<'['<<u<<','<<v<<']';};
 for(int e=0;e<192;e++){if(base[e])emit(es[e][0],es[e][1]);if(bestg[e])emit(es[e][0]+64,es[e][1]+64);}for(int v:bestS)emit(v,v+64);out<<"]}\n";
 cerr<<"finished checked="<<total<<" best="<<best<<'\n';
}
