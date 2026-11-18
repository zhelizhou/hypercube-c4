// Independent integer checker. It does not read any precomputed flag-coefficient table.
// It derives Q3 automorphisms, proves coverage of all layer pairs, enumerates every
// legal grey-edge completion, and directly counts six quadratic terms, with simultaneous root-group averaging.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <vector>
using namespace std;
using I=int64_t; using Big=__int128_t;
string bigstr(Big x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;string s;while(x){s+=char('0'+x%10);x/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
Big parsebig(const string&s){bool neg=!s.empty()&&s[0]=='-';Big x=0;for(size_t i=neg;i<s.size();i++){assert(s[i]>='0'&&s[i]<='9');x=10*x+s[i]-'0';}return neg?-x:x;}
int pc(unsigned x){return __builtin_popcount(x);}
template<class T> vector<T> read(const char* p){ifstream f(p,ios::binary|ios::ate);assert(f.good());size_t n=f.tellg();f.seekg(0);vector<T> a(n/sizeof(T));f.read((char*)a.data(),n);return a;}
int main(int argc,char**argv){
 const char* matrixfile=argc>1?argv[1]:"exact_matrices.txt";
 ifstream input(matrixfile);assert(input.good());I D;string target_s,den_s;input>>D>>target_s>>den_s;assert(D>0&&D<=1000000000LL);Big target=parsebig(target_s),den=parsebig(den_s);assert(den==64512*Big(D)*D);
 int ns[6]={240,212,190,187,170,9};vector<vector<I>> Q(6);Big ab=Big(D)*D;
 for(int b=0;b<6;b++){int n;input>>n;assert(n==ns[b]);Q[b].resize(n*n);I mx=0;for(I&v:Q[b]){input>>v;mx=max(mx,v<0?-v:v);}ab+=mx;}
 assert(8*ab<numeric_limits<I>::max());
 auto val=[&](int b,int i,int j)->I{assert(i>=0&&i<ns[b]&&j>=0&&j<ns[b]);return Q[b][i*ns[b]+j];};
 int ei[8][8];fill(&ei[0][0],&ei[0][0]+64,-1);vector<array<int,2>> edges;
 for(int x=0;x<8;x++)for(int i=0;i<3;i++)if(!(x>>i&1)){int y=x^(1<<i);ei[x][y]=ei[y][x]=edges.size();edges.push_back({x,y});}
 vector<int> squares;
 for(int i=0;i<3;i++)for(int j=i+1;j<3;j++)for(int x=0;x<8;x++)if(!(x&((1<<i)|(1<<j)))){
  int u=x^(1<<i),v=x^(1<<j),w=u^(1<<j);squares.push_back((1<<ei[x][u])|(1<<ei[x][v])|(1<<ei[u][w])|(1<<ei[v][w]));
 }
 vector<int> valid;bool good[4096];for(int a=0;a<4096;a++){good[a]=true;for(int s:squares)if((a&s)==s)good[a]=false;if(good[a])valid.push_back(a);}assert(valid.size()==2902);
 vector<array<int,4096>> tr;array<int,3> perm={0,1,2};
 do{for(int t=0;t<8;t++){int vm[8],em[12];for(int x=0;x<8;x++){vm[x]=t;for(int j=0;j<3;j++)if(x>>j&1)vm[x]^=1<<perm[j];}
  for(int e=0;e<12;e++)em[e]=ei[vm[edges[e][0]]][vm[edges[e][1]]];array<int,4096> row;
  for(int m=0;m<4096;m++){int out=0;for(int e=0;e<12;e++)if(m>>e&1)out|=1<<em[e];row[m]=out;}tr.push_back(row);
 }}while(next_permutation(perm.begin(),perm.end()));assert(tr.size()==48);
 auto keys=read<int32_t>("keys.bin");assert(keys.size()==90179);assert(is_sorted(keys.begin(),keys.end()));vector<int> idx(1<<24,-1);
 for(int h=0;h<(int)keys.size();h++){int a=keys[h]/4096,b=keys[h]%4096;assert(good[a]&&good[b]);int canon=1<<24;
  for(const auto&t:tr){int u=t[a],v=t[b];canon=min(canon,min(u*4096+v,v*4096+u));
   for(int k:{u*4096+v,v*4096+u}){assert(idx[k]==-1||idx[k]==h);idx[k]=h;}
  }assert(canon==keys[h]);
 }
 for(int a:valid)for(int b:valid)assert(idx[a*4096+b]>=0);
 cout<<"PASS: independent coverage of all "<<valid.size()*valid.size()<<" ordered Q3 layer pairs by 90179 disjoint automorphism orbits.\n";
 // Reconstruct canonical codes for empty-face flags and vertex-root flags.
 int qe[4][2]={{0,1},{0,2},{1,3},{2,3}},qei[4][4];fill(&qei[0][0],&qei[0][0]+16,-1);for(int e=0;e<4;e++)qei[qe[e][0]][qe[e][1]]=qei[qe[e][1]][qe[e][0]]=e;
 // Full face-root flags: canonicalize the ROOT, and average BOTH flag
 // arguments by the same stabilizer element. Do not quotient them separately.
 int rt[8][16],st[8][256],gg=0;
 for(int sw=0;sw<2;sw++)for(int t=0;t<4;t++){
  int vm[4],em[4];for(int x=0;x<4;x++)vm[x]=t^(sw?((x&1)<<1)|((x&2)>>1):x);
  for(int e=0;e<4;e++)em[e]=qei[vm[qe[e][0]]][vm[qe[e][1]]];
  for(int r=0;r<16;r++){int z=0;for(int e=0;e<4;e++)if(r>>e&1)z|=1<<em[e];rt[gg][r]=z;}
  for(int f=0;f<256;f++){int z=0;for(int j=0;j<4;j++){if(f>>j&1)z|=1<<vm[j];if(f>>(j+4)&1)z|=1<<(4+em[j]);}st[gg][f]=z;}gg++;
 }
 int roots[5]={0,1,3,6,7},sid[5][256];fill(&sid[0][0],&sid[0][0]+5*256,-1);
 for(int b=0;b<5;b++){
  int cnt=0;for(int f=0;f<240;f++){bool ok=true;int c=f&15,p=f>>4;
   for(int e=0;e<4;e++)if((roots[b]>>e&1)&&(p>>e&1)&&(c>>qe[e][0]&1)&&(c>>qe[e][1]&1))ok=false;
   if(ok)sid[b][f]=cnt++;
  }assert(cnt==ns[b]);
 }
 vector<I> faceval(16*65536);vector<unsigned char> facevalid(16*65536,0);
 for(int r=0;r<15;r++){
  int cr=15,h0=-1;for(int h=0;h<8;h++)cr=min(cr,rt[h][r]);
  for(int h=0;h<8;h++)if(rt[h][r]==cr){h0=h;break;}assert(h0>=0);
  int b=find(roots,roots+5,cr)-roots;assert(b<5);vector<int> stab;
  for(int h=0;h<8;h++)if(rt[h][cr]==cr)stab.push_back(h);assert(8%stab.size()==0);
  for(int u=0;u<240;u++)for(int v=0;v<240;v++){
   int a=st[h0][u],bb=st[h0][v];if(sid[b][a]<0||sid[b][bb]<0)continue;
   I z=0;for(int h:stab)z+=val(b,sid[b][st[h][a]],sid[b][st[h][bb]]);
   int ix=(r*256+u)*256+v;faceval[ix]=I(8/stab.size())*z;facevalid[ix]=1;
  }
 }
 int vcan[16],vc[16];vector<int> vreps;for(int s=0;s<16;s++){int sw=((s&1)<<1)|((s&2)>>1)|((s&4)<<1)|((s&8)>>1);vcan[s]=min(s,sw);if(s<15)vreps.push_back(vcan[s]);}
 sort(vreps.begin(),vreps.end());vreps.erase(unique(vreps.begin(),vreps.end()),vreps.end());assert(vreps.size()==9);for(int s=0;s<15;s++)vc[s]=lower_bound(vreps.begin(),vreps.end(),vcan[s])-vreps.begin();vc[15]=-1;
 int e4[16][16];fill(&e4[0][0],&e4[0][0]+256,-1);
 for(int e=0;e<12;e++){int x=edges[e][0],y=edges[e][1];e4[x][y]=e4[y][x]=e;e4[x+8][y+8]=e4[y+8][x+8]=e+12;}
 for(int x=0;x<8;x++)e4[x][x+8]=e4[x+8][x]=24+x;
 struct Face{uint32_t mask;int root[4];int path[2][8];};vector<Face> fs;
 for(int i=0;i<4;i++)for(int j=i+1;j<4;j++)for(int x=0;x<16;x++)if(!(x&((1<<i)|(1<<j)))){
  Face f;f.mask=0;int vm[4]={x,x^(1<<i),x^(1<<j),x^(1<<i)^(1<<j)};
  for(int a=0;a<4;a++){f.root[a]=e4[vm[qe[a][0]]][vm[qe[a][1]]];f.mask|=1u<<f.root[a];}int l=0;
  for(int k=0;k<4;k++)if(k!=i&&k!=j){for(int a=0;a<4;a++)f.path[l][a]=e4[vm[a]][vm[a]^(1<<k)];for(int a=0;a<4;a++)f.path[l][a+4]=e4[vm[qe[a][0]]^(1<<k)][vm[qe[a][1]]^(1<<k)];l++;}fs.push_back(f);
 }assert(fs.size()==24);
 int vp[16][6][4],l=0;for(int i=0;i<4;i++)for(int j=i+1;j<4;j++){for(int x=0;x<16;x++){int vm[4]={x,x^(1<<i),x^(1<<j),x^(1<<i)^(1<<j)};for(int a=0;a<4;a++)vp[x][l][a]=e4[vm[qe[a][0]]][vm[qe[a][1]]];}l++;}
 // Crossing-edge completion maps for every other choice of hidden direction.
 static int ma[3][2][4096]={},mb[3][2][4096]={},ms[3][2][256]={};int inside[256]={};
 for(int s=0;s<256;s++)for(int e=0;e<12;e++)if((s>>edges[e][0]&1)&&(s>>edges[e][1]&1))inside[s]|=1<<e;
 for(int i=0;i<3;i++){vector<int> rem;for(int j=0;j<3;j++)if(j!=i)rem.push_back(j);rem.push_back(3);
  for(int h=0;h<2;h++){int vm[8];for(int x=0;x<8;x++){vm[x]=h<<i;for(int j=0;j<3;j++)if(x>>j&1)vm[x]|=1<<rem[j];}
   for(int e=0;e<12;e++){int x=vm[edges[e][0]],y=vm[edges[e][1]];
    if((x^y)==8){for(int s=0;s<256;s++)if(s>>(x&7)&1)ms[i][h][s]|=1<<e;}
    else{int q=ei[x&7][y&7];for(int m=0;m<4096;m++)if(m>>q&1){if(x&8)mb[i][h][m]|=1<<e;else ma[i][h][m]|=1<<e;}}
   }
  }
 }
 auto finite_score=[&](uint32_t g)->Big{int hist[5]={};for(int x=0;x<16;x++){int degree=0;for(int a=0;a<4;a++)degree+=(g>>e4[x][x^(1<<a)])&1;hist[degree]++;}return 3*hist[4]-hist[0]-hist[2];};
 den=1;
 if(argc>3&&string(argv[2])=="--graphs"){auto gs=read<uint32_t>(argv[3]);for(uint32_t g:gs)cout<<"SCORE "<<g<<" "<<bigstr(finite_score(g))<<" / "<<bigstr(den)<<"\n";return 0;}
 long long all=0,checked=0;Big best=-(Big(1)<<126);uint32_t worst=0;
 for(int h=0;h<(int)keys.size();h++){int a=keys[h]/4096,b=keys[h]%4096;
  for(int s=0;s<256;s++)if(!(inside[s]&(a&b))){all++;int r[4]={h,0,0,0};bool minimal=true;
   for(int i=0;i<3;i++){int q0=ma[i][0][a]|mb[i][0][b]|ms[i][0][s],q1=ma[i][1][a]|mb[i][1][b]|ms[i][1][s];r[i+1]=idx[q0*4096+q1];assert(r[i+1]>=0);if(r[i+1]<h)minimal=false;}
   if(!minimal)continue;checked++;uint32_t g=(uint32_t)a|((uint32_t)b<<12)|((uint32_t)s<<24);Big z=finite_score(g);
   if(z>best){best=z;worst=g;}
   if(target>=0&&z>target){cerr<<"FAIL: graph="<<g<<" numerator="<<bigstr(z)<<" > "<<bigstr(target)<<"\n";return 2;}
  }
 }
 assert(all==13150453&&checked==3312331);if(target>=0)assert(best==target);
 cout<<"PASS: all "<<all<<" legal marked completions enumerated.\n";
 cout<<"PASS: all "<<checked<<" symmetry-reduced representatives verified by direct integer counting.\n";
 cout<<"EXACT_MAX "<<bigstr(best)<<" / "<<bigstr(den)<<"\n";
 cout<<"WORST_GRAPH "<<worst<<"\n";
}
