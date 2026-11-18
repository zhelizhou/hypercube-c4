#ifdef __BMI2__
#include <immintrin.h>
#endif
#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <vector>
#include <omp.h>
using namespace std;
using u32=uint32_t;using ll=int64_t;
template<class T>vector<T> readf(const char* name){ifstream f(name,ios::binary|ios::ate);assert(f);vector<T> a(f.tellg()/sizeof(T));f.seekg(0);f.read((char*)a.data(),a.size()*sizeof(T));assert(f);return a;}
vector<pair<int,int>> edges3,edges4;
int idx4[16][16],idx3[8][8];
using Tab=array<array<u32,256>,4>;
vector<Tab> syms;
static u32 proj[6][8][4096];
void geometry(){
 for(int d=0;d<3;d++)for(int x=0;x<8;x++)if(!(x>>d&1)){int y=x^(1<<d);idx3[x][y]=idx3[y][x]=edges3.size();edges3.emplace_back(x,y);}
 for(int x=0;x<8;x++)edges4.emplace_back(2*x,2*x+1);
 for(int p:{1,0})for(auto[x,y]:edges3)edges4.emplace_back(2*x+p,2*y+p);
 for(int b=0;b<32;b++){auto[x,y]=edges4[b];idx4[x][y]=idx4[y][x]=b;}
 array<int,4> perm{0,1,2,3};
 do{for(int t=0;t<16;t++){
  auto mapv=[&](int x){int z=t;for(int j=0;j<4;j++)z^=(x>>j&1)<<perm[j];return z;};
  Tab tab{};for(int b=0;b<32;b++){auto[x,y]=edges4[b];u32 dest=1u<<idx4[mapv(x)][mapv(y)]; for(int v=0;v<256;v++)if(v>>(b%8)&1)tab[b/8][v]|=dest;}
  syms.push_back(tab);
 }}while(next_permutation(perm.begin(),perm.end()));
 // Q5 ordering bits x,y,r0,r1,r2. Component order A,B,C,D,X,Y,Z,W.
 array<vector<pair<int,int>>,8> parts;
 for(int b=0;b<4;b++)for(auto[x,y]:edges3)parts[b].emplace_back(4*x+b,4*y+b);
 for(int b=4;b<8;b++)for(int r=0;r<8;r++){
  static int ends[][2]={{0,1},{0,2},{1,3},{2,3}};parts[b].emplace_back(4*r+ends[b-4][0],4*r+ends[b-4][1]);
 }
 for(int i=0;i<3;i++)for(int t=0;t<2;t++)for(int b=0;b<8;b++){
  auto compress=[&](int x){int lower=(1<<(i+2))-1;return (x&lower)|((x>>(i+3))<<(i+2));};
  array<u32,12> bits{};for(int j=0;j<(int)parts[b].size();j++){
   auto[x,y]=parts[b][j];if((x>>(i+2)&1)!=t||(y>>(i+2)&1)!=t)continue;
   bits[j]=1u<<idx4[compress(x)][compress(y)];
  }
  for(int z=1;z<(1<<parts[b].size());z++)proj[2*i+t][b][z]=proj[2*i+t][b][z&(z-1)]|bits[countr_zero((u32)z)];
 }
}
u32 image(const Tab&tab,u32 m){return tab[0][m&255]|tab[1][m>>8&255]|tab[2][m>>16&255]|tab[3][m>>24];}
struct E{int c;int m;int id;};
#include "arms.hpp"
static u32 compress_bits(u32 x,u32 mask){
#ifdef __BMI2__
    return _pext_u32(x,mask);
#else
    u32 answer=0, out=1;
    while(mask){u32 bit=mask&(~mask+1u); if(x&bit)answer|=out;mask-=bit;out<<=1;}
    return answer;
#endif
}
int main(int argc,char**argv){
 assert(argc>=4);geometry();auto masks=readf<u32>("full_masks.bin");auto s=readf<ll>(argv[1]);assert(masks.size()==s.size());
 const ll bound=stoll(argv[2]),floor=10*bound-9*(*max_element(s.begin(),s.end()));
 vector<int> active,piv;unordered_map<u32,int> ids;vector<vector<E>> adj(4096);unordered_map<u32,vector<E>> between;
 for(int i=0;i<(int)s.size();i++)if(s[i]>=floor){active.push_back(i);if(s[i]>=bound)piv.push_back(i);}
 sort(piv.begin(),piv.end(),[&](int x,int y){return s[x]>s[y];});
 for(int id:active)for(auto&g:syms){
  u32 m=image(g,masks[id]);if(!ids.emplace(m,id).second)continue;int a=m>>20,b=m>>8&4095,c=m&255;E e{b,c,id};
  adj[a].push_back(e);between[m>>8].push_back(e);
 }
 cerr<<"cutoff "<<floor<<" eligible orbits "<<active.size()<<" pivots "<<piv.size()<<" labelled "<<ids.size()<<endl;
 
 u32 mask20=0;
 for(int t:{0,1,2,4,5})mask20|=proj[0][t][t<4?4095:255];
 assert(popcount(mask20)==20);
 vector<ll> cap20(1<<20, floor-1);
 for(auto [raw,id]:ids){auto &q=cap20[compress_bits(raw,mask20)];q=max(q,s[id]);}
 auto cmp=[&](E a,E b){return s[a.id]>s[b.id];};
 for(auto&v:adj)sort(v.begin(),v.end(),cmp); for(auto&[k,v]:between)sort(v.begin(),v.end(),cmp);
 const auto &lookup=ids;const auto &opposite=between;
 Attachments attach(edges4);auto K=readf<ll>(argv[4]);assert(K.size()==99*256*256);
 int num=piv.size();assert(argc==5 && string(argv[3])=="all");atomic<ll> maxscore(10*bound);atomic<int> done(0);ofstream out("high5.bin",ios::binary); int64_t count=0; 
 #pragma omp parallel for schedule(dynamic,1)
 for(int i=0;i<num;i++){
   int id=piv[i];ll top=s[id]; if(10*top <maxscore.load())continue;
  u32 h=masks[id];size_t cost=~size_t(0);
  for(auto&g:syms){u32 m=image(g,masks[id]);size_t cc=adj[m>>20].size()*adj[m>>8&4095].size();if(cc<cost){cost=cc;h=m;}}
  int A=h>>20,B=h>>8&4095,X=h&255;
  array<u32,6> pre;for(int j=0;j<6;j++)pre[j]=proj[j][0][A]|proj[j][1][B]|proj[j][4][X];
  for(const E& y:adj[A]){
   ll sy=s[y.id];if(sy>top)continue;if(9*top+sy<maxscore.load())break;
   array<u32,6> pre2;for(int j=0;j<6;j++)pre2[j]=pre[j]|proj[j][2][y.c]|proj[j][5][y.m];

   ll six=0;bool viable=true;
   for(int k=0;k<6;k++){
    ll cap=cap20[compress_bits(pre2[k],mask20)];
    if(cap<floor){viable=false;break;}
    six+=min(top,cap);
   }
   if(!viable || 3*top+sy+six<maxscore.load())continue;
   for(const E& z:adj[B]){
    ll sz=s[z.id];if(sz>top)continue;if(8*top+sy+sz<maxscore.load())break;
    auto it=opposite.find(y.c*4096+z.c);if(it==opposite.end())continue;
    const auto& list=it->second;if(top+six+sy+sz+min(top,s[list.front().id])<maxscore.load())continue;
    u32 pre3[6];for(int j=0;j<6;j++)pre3[j]=pre2[j]|proj[j][3][z.c]|proj[j][6][z.m];
    int forbidden=X&y.m&z.m;
    for(const E& v:list){
     ll sv=s[v.id]; if(sv>top)continue;if(top+six+sy+sz+sv<maxscore.load())break;if(forbidden&v.m)continue;
     ll sum=top+sy+sz+sv;array<int,10> row{id,y.id,z.id,v.id};int j=0;
     for(;j<6;j++){auto jt=lookup.find(pre3[j]|proj[j][7][v.m]);if(jt==lookup.end())break;
      int n=jt->second;if(s[n]>top)break;row[4+j]=n;sum+=s[n];if(sum+(5-j)*top<maxscore.load())break;
     }
     if(j==6){
       u32 ff[10]={(u32(A)<<20)|u32(y.c<<8)|u32(y.m),(u32(B)<<20)|u32(z.c<<8)|u32(z.m),h,(u32(y.c)<<20)|u32(z.c<<8)|u32(v.m)};
       for(int b=0;b<6;++b)ff[4+b]=pre3[b]|proj[b][7][v.m];
       u32 keys[40];attach.keys(ff,keys);
       for(auto e:keys)sum-=K[e];
       if(sum<maxscore.load())continue;
      #pragma omp critical
      {array<uint16_t,8> record{(uint16_t)A,(uint16_t)B,(uint16_t)y.c,(uint16_t)z.c,(uint16_t)X,(uint16_t)y.m,(uint16_t)z.m,(uint16_t)v.m};out.write((char*)&sum,8);out.write((char*)record.data(),16);++count;}
     }
    }
   }
  }
  int n=++done;if(n%100==0){cerr<<"processed "<<n<<" max "<<maxscore.load()<<endl;}
 }
 cout<<"full pivot count "<<num<<", qualifying configurations "<<count<<endl;assert(out);
}
