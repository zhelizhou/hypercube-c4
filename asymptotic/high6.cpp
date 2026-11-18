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
struct Projection{U edge[4][256]{},vert[2][256]{};
 U signature(U e,U v)const{return edge[0][e&255]|edge[1][e>>8&255]|edge[2][e>>16&255]|edge[3][e>>24]|vert[0][v&255]|vert[1][v>>8];}
};
array<Projection,8> sub;
void maps3(){
 for(int d=0;d<4;d++)for(int t=0;t<2;t++){
  auto &p=sub[2*d+t];
  for(int x=0;x<16;x++)if((x>>d&1)==t){
   int v=drop(x,d);for(int i=0;i<256;i++)if(i>>(x%8)&1)p.vert[x/8][i]|=1u<<(12+v);
   for(int j=0;j<4;j++)if(j!=d&&!(x>>j&1)){
    int k=edgebit(j,x,4), q=edgebit(j-(j>d),v,3);
    for(int i=0;i<256;i++)if(i>>(k%8)&1)p.edge[k/8][i]|=1u<<q;
   }
  }
 }
}
struct Option {U v,o;L score;int id;array<U,10> sig;};
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
array<vector<Option>,10> domains(const Graph&g){
 array<vector<Option>,10> a;
 for(int i=0;i<10;i++){
  auto &c=canon(g.faces[i].base);auto &act=acts[acts[c.send.front()].inv];
  for(auto [key,val]:options.at(c.base))if(val.first<=g.score){L sc=val.first;
   Option h{act.verts(key>>32),act.edges(U(key)),sc,val.second,{}};
   for(int j=0;j<10;j++)if(j/2!=i/2){
    int axis=j/2-(j/2>i/2);h.sig[j]=sub[2*axis+(j&1)].signature(h.o,h.v);
   }
   a[i].push_back(h);
  }
  sort(a[i].begin(),a[i].end(),[](const Option&a,const Option&b){return a.score>b.score;});
 }
 return a;
}
L pair_bound(const Graph&g,const array<vector<Option>,10>& a,L low){
 array<array<L,10>,10> pair{};
 for(int i=0;i<10;i++)for(int j=i+1;j<10;j++){
  L si=a[i].empty()?low:a[i].front().score,sj=a[j].empty()?low:a[j].front().score;
  if(i/2==j/2){pair[i][j]=si+sj;continue;}
  L val=max(si,sj)+low;unordered_map<U,L> d;
  for(auto &o:a[i])d.emplace(o.sig[j],o.score);
  for(auto &o:a[j]){
   if(o.score+si<=val)break;
   auto it=d.find(o.sig[i]);if(it!=d.end())val=max(val,it->second+o.score);
  }
  pair[i][j]=val;
 }
 array<L,1024> dp{};for(int m=1;m<1024;m++)if(popcount((U)m)%2==0){
  int i=countr_zero((U)m);L opt=INT64_MAX;
  for(int j=i+1;j<10;j++)if(m&(1<<j))opt=min(opt,pair[i][j]+dp[m^(1<<i)^(1<<j)]);
  dp[m]=opt;
 }
 return 2*g.score+dp.back();
}

struct Other {array<U,10> faces{};L score;int id;};
vector<Other> other_options(int fac,U base,L ceiling){
 int d=fac/2,t=fac&1;const auto &c=canon(base);
 const auto& act=acts[acts[c.send.front()].inv];
 vector<Other> all;auto it=options.find(c.base);if(it==options.end())return all;
 for(const auto &[key,val]:it->second)if(val.first<=ceiling){L score=val.first;
  U vertical=act.verts(key>>32),opp=act.edges(U(key));Other g{};g.score=score;g.id=val.second;
  g.faces[fac]=base;g.faces[fac^1]=opp;
  for(int j=0;j<10;j++)if(j/2!=d){
   int q=j/2;U f=0;
   for(int k=0;k<4;k++)for(int v=0;v<16;v++)if(!(v>>k&1)){
    int e=k+(k>=q),x=lift(v,q,j&1),z=drop(x,d);unsigned bit;
    if(e==d)bit=vertical>>z&1u;
    else bit=(((x>>d&1)==t)?base:opp)>>edgebit(e-(e>d),z,4)&1u;
    f|=bit<<edgebit(k,v,4);
   }
   g.faces[j]=f;
  }
  all.push_back(g);
 }
 sort(all.begin(),all.end(),[](const Other&a,const Other&b){return a.score>b.score;});
 return all;
}

