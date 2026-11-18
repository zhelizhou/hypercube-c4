#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <tuple>
#include <vector>
using namespace std;
using Wide=__uint128_t;using U=uint32_t;using L=int64_t;
using Six=array<uint64_t,3>;using Seven=array<uint64_t,7>;
int drop(int x,int d){return (x&((1<<d)-1))|((x>>(d+1))<<d);}
int lift(int x,int d,int t){return (x&((1<<d)-1))|((x>>d)<<(d+1))|(t<<d);}
int edge(int n,int d,int x){return (d<<(n-1))+drop(x,d);}
template<size_t N>int bit(const array<uint64_t,N>&a,int i){return (a[i/64]>>(i%64))&1;}
template<size_t N>void put(array<uint64_t,N>&a,int i){a[i/64]|=uint64_t(1)<<(i%64);}
struct Local{Wide base,opp;U match;};
struct Graph {Six bits;L score;array<Local,12> face{};
 Graph(Six b,L s):bits(b),score(s){
  for(int f=0;f<12;f++)for(int v=0;v<32;v++){
   int d=f/2,x=lift(v,d,f&1);auto &p=face[f];p.match|=U(bit(b,edge(6,d,x)))<<v;
   for(int j=0;j<5;j++)if(!(v>>j&1)){
    int k=edge(5,j,v),e=j+(j>=d);p.base|=Wide(bit(b,edge(6,e,x)))<<k;
    p.opp|=Wide(bit(b,edge(6,e,x^(1<<d))))<<k;
   }
  }
 }
};
struct Act{
 array<array<Wide,256>,10> edges{};array<array<U,256>,4> vertices{};int inv=0;
 Wide e(Wide x)const{Wide out=0;for(int j=0;j<10;j++){out|=edges[j][unsigned(x)&255];x>>=8;}return out;}
 U v(U x)const{return vertices[0][x&255]|vertices[1][x>>8&255]|vertices[2][x>>16&255]|vertices[3][x>>24];}
};
vector<Act> action;
array<Seven,14> masks{};
void init(){
 action.reserve(3840);map<array<int,32>,int> index;vector<array<int,32>> vs;array<int,5> perm{0,1,2,3,4};
 do{for(int sh=0;sh<32;sh++){
  action.emplace_back();Act&g=action.back();array<int,32> m;array<Wide,80> unit{};array<U,32> vu{};
  for(int i=0;i<32;i++){int y=sh;for(int j=0;j<5;j++)y^=(i>>j&1)<<perm[j];m[i]=y;vu[i]=U(1)<<y;}
  for(int i=0;i<32;i++)for(int j=0;j<5;j++)if(!(i>>j&1))unit[edge(5,j,i)]=Wide(1)<<edge(5,perm[j],m[i]);
  for(unsigned b=1;b<256;b++) {int bb=countr_zero(b);for(int j=0;j<10;j++)g.edges[j][b]=g.edges[j][b&(b-1)]|unit[8*j+bb];
   for(int j=0;j<4;j++)g.vertices[j][b]=g.vertices[j][b&(b-1)]|vu[8*j+bb];}
  index[m]=vs.size();vs.push_back(m);
 }}while(next_permutation(perm.begin(),perm.end()));
 for(int i=0;i<3840;i++){array<int,32> inv;for(int j=0;j<32;j++)inv[vs[i][j]]=j;action[i].inv=index.at(inv);}
 for(int f=0;f<14;f++)for(int x=0;x<128;x++)if((x>>(f/2)&1)==(f&1))
  for(int j=0;j<7;j++)if(j!=f/2&&!(x>>j&1))put(masks[f],edge(7,j,x));
}
struct Can{Wide key;vector<int> ids;};map<Wide,Can> cache;
const Can& canonical(Wide raw){
 auto[it,fresh]=cache.try_emplace(raw,Can{~Wide(0),{}});auto &c=it->second;
 if(fresh)for(int j=0;j<3840;j++){Wide v=action[j].e(raw);if(v<c.key){c.key=v;c.ids.clear();}if(v==c.key)c.ids.push_back(j);}
 return c;
}
using Key=tuple<Wide,U,Wide>;map<Key,int> types;
map<Wide,map<pair<U,Wide>,int>> options;vector<Graph> graphs;
void ingest(Six bits,L score){
 Graph g(bits,score);Key best{~Wide(0),~U(0),~Wide(0)};
 for(const auto &f:g.face){auto&c=canonical(f.base);for(int j:c.ids)best=min(best,Key{c.key,action[j].v(f.match),action[j].e(f.opp)});}
 auto[it,fresh]=types.emplace(best,graphs.size());if(!fresh){assert(graphs[it->second].score==score);return;}
 int id=it->second;graphs.push_back(g);
 for(auto f:g.face){const auto&c=canonical(f.base);auto &d=options[c.key];for(int j:c.ids){
  auto[entry,ins]=d.emplace(pair{action[j].v(f.match),action[j].e(f.opp)},id);assert(ins||entry->second==id);
 }}
}
struct Option{Seven bits{};int id;};
vector<Option> domain(int f,int root,int t,Wide base,L maxscore){
 vector<Option> out;auto &c=canonical(base);auto it=options.find(c.key);if(it==options.end())return out;
 auto &undo=action[action[c.ids.front()].inv];array<int,5> axis;int k=0;for(int j=0;j<7;j++)if(j!=f/2&&j!=root)axis[k++]=j;
 for(auto &[k,id]:it->second){if(graphs[id].score>maxscore)continue;
  U v=undo.v(k.first);Wide opp=undo.e(k.second);Option o{};o.id=id;
  for(int j=0;j<32;j++){
   int x=((f&1)<<(f/2))|(t<<root);for(int a=0;a<5;a++)x|=((j>>a)&1)<<axis[a];
   if(v>>j&1)put(o.bits,edge(7,root,x));
   for(int a=0;a<5;a++)if(!(j>>a&1)){
    int b=edge(5,a,j);if((base>>b)&1)put(o.bits,edge(7,axis[a],x));if((opp>>b)&1)put(o.bits,edge(7,axis[a],x^(1<<root)));
   }
  }out.push_back(o);
 }
 sort(out.begin(),out.end(),[](auto&a,auto&b){return graphs[a.id].score>graphs[b.id].score;});return out;
}
Wide upper(const Seven&b,int f){Wide s=0;for(int j=0;j<32;j++)for(int a=0;a<5;a++)if(!(j>>a&1))
 s|=Wide(bit(b,edge(7,a+(a>=f/2),64+lift(j,f/2,f&1))))<<edge(5,a,j);return s;
}

