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
thread_local unordered_map<U,Canon> cube;
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
vector<Graph> raw;
void ingest(const Rec&r){
 Graph g(r); Code best{UINT32_MAX,UINT32_MAX,UINT32_MAX};
 for(auto f:g.faces){
  const auto& c=canon(f.base);
  for(int j:c.send)best=min(best,Code{c.base,acts[j].verts(f.vertical),acts[j].edges(f.opp)});
 }
 auto[it,inserted]=unique_graph.emplace(best,raw.size());
 if(!inserted){assert(raw[it->second].score==r.score);return;}
 raw.push_back(g);
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

// Each bit of a three-word vector is one of the 192 edges of Q6.
struct Bits {
 array<uint64_t,3> word{};
 void set(int k){word[k/64]|=uint64_t(1)<<(k%64);}
};
struct Placement{Bits present;L score;};
vector<Bits> facet_mask(12);
int rank5(int axis,int v){return axis*32+drop(v,axis);}
void six_faces(){
 for(int f=0;f<12;f++){
  int d=f/2;for(int x=0;x<64;x++)if((x>>d&1)==(f&1)){
   for(int e=0;e<6;e++)if(e!=d&&!(x>>e&1))facet_mask[f].set(rank5(e,x));
  }
  int total=0;for(auto v:facet_mask[f].word)total+=popcount(v);assert(total==80);
 }
}
// The two fixed coordinates specify a four-cube.  A candidate five-cube
// extends it by one coordinate. Install all its edges in global coordinates.
Placement place_raw(int fixed,int root,int side,U base,U vertical,U opp,L score){
 Placement ans{};ans.score=score;int fixed_axis=fixed/2;
 array<int,4> axes{};int k=0;for(int j=0;j<6;j++)if(j!=fixed_axis&&j!=root)axes[k++]=j;
 for(int v=0;v<16;v++){
  int x=((fixed&1)<<fixed_axis)|(side<<root);for(int a=0;a<4;a++)x|=(v>>a&1)<<axes[a];
  if(vertical>>v&1)ans.present.set(rank5(root,x));
  for(int a=0;a<4;a++)if(!(v>>a&1)){
   int e=edgebit(a,v,4);
   if(base>>e&1)ans.present.set(rank5(axes[a],x));
   if(opp>>e&1)ans.present.set(rank5(axes[a],x^(1<<root)));
  }
 }
 return ans;
}

struct Embed{
 array<array<Bits,256>,10> table{};
 Embed(int face,int axis,int side){
  for(int i=0;i<10;i++){
   array<Bits,8> one{};
   for(int b=0;b<8;b++){
    int k=8*i+b;U base=0,vertical=0,opp=0;
    if(k<32)base=U(1)<<k;else if(k<48)vertical=U(1)<<(k-32);else opp=U(1)<<(k-48);
    one[b]=place_raw(face,axis,side,base,vertical,opp,0).present;
   }
   for(int byte=1;byte<256;byte++){
    table[i][byte]=table[i][byte&(byte-1)];
    for(int j=0;j<3;j++)table[i][byte].word[j]|=one[countr_zero((U)byte)].word[j];
   }
  }
 }
 Placement place(U base,U vertical,U opp,L score)const{
  Placement p{};p.score=score;
  for(int i=0;i<10;i++){
   int byte=i<4?(base>>(8*i))&255:(i<6?(vertical>>(8*(i-4)))&255:(opp>>(8*(i-6)))&255);
   for(int j=0;j<3;j++)p.present.word[j]|=table[i][byte].word[j];
  }return p;
 }
};
thread_local map<tuple<int,int,int>,Embed> embeds;
vector<Placement> extensions(int face,int axis,int side,U base,L maxscore){
 vector<Placement> a;const auto& c=canon(base);auto it=options.find(c.base);if(it==options.end())return a;
 const auto &undo=acts[acts[c.send.front()].inv];auto &em=embeds.try_emplace({face,axis,side},face,axis,side).first->second;
 for(auto &[key,val]:it->second)if(val.first<=maxscore)
  a.push_back(em.place(base,undo.verts(key>>32),undo.edges(U(key)),val.first));
 sort(a.begin(),a.end(),[](const Placement&x,const Placement&y){return x.score>y.score;});
 return a;
}
struct Board {
 Bits mask,present;
 bool accepts(const Placement&p,int f)const{
  for(int k=0;k<3;k++)if((present.word[k]^p.present.word[k])&mask.word[k]&facet_mask[f].word[k])return false;
  return true;
 }
 Board filled(const Placement& p,int f)const{
  Board b=*this;for(int k=0;k<3;k++){b.present.word[k]|=p.present.word[k];b.mask.word[k]|=facet_mask[f].word[k];}return b;
 }
};
U upper_four(int f,const Placement&p){
 U mask=0;int d=f/2;
 for(int x=0;x<16;x++)for(int j=0;j<4;j++)if(!(x>>j&1)){
  int v=32+lift(x,d,f&1),q=rank5(j+(j>=d),v);
  uint64_t bit=(p.present.word[q/64]>>(q%64))&1;
  mask|=U(bit)<<edgebit(j,x,4);
 }
 return mask;
}
struct Checker {
 const Graph &g;L low;L &best;
 array<vector<Placement>,10> d;map<pair<int,U>,vector<Placement>> opposite;
 void solve(int mask,L sum,const Board &b,const vector<Placement>*up){
  L upmax=g.score;if(up){upmax=low;for(auto&p:*up)if(b.accepts(p,11)){upmax=p.score;break;}}
  L cap=sum+upmax;int take=-1;size_t smallest=SIZE_MAX;array<vector<int>,10> choices;
  for(int i=0;i<10;i++)if(mask>>i&1){
   auto &v=choices[i];for(int j=0;j<(int)d[i].size();j++)if(b.accepts(d[i][j],i))v.push_back(j);
   cap+=v.empty()?low:d[i][v.front()].score;if(v.size()<smallest){smallest=v.size();take=i;}
  }
  if(cap<=best)return;
  if(mask==0){best=cap;return;}
  int i=take,next=mask^(1<<i);auto &v=choices[i];L mx=v.empty()?low:d[i][v.front()].score;
  for(int j:v){
   auto &o=d[i][j];if(cap-mx+o.score<=best)break;
   const vector<Placement>*nextup=up;if(!up){
    U base=upper_four(i,o);auto[it,first]=opposite.try_emplace({i,base});
    if(first)it->second=extensions(11,i/2,i&1,base,g.score);
    nextup=&it->second;
   }
   solve(next,sum+o.score,b.filled(o,i),nextup);
  }
  if(cap-mx+low>best)solve(next,sum+low,b,up);
 }
 void run(){
  for(int i=0;i<10;i++)d[i]=extensions(i,5,0,g.faces[i].base,g.score);
  solve(1023,g.score,Board{},nullptr);
 }
};
U legacy(U b){
 U out=0;for(int d=0;d<4;d++)for(int x=0;x<16;x++)if(!(x>>d&1)){
  unsigned v=b>>edgebit(d,x,4)&1u;int k=d==0?(x>>1):(8+12*(1-(x&1))+edgebit(d-1,x>>1,3));out|=v<<k;
 }
 return out;
}

int main(int argc,char**argv){
 assert(argc==7);
 L cutoff=stoll(argv[2]),num=stoll(argv[4]),den=stoll(argv[5]),target=stoll(argv[6]);
 assert(0<num&&num<=den&&den>0);
 auto mix=[&](L first,L second){
  __int128 n=__int128(den-num)*first+__int128(num)*second;
  __int128 c=n/den+(n%den>0);assert(c>-(L(1)<<57)&&c<(L(1)<<57));return L(c);
 };
 ifstream input(argv[1],ios::binary);assert(input);geometry();six_faces();
 Rec r;int count=0;while(input.read((char*)&r,sizeof(r))){assert(r.score>=cutoff);ingest(r);++count;}
 assert(input.eof()&&input.gcount()==0);
 ifstream fp("full_masks.bin",ios::binary|ios::ate);assert(fp);vector<U> masks(fp.tellg()/4);fp.seekg(0);fp.read((char*)masks.data(),4*masks.size());assert(fp);
 ifstream fs(argv[3],ios::binary|ios::ate);assert(fs&&fs.tellg()==(streamoff)(8*masks.size()));
 vector<L> scores(masks.size());fs.seekg(0);fs.read((char*)scores.data(),8*scores.size());assert(fs);
 L low=mix(cutoff,10*(*max_element(scores.begin(),scores.end())));
 map<U,int> converted;
 for(int i=0;i<(int)raw.size();i++){
  Graph &g=raw[i];L total=0;
  for(auto&f:g.faces){
   U k=canon(f.base).base;auto[it,fresh]=converted.try_emplace(k,-1);if(fresh){
    U mn=UINT32_MAX;for(auto &ac:acts)mn=min(mn,legacy(ac.edges(k)));
    auto p=lower_bound(masks.begin(),masks.end(),mn);assert(p!=masks.end()&&*p==mn);it->second=p-masks.begin();
   }total+=scores[it->second];
  }
  g.score=mix(g.score,total);if(g.score>low)store_graph(g,i);
 }
 sort(graphs.begin(),graphs.end(),[](const Typed&a,const Typed&b){return a.g.score>b.g.score;});
 L best=max(12*low,target);int checks=0;
 const L start=best;int limit=0;while(limit<(int)graphs.size()&&12*graphs[limit].g.score>start)limit++;
 #pragma omp parallel for schedule(dynamic,1)
 for(int i=0;i<limit;i++){L local=start;Checker checker{graphs[i].g,low,local};checker.run();
  #pragma omp critical(check_6)
  {best=max(best,local);checks++;}
 }
 cout<<"six_upper "<<best<<" low "<<low<<" records "<<count<<" orbits "<<raw.size()<<" anchors "<<checks<<endl;
}
