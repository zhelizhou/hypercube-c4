#include <algorithm>
#include <cassert>
#include <cstdint>
#include <vector>
#include <fstream>
#include <string>
using namespace std;
using L=int64_t;using I=__int128_t;
vector<L> read_file(const char*p){
 ifstream f(p,ios::binary|ios::ate);assert(f&&f.tellg()%8==0);
 vector<L> v(f.tellg()/8);f.seekg(0);f.read((char*)v.data(),8*v.size());assert(f);return v;
}
void write_file(const char*p,const vector<L>&v){
 ofstream f(p,ios::binary);f.write((const char*)v.data(),8*v.size());assert(f);
}
int main(int argc,char**argv){
 assert(argc==8);L m=stoll(argv[4]),d=stoll(argv[5]);assert(0<m&&m<d);
 auto u=read_file(argv[1]),s=read_file(argv[2]),g=read_file(argv[3]);assert(u.size()==s.size());
 for(size_t i=0;i<u.size();i++){
  I x=I(d-m)*u[i]+I(m)*s[i];u[i]=x/d+(x%d>0);
 }
 for(L&v:g){assert(v>=0);v=(I(d-m)*v)/d;}
 write_file(argv[6],u);write_file(argv[7],g);
}
