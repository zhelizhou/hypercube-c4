#include "five_geometry.hpp"
int main(int argc,char**argv){
 assert(argc==4);ifstream f(argv[1],ios::binary),input(argv[2],ios::binary);ofstream out(argv[3],ios::binary);assert(f&&input&&out);
 geometry();Rec r;while(f.read((char*)&r,24))ingest(r);
 vector<int> ix(raw.size());iota(ix.begin(),ix.end(),0);sort(ix.begin(),ix.end(),[](int a,int b){return codes[a]<codes[b];});
 for(int j=0;j<(int)ix.size();j++)store_graph(raw[ix[j]],j);
 L sc;array<uint64_t,3> bits;
 while(input.read((char*)&sc,8)){
  input.read((char*)bits.data(),24);assert(input);
  auto edge=[&](int d,int v){int q=32*d+drop(v,d);return (bits[q/64]>>(q%64))&1;};
  array<int,12> labs;labs.fill(-1);
  for(int z=0;z<12;z++){
   int d=z/2,t=z&1;array<int,5> ax;int na=0;for(int j=0;j<6;j++)if(j!=d)ax[na++]=j;
   U base=0,vv=0,opp=0;
   for(int v=0;v<16;v++){
    int x=t<<d;for(int j=0;j<4;j++)x|=((v>>j)&1)<<ax[j];vv|=U(edge(ax[4],x))<<v;
    for(int j=0;j<4;j++)if(!(v>>j&1)){int b=edgebit(j,v,4);base|=U(edge(ax[j],x))<<b;opp|=U(edge(ax[j],x^(1<<ax[4])))<<b;}
   }
   auto&c=canon(base);auto it=options.find(c.base);if(it==options.end())continue;auto &g=acts[c.send.front()];
   auto jt=it->second.find((uint64_t(g.verts(vv))<<32)|g.edges(opp));if(jt!=it->second.end())labs[z]=jt->second.second;
  }
  out.write((char*)&sc,8);out.write((char*)labs.data(),48);
 }
 assert(out&&input.eof()&&input.gcount()==0);
}
