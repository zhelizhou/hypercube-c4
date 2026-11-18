
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

int main(int argc,char**argv){
 assert(argc==6);
 geometry();Attachments attach(edges4);ifstream f(argv[1]);string magic;int n;f>>magic>>n;assert(f&&magic=="ARM_FACTORS_V1"&&n==99);
 vector<ll> gap(99*65536);vector<ll> diagonal(99*256);
 for(int t=0;t<99;t++){
  int rank;f>>rank;assert(f&&rank>=0&&rank<=256);
  vector<vector<ll>> b(256,vector<ll>(rank));
  for(auto&row:b)for(auto&v:row){f>>v;assert(f&&v>=-10000000&&v<=10000000);}
  for(int i=0;i<256;i++){
   for(ll v:b[i])diagonal[t*256+i]+=v*v;
   for(int j=i;j<256;j++){
    ll d=0;for(int k=0;k<rank;k++){ll v=b[i][k]-b[j][k];d+=v*v;}
    gap[(t*256+i)*256+j]=d;
   }
  }
 }
 string trailing;assert(!(f>>trailing));
 auto masks=readf<u32>(argv[2]);auto scores=readf<ll>(argv[3]);assert(masks.size()==scores.size());
 for(size_t i=0;i<masks.size();i++){
  uint16_t a[8];attach.unary(masks[i],a);__int128 s=scores[i];
  for(int j=0;j<8;j++)s+=diagonal[a[j]];
  assert(s>-(ll(1)<<57)&&s<(ll(1)<<57));scores[i]=(ll)s;
 }
 ofstream unary(argv[4],ios::binary),g(argv[5],ios::binary);
 unary.write((char*)scores.data(),scores.size()*8);g.write((char*)gap.data(),gap.size()*8);
 assert(unary&&g);return 0;
}
