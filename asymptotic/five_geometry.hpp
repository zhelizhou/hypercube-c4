#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <tuple>
#include <unordered_map>
#include <vector>
using namespace std;
using U=uint32_t;
using L=int64_t;
using Code=tuple<U,U,U>;
struct Rec {L score;array<uint16_t,8> masks;};
static_assert(sizeof(Rec)==24);
int drop(int v,int d){return (v&((1<<d)-1))|((v>>(d+1))<<d);}
int lift(int v,int d,int t){return (v&((1<<d)-1))|((v>>d)<<(d+1))|(t<<d);}
int edgebit(int d,int x,int n){return (d<<(n-1))+drop(x,d);}
struct Four {U base,vertical,opp;};
struct Graph { unsigned char a[32][5]{};array<Four,10> faces{}; L score;
 explicit Graph(const Rec&r):score(r.score){
  for(int i=0;i<32;i++)for(int d=0;d<5;d++){
    const int fiber=i&3, v=i>>2;
    if(d>=2)a[i][d]=r.masks[fiber]>>edgebit(d-2,v,3)&1;
    else {int part=d==0?((fiber&2)?7:4):((fiber&1)?6:5);a[i][d]=r.masks[part]>>v&1;}
  }
  for(int d=0;d<5;d++)for(int t=0;t<2;t++){
   auto &f=faces[2*d+t];
   for(int v=0;v<16;v++){
    int x=lift(v,d,t);f.vertical|=U(a[x][d])<<v;
    for(int j=0;j<4;j++)if(!(v>>j&1)){
     int e=j+(j>=d), k=edgebit(j,v,4);
     f.base|=U(a[x][e])<<k;f.opp|=U(a[x^(1<<d)][e])<<k;
    }
   }
  }
 }
};
struct Action{U e[4][256]{},v[2][256]{};int inv;
 U edges(U x)const{return e[0][x&255]|e[1][x>>8&255]|e[2][x>>16&255]|e[3][x>>24];}
 U verts(U x)const{return v[0][x&255]|v[1][x>>8];}
};
vector<Action> acts;
struct Canon{U base;vector<int> send;};
unordered_map<U,Canon> cube;
void geometry(){
 array<int,4> p{0,1,2,3};map<array<int,16>,int> lookup;vector<array<int,16>> vv;
 do{for(int t=0;t<16;t++){
   Action g{};array<int,16> f;for(int v=0;v<16;v++){int y=t;for(int j=0;j<4;j++)y^=((v>>j)&1)<<p[j];f[v]=y;}
   for(int k=0;k<16;k++)for(int i=0;i<256;i++)if(i>>(k%8)&1)g.v[k/8][i]|=1u<<f[k];
   for(int d=0;d<4;d++)for(int x=0;x<16;x++)if(!(x>>d&1)){
    int k=edgebit(d,x,4),q=edgebit(p[d],f[x],4);
    for(int i=0;i<256;i++)if(i>>(k%8)&1)g.e[k/8][i]|=1u<<q;
   }
   lookup[f]=acts.size();acts.push_back(g);vv.push_back(f);
 }}while(next_permutation(p.begin(),p.end()));
 for(int i=0;i<384;i++){array<int,16> v;for(int j=0;j<16;j++)v[vv[i][j]]=j;acts[i].inv=lookup.at(v);}
}
const Canon& canon(U u){
 auto it=cube.find(u);if(it!=cube.end())return it->second;
 Canon r{UINT32_MAX,{}};
 for(int j=0;j<384;j++){U b=acts[j].edges(u);if(b<r.base){r.base=b;r.send.clear();}if(b==r.base)r.send.push_back(j);}
 return cube.emplace(u,move(r)).first->second;
}
using Value=pair<L,int>;using Dict=unordered_map<uint64_t,Value>;
unordered_map<U,Dict> options;
struct Typed {Graph g;int index;};
vector<Typed> graphs;
map<Code,int> unique_graph;
vector<Graph> raw;vector<Code> codes;
void ingest(const Rec&r){
 Graph g(r); Code best{UINT32_MAX,UINT32_MAX,UINT32_MAX};
 for(auto f:g.faces){
  const auto& c=canon(f.base);
  for(int j:c.send)best=min(best,Code{c.base,acts[j].verts(f.vertical),acts[j].edges(f.opp)});
 }
 auto[it,inserted]=unique_graph.emplace(best,raw.size());
 if(!inserted){assert(raw[it->second].score==r.score);return;}
 raw.push_back(g);codes.push_back(best);
}
void store_graph(const Graph&g,int id){
 graphs.push_back({g,id});
 for(auto f:g.faces){
  const auto& c=canon(f.base);auto &dict=options[c.base];
  for(int j:c.send){
   auto &a=acts[j];uint64_t k=(uint64_t(a.verts(f.vertical))<<32)|a.edges(f.opp);
   auto [it,first]=dict.emplace(k,Value{g.score,id});assert(first||it->second==Value(g.score,id));
  }
 }
}