using Mask=array<uint64_t,3>;
int bit6(int dir,int x){return dir*32+drop(x,dir);}
struct Full {Mask bits{},used{};
 void set(int k,unsigned val){uint64_t b=uint64_t(1)<<(k%64);int j=k/64;
  if(used[j]&b)assert(((bits[j]&b)!=0)==bool(val));used[j]|=b;if(val)bits[j]|=b;
 }
 int get(int d,int x)const{int k=bit6(d,x);return bits[k/64]>>(k%64)&1;}
};
ofstream hout;map<Mask,L> emitted;L totalleaves=0;
void output_graph(const Graph&g,const array<vector<Option>,10>&a,const array<int,10>&choice,const Other*opp,L score,L low){
 Full f;int count=1;
 for(int v=0;v<32;v++)for(int k=0;k<5;k++)if(!(v>>k&1))f.set(bit6(k,v),g.a[v][k]);
 for(int i=0;i<10;i++)if(choice[i]>=0){
  count++;const Option&o=a[i][choice[i]];int d=i/2;
  for(int v=0;v<16;v++){
   int x=lift(v,d,i&1);f.set(bit6(5,x),o.v>>v&1);
   for(int k=0;k<4;k++)if(!(v>>k&1))f.set(bit6(k+(k>=d),x+32),o.o>>edgebit(k,v,4)&1);
  }
 }
 if(opp){count++;for(int i=0;i<10;i++)for(int v=0;v<16;v++)for(int k=0;k<4;k++)if(!(v>>k&1))
  f.set(bit6(k+(k>=i/2),32+lift(v,i/2,i&1)),opp->faces[i]>>edgebit(k,v,4)&1);}
 assert(count>=8);
 for(auto x:f.used)assert(x==UINT64_MAX);
 #pragma omp atomic update
 ++totalleaves;
 bool known;
 #pragma omp critical(record_6)
 {known=emitted.contains(f.bits);}
 if(known)return;
 for(int d=0;d<6;d++)for(int e=0;e<d;e++)for(int x=0;x<64;x++)if(!(x&((1<<d)|(1<<e))))
  if(f.get(d,x)&&f.get(e,x)&&f.get(d,x^(1<<e))&&f.get(e,x^(1<<d)))return;
 L true_sum=0;
 for(int t=0;t<12;t++){
  int fixed=t/2;array<int,5> ax{};int z=0;for(int d=0;d<6;d++)if(d!=fixed)ax[z++]=d;
  U base=0,vv=0,other=0;
  for(int v=0;v<16;v++){
   int x=(t&1)<<fixed;for(int j=0;j<4;j++)x|=((v>>j)&1)<<ax[j];
   vv|=U(f.get(ax[4],x))<<v;
   for(int j=0;j<4;j++)if(!(v>>j&1)){
    int b=edgebit(j,v,4);base|=U(f.get(ax[j],x))<<b;other|=U(f.get(ax[j],x^(1<<ax[4])))<<b;
   }
  }
  const auto &c=canon(base);auto it=options.find(c.base);L val=low;
  if(it!=options.end()){auto &act=acts[c.send.front()];auto jt=it->second.find((uint64_t(act.verts(vv))<<32)|act.edges(other));if(jt!=it->second.end())val=jt->second.first;}
  true_sum+=val;
 }
 assert(true_sum>=score);
 #pragma omp critical(record_6)
 {
  auto[it,first]=emitted.emplace(f.bits,true_sum);assert(it->second==true_sum);
  if(first){hout.write((char*)&true_sum,8);hout.write((char*)f.bits.data(),24);}
 }
}
using Live=array<vector<int>,10>;
struct Solver{
 const Graph& g;const array<vector<Option>,10>& a;L low,best;int64_t nodes=0;array<int,10> choice{},saved{};int opposite=-1;
 struct Key{int fac;U base;auto operator<=>(const Key&)const=default;};
 map<Key,vector<Other>> cache;
 void search(int mask,L sum,const Live &d,const vector<Other>*other,const vector<int>&live){
  nodes++;
  L oc=other?(live.empty()?low:(*other)[live[0]].score):g.score;
  L cap=sum+oc;int take=-1;size_t smallest=SIZE_MAX;
  for(int i=0;i<10;i++)if(mask>>i&1){
   cap+=d[i].empty()?low:a[i][d[i].front()].score;
   if(d[i].size()<smallest){take=i;smallest=d[i].size();}
  }
  if(cap<=best)return;
  if(!mask){
   assert(other);for(int h:live){L sc=sum+(*other)[h].score;if(sc<=best)break;output_graph(g,a,choice,&(*other)[h],sc,low);}
   if(sum+low>best)output_graph(g,a,choice,nullptr,sum+low,low);
   return;
  }
  int i=take;L mx=d[i].empty()?low:a[i][d[i][0]].score;int next=mask^(1<<i);
  for(int k:d[i]){
   const auto& opt=a[i][k];if(cap-mx+opt.score<=best)break;
   Live nd;L bound=sum+opt.score+oc;
   for(int j=0;j<10;j++)if(next>>j&1){
    if(i/2==j/2)nd[j]=d[j];else{
      for(int h:d[j])if(a[j][h].sig[i]==opt.sig[j])nd[j].push_back(h);
    }
    bound+=nd[j].empty()?low:a[j][nd[j].front()].score;
   }
   if(bound<=best)continue;
   const vector<Other>*no=other; vector<int> nl;
   if(!other){
    auto[it,fresh]=cache.try_emplace({i,opt.o});if(fresh)it->second=other_options(i,opt.o,g.score);
    no=&it->second;nl.resize(no->size());iota(nl.begin(),nl.end(),0);
   }else for(int h:live)if((*other)[h].faces[i]==opt.o)nl.push_back(h);
   choice[i]=k;search(next,sum+opt.score,nd,no,nl);
  }
  choice[i]=-1;if(cap-mx+low>best)search(next,sum+low,d,other,live);
 }
 L solve(){
  Live d{};for(int i=0;i<10;i++){d[i].resize(a[i].size());iota(d[i].begin(),d[i].end(),0);}
  search(1023,g.score,d,nullptr,{});return best;
 }
};