// The second search propagates pairwise compatibility of complete facet labels.
bool agree(const Option&a,int i,const Option&b,int j){
 for(int k=0;k<7;k++)if((a.bits[k]^b.bits[k])&masks[i][k]&masks[j][k])return false;
 return true;
}
using Sets=array<vector<int>,12>;
struct Search{const Graph&g;L low;L&best;array<vector<Option>,12> d;map<pair<int,Wide>,vector<Option>> other;
 void go(int mask,L sum,const Sets&sets,const vector<Option>*opp,const vector<int>&live){
  L oc=opp?(live.empty()?low:graphs[(*opp)[live.front()].id].score):g.score;
  L cap=sum+oc;int chosen=-1;size_t small=SIZE_MAX;
  for(int i=11;i>=0;i--)if(mask&(1<<i)){
   cap+=sets[i].empty()?low:graphs[d[i][sets[i][0]].id].score;
   if(sets[i].size()<small){small=sets[i].size();chosen=i;}
  }
  if(cap<=best)return;if(mask==0){best=cap;return;}
  int i=chosen,next=mask^(1<<i);const auto&v=sets[i];L hi=v.empty()?low:graphs[d[i][v.front()].id].score;
  // Try the low option first if it can still improve the incumbent.
  if(cap-hi+low>best)go(next,sum+low,sets,opp,live);
  for(int k:v){
   const auto&q=d[i][k];L sc=graphs[q.id].score;if(cap-hi+sc<=best)break;
   Sets keep;
   for(int j=0;j<12;j++)if(next&(1<<j)){
    for(int h:sets[j])if(agree(q,i,d[j][h],j))keep[j].push_back(h);
   }
   const vector<Option>*nu=opp;vector<int> ids;
   if(opp){
    for(int h:live)if(agree(q,i,(*opp)[h],13))ids.push_back(h);
   }else{
    Wide base=upper(q.bits,i);auto[it,fresh]=other.try_emplace({i,base});if(fresh)it->second=domain(13,i/2,i&1,base,g.score);
    nu=&it->second;for(int h=0;h<(int)nu->size();h++)ids.push_back(h);
   }
   go(next,sum+sc,keep,nu,ids);
  }
 }
 void run(){
  Sets sets;
  for(int j=0;j<12;j++){
   d[j]=domain(j,6,0,g.face[j].base,g.score);
   for(int k=0;k<(int)d[j].size();k++)sets[j].push_back(k);
  }
  go(4095,g.score,sets,nullptr,{});
 }
};
int main(int argc,char**argv){
 assert(argc==3||argc==4);L low=stoll(argv[2]);ifstream f(argv[1],ios::binary);assert(f);init();
 ifstream weights;if(argc==4){weights.open(argv[3],ios::binary);weights.read((char*)&low,8);assert(weights);}
 L s;while(f.read((char*)&s,8)){Six b{};f.read((char*)b.data(),24);assert(f);if(argc==4){weights.read((char*)&s,8);assert(weights);}if(s>low)ingest(b,s);}assert(f.eof()&&f.gcount()==0);
 vector<int> ix;for(int i=0;i<(int)graphs.size();i++)ix.push_back(i);
 sort(ix.begin(),ix.end(),[](int a,int b){return graphs[a].score>graphs[b].score;});
 cerr<<"six-dimensional orbits "<<graphs.size()<<" rooted base types "<<options.size()<<endl;
 L best=14*low;int work=0;for(int i:ix){if(14*graphs[i].score<=best)break;Search q{graphs[i],low,best};q.run();work++;}
 cout<<"seven_sum "<<best<<" six_orbits "<<graphs.size()<<" anchors "<<work<<endl;
}
