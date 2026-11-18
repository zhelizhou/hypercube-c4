#include "five_geometry.hpp"
U legacy(U b){
 U out=0;for(int d=0;d<4;d++)for(int x=0;x<16;x++)if(!(x>>d&1)){
  unsigned v=b>>edgebit(d,x,4)&1u;int k=d==0?(x>>1):(8+12*(1-(x&1))+edgebit(d-1,x>>1,3));out|=v<<k;
 }
 return out;
}
void features(const vector<int>&idx,const char* path){
 ifstream p("full_masks.bin",ios::binary|ios::ate);assert(p);vector<U> m(p.tellg()/4);p.seekg(0);p.read((char*)m.data(),m.size()*4);
 ofstream out(path,ios::binary);map<U,int> cv;
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
 assert(argc==3);ifstream input(argv[1],ios::binary);assert(input);geometry();Rec r;
 while(input.read((char*)&r,24))ingest(r);assert(input.eof()&&input.gcount()==0);
 vector<int> ix(raw.size());iota(ix.begin(),ix.end(),0);
 sort(ix.begin(),ix.end(),[](int a,int b){return codes[a]<codes[b];});
 features(ix,argv[2]);
}