U legacy(U b){
 U out=0;for(int d=0;d<4;d++)for(int x=0;x<16;x++)if(!(x>>d&1)){
  unsigned v=b>>edgebit(d,x,4)&1u;int k=d==0?(x>>1):(8+12*(1-(x&1))+edgebit(d-1,x>>1,3));out|=v<<k;
 }
 return out;
}
void features(const vector<int>&idx){
 ifstream p("full_masks.bin",ios::binary|ios::ate);assert(p);vector<U> m(p.tellg()/4);p.seekg(0);p.read((char*)m.data(),m.size()*4);
 ofstream out("six_five.dat",ios::binary);map<U,int> cv;
 for(int i:idx){
  auto &g=raw[i];out.write((char*)&g.score,8);array<int,10> f;
  for(int j=0;j<10;j++){
   U k=canon(g.faces[j].base).base;auto[it,fresh]=cv.try_emplace(k,-1);if(fresh){
    U mn=UINT32_MAX;for(auto &ac:acts)mn=min(mn,legacy(ac.edges(k)));auto pos=lower_bound(m.begin(),m.end(),mn);
    assert(pos!=m.end()&&*pos==mn);it->second=pos-m.begin();
   }f[j]=it->second;
  }out.write((char*)f.data(),40);
 }assert(out);
}

int main(int argc,char**argv){
 assert(argc==5);L low=stoll(argv[2]),floor=stoll(argv[3]);ifstream in(argv[1],ios::binary);assert(in);
 geometry();maps3();Rec r;while(in.read((char*)&r,sizeof(r))){assert(r.score>=low);ingest(r);}assert(in.eof()&&in.gcount()==0);
 for(int i=0;i<(int)raw.size();i++)if(raw[i].score>low)store_graph(raw[i],i);
 sort(graphs.begin(),graphs.end(),[](const Typed&a,const Typed&b){return a.g.score>b.g.score;});
 assert(!graphs.empty()&&7*graphs[0].g.score+5*low<floor);
 hout.open(argv[4],ios::binary);assert(hout);int anchors=0;
 int limit=0;while(limit<(int)graphs.size()&&12*graphs[limit].g.score>=floor)limit++;
 #pragma omp parallel for schedule(dynamic,1)
 for(int ix=0;ix<limit;ix++){auto &g=graphs[ix].g;
  auto a=domains(g);if(pair_bound(g,a,low)>=floor){Solver sol{g,a,low,floor-1};sol.solve();}
  #pragma omp critical(record_6)
  {if(++anchors%500==0)cerr<<"anchors "<<anchors<<" records "<<emitted.size()<<endl;}
 }
 assert(hout);cout<<"anchors "<<anchors<<" records "<<emitted.size()<<" leaves "<<totalleaves<<endl;
}
