// Independently constructed from the abstract scoring contract, 2026-11-16.
// No producer geometry, oracle implementation, or stored orbit keys were read.
#include <algorithm>
#include <array>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using I=__int128_t; using U=uint32_t; using L=int64_t;
std::string str(I x){if(!x)return "0";bool neg=x<0;if(neg)x=-x;std::string s;while(x){s+=char('0'+x%10);x/=10;}if(neg)s+='-';reverse(s.begin(),s.end());return s;}
void need(bool x,const std::string&s){if(!x)throw std::runtime_error(s);}
L narrow(I x){need(x>=std::numeric_limits<L>::min()&&x<=std::numeric_limits<L>::max(),"int64 table overflow");return L(x);}
I ab(I x){return x<0?-x:x;}
struct Cube {int n;std::vector<std::pair<int,int>> edges;std::vector<std::vector<int>> ei;std::vector<U>squares;
 Cube(int n_):n(n_),ei(1<<n_,std::vector<int>(1<<n_,-1)){}
 bool legal(U m)const{for(U s:squares)if((m&s)==s)return false;return true;}
};
// Required Q3 edge order is x-major within each lower-dimensional layer,
// not recursive Q2 layering. Set it explicitly before any Q4 geometry exists.
Cube q3(3),q4(4);
void initialize_edges(){
 q3.edges.clear();for(auto&r:q3.ei)std::fill(r.begin(),r.end(),-1);
 for(int x=0;x<8;++x)for(int a=0;a<3;++a)if(!(x&(1<<a))){int y=x^(1<<a);q3.ei[x][y]=q3.ei[y][x]=int(q3.edges.size());q3.edges.push_back({x,y});}
 q3.squares.clear();for(int a=0;a<3;++a)for(int b=a+1;b<3;++b)for(int x=0;x<8;++x)if(!(x&(1<<a))&&!(x&(1<<b))){U s=0;for(auto e:std::array<std::pair<int,int>,4>{{{x,x^(1<<a)},{x,x^(1<<b)},{x^(1<<a),x^(1<<a)^(1<<b)},{x^(1<<b),x^(1<<a)^(1<<b)}}})s|=U(1)<<q3.ei[e.first][e.second];q3.squares.push_back(s);}
 q4.edges.clear();for(auto&r:q4.ei)std::fill(r.begin(),r.end(),-1);
 for(int layer=0;layer<2;++layer)for(auto [x,y]:q3.edges){x+=8*layer;y+=8*layer;q4.ei[x][y]=q4.ei[y][x]=int(q4.edges.size());q4.edges.push_back({x,y});}
 for(int x=0;x<8;++x){q4.ei[x][x+8]=q4.ei[x+8][x]=int(q4.edges.size());q4.edges.push_back({x,x+8});}
 q4.squares.clear();for(int a=0;a<4;++a)for(int b=a+1;b<4;++b)for(int x=0;x<16;++x)if(!(x&(1<<a))&&!(x&(1<<b))){U s=0;for(auto e:std::array<std::pair<int,int>,4>{{{x,x^(1<<a)},{x,x^(1<<b)},{x^(1<<a),x^(1<<a)^(1<<b)},{x^(1<<b),x^(1<<a)^(1<<b)}}})s|=U(1)<<q4.ei[e.first][e.second];q4.squares.push_back(s);}
 need(q3.edges.size()==12&&q3.squares.size()==6&&q4.edges.size()==32&&q4.squares.size()==24,"cube dimensions");
}
struct Iso {std::vector<int> v,e;};
std::vector<Iso> isometries(const Cube&c){std::vector<Iso> out;std::vector<int> p(c.n);std::iota(p.begin(),p.end(),0);do{for(int t=0;t<(1<<c.n);++t){Iso g;g.v.resize(1<<c.n);for(int x=0;x<(1<<c.n);++x){int y=t;for(int a=0;a<c.n;++a)if(x&(1<<a))y^=1<<p[a];g.v[x]=y;}for(auto [x,y]:c.edges){int k=c.ei[g.v[x]][g.v[y]];need(k>=0,"isometry edge");g.e.push_back(k);}out.push_back(g);}}while(std::next_permutation(p.begin(),p.end()));return out;}
U transform(U m,const Iso&g){U r=0;while(m){int b=__builtin_ctz(m);m&=m-1;r|=U(1)<<g.e[b];}return r;}
const std::array<std::pair<int,int>,4> sqedges={{{0,1},{0,2},{1,3},{2,3}}};
struct SqIso {std::array<int,4> v,e;};
std::vector<SqIso> sqgroup(){std::vector<SqIso>r;for(int swap=0;swap<2;++swap)for(int t=0;t<4;++t){SqIso g;for(int x=0;x<4;++x)g.v[x]=(swap?(((x&1)<<1)|((x&2)>>1)):x)^t;for(int i=0;i<4;++i){auto [a,b]=sqedges[i];a=g.v[a];b=g.v[b];if(a>b)std::swap(a,b);int j=0;while(j<4&&sqedges[j]!=std::pair<int,int>(a,b))++j;need(j<4,"square action");g.e[i]=j;}r.push_back(g);}return r;}
int rootmap(int m,const SqIso&g){int r=0;for(int j=0;j<4;++j)if(m&(1<<j))r|=1<<g.e[j];return r;}
int flagmap(int m,const SqIso&g){int r=0;for(int j=0;j<4;++j){if(m&(1<<j))r|=1<<g.v[j];if(m&(1<<(4+j)))r|=1<<(4+g.e[j]);}return r;}
bool flaglegal(int root,int code){if(code>=240)return false;for(int j=0;j<4;++j){auto[a,b]=sqedges[j];if((root&(1<<j))&&(code&(1<<(4+j)))&&(code&(1<<a))&&(code&(1<<b)))return false;}return true;}
struct Inputs {L D,target,den;std::array<int,6>dim;std::array<std::vector<L>,6>q;std::array<L,6>lin;I maxface=0,maxvertex=0,absbound=0;};
Inputs readinput(const char*mat,const char*linear){Inputs x;std::ifstream f(mat);need(bool(f),"open matrix input");need(bool(f>>x.D>>x.target>>x.den),"matrix header");need(x.den>0,"positive metadata denominator");int ds[]={240,212,190,187,170,9};for(int b=0;b<6;++b){need(bool(f>>x.dim[b])&&x.dim[b]==ds[b],"matrix dimension");int n=ds[b];x.q[b].resize(n*n);for(auto&v:x.q[b])need(bool(f>>v),"matrix integer");for(int i=0;i<n;++i)for(int j=0;j<n;++j){need(x.q[b][i*n+j]==x.q[b][j*n+i],"matrix symmetric");I v=ab(x.q[b][i*n+j]);if(b<5)x.maxface=std::max(x.maxface,v);else x.maxvertex=std::max(x.maxvertex,v);}}std::string extra;need(!(f>>extra),"trailing matrix data");std::ifstream l(linear);need(bool(l),"open linear input");for(auto&v:x.lin)need(bool(l>>v),"linear coefficient");need(!(l>>extra),"trailing linear data");I hm=0;for(int j=1;j<6;++j)hm=std::max(hm,ab(x.lin[j]));x.absbound=32*ab(x.lin[0])+16*hm+64512*(x.maxface+x.maxvertex);need(x.absbound<(I(1)<<120),"128-bit bound");return x;}
struct Tables {std::array<std::vector<L>,15>face;std::vector<L>vertex;std::array<bool,65536>vlegal{};std::array<int,16>vstate{};std::array<std::array<int,256>,5>fi{};std::vector<SqIso>sg;};
Tables make_scores(const Inputs&in){Tables t;t.sg=sqgroup();int roots[]={0,1,3,6,7};for(int k=0;k<5;++k){t.fi[k].fill(-1);int count=0;for(int c=0;c<240;++c)if(flaglegal(roots[k],c))t.fi[k][c]=count++;need(count==in.dim[k],"independent legal flag count");std::cout<<"FLAG_COUNT root="<<roots[k]<<" count="<<count<<"\n";}
 for(int r=0;r<15;++r){int cr=16,cg=-1;for(int j=0;j<8;++j){int z=rootmap(r,t.sg[j]);if(z<cr){cr=z;cg=j;}}int k=0;while(k<5&&roots[k]!=cr)++k;need(k<5,"root orbit");std::vector<int>st;for(int g=0;g<8;++g)if(rootmap(cr,t.sg[g])==cr)st.push_back(g);need(8%st.size()==0,"stabilizer divisibility");std::array<std::vector<int>,256> ims;for(int c=0;c<240;++c)if(flaglegal(r,c)){int canonical=flagmap(c,t.sg[cg]);for(int g:st){int state=t.fi[k][flagmap(canonical,t.sg[g])];need(state>=0,"transported flag state");ims[c].push_back(state);}}
  t.face[r].assign(65536,0);std::array<L,256>diagonal{};auto face8=[&](int s,int u)->L{I sum=0;for(unsigned j=0;j<st.size();++j)sum+=in.q[k][ims[s][j]*in.dim[k]+ims[u][j]];return narrow(sum*(8/st.size()));};for(int s=0;s<240;++s)if(!ims[s].empty())diagonal[s]=face8(s,s);for(int s=0;s<240;++s)if(!ims[s].empty())for(int u=0;u<240;++u)if(!ims[u].empty())t.face[r][s|(u<<8)]=narrow(280*I(face8(s,u))+28*I(diagonal[s])+28*I(diagonal[u]));
 }
 t.vstate.fill(-1);int reps[]={0,1,3,4,5,6,7,12,13};for(int c=0;c<15;++c){int sw=((c&1)<<1)|((c&2)>>1)|((c&4)<<1)|((c&8)>>1);int rep=std::min(c,sw);int i=0;while(i<9&&reps[i]!=rep)++i;need(i<9,"vertex state orbit");t.vstate[c]=i;}
 std::array<std::pair<int,int>,6>pairs;int z=0;for(int a=0;a<4;++a)for(int b=a+1;b<4;++b)pairs[z++]={a,b};int dis=0,ov=0,diag=0;for(int i=0;i<6;++i)for(int j=i;j<6;++j){if(i==j)++diag;else{auto[a,b]=pairs[i];auto[c,d]=pairs[j];if(a!=c&&a!=d&&b!=c&&b!=d)++dis;else ++ov;}}need(dis==3&&ov==12&&diag==6,"vertex pair multiplicities");t.vertex.resize(65536);for(int x=0;x<65536;++x){int states[6];bool legal=true;for(int i=0;i<6;++i){auto[a,b]=pairs[i];int c=((x>>a)&1)|(((x>>b)&1)<<1)|(((x>>(4+2*i))&3)<<2);if(c==15){legal=false;break;}states[i]=t.vstate[c];}if(!legal)continue;I sum=0;for(int i=0;i<6;++i)for(int j=i;j<6;++j){auto[a,b]=pairs[i];auto[c,d]=pairs[j];int weight=i==j?24:((a!=c&&a!=d&&b!=c&&b!=d)?720:144);sum+=I(weight)*in.q[5][states[i]*9+states[j]];}t.vertex[x]=narrow(sum);t.vlegal[x]=true;}
 return t;
}
struct Geometry {std::vector<std::array<int,20>>faces;std::vector<std::array<int,16>>verts;U ft[24][4][256]{};uint16_t vt[16][4][256]{};};
template<size_t N>U gather(U m,const std::array<int,N>&es){U z=0;for(unsigned j=0;j<N;++j)z|=((m>>es[j])&1)<<j;return z;}
Geometry make_geometry(){Geometry g;for(int a=0;a<4;++a)for(int b=a+1;b<4;++b)for(int base=0;base<16;++base)if(!(base&(1<<a))&&!(base&(1<<b))){std::array<int,20>bits;int rv[4];for(int x=0;x<4;++x)rv[x]=base|((x&1)?1<<a:0)|((x&2)?1<<b:0);for(int j=0;j<4;++j){auto[x,y]=sqedges[j];bits[j]=q4.ei[rv[x]][rv[y]];}int t=4;for(int d=0;d<4;++d)if(d!=a&&d!=b){for(int x=0;x<4;++x)bits[t++]=q4.ei[rv[x]][rv[x]^(1<<d)];for(auto[x,y]:sqedges)bits[t++]=q4.ei[rv[x]^(1<<d)][rv[y]^(1<<d)];}need(t==20,"face geometry");g.faces.push_back(bits);}
 for(int v=0;v<16;++v){std::array<int,16>bits;int j=0;for(int a=0;a<4;++a)bits[j++]=q4.ei[v][v^(1<<a)];for(int a=0;a<4;++a)for(int b=a+1;b<4;++b){bits[j++]=q4.ei[v^(1<<a)][v^(1<<a)^(1<<b)];bits[j++]=q4.ei[v^(1<<b)][v^(1<<a)^(1<<b)];}need(j==16,"vertex geometry");g.verts.push_back(bits);}
 for(int f=0;f<24;++f)for(int b=0;b<4;++b)for(int x=0;x<256;++x)g.ft[f][b][x]=gather(U(x)<<(8*b),g.faces[f]);
 for(int v=0;v<16;++v)for(int b=0;b<4;++b)for(int x=0;x<256;++x)g.vt[v][b][x]=uint16_t(gather(U(x)<<(8*b),g.verts[v]));
 return g;
}
I literal_score(U mask,const Inputs&in,const Tables&t,const Geometry&g){need(q4.legal(mask),"literal score illegal square");int deg[16]={};int edges=0;for(int e=0;e<32;++e)if(mask&(U(1)<<e)){++edges;auto[x,y]=q4.edges[e];++deg[x];++deg[y];}I z=I(in.lin[0])*edges;for(int d:deg)z+=in.lin[1+d];for(auto&f:g.faces){U x=gather(mask,f);int r=x&15,s=(x>>4)&255,u=(x>>12)&255;need(r<15&&flaglegal(r,s)&&flaglegal(r,u),"literal illegal flag");z+=t.face[r][s|(u<<8)];}for(auto&v:g.verts){U x=gather(mask,v);need(t.vlegal[x],"literal illegal vertex state");z+=t.vertex[x];}return z;}
// Literal scorer: query each requested edge by endpoints and contract raw Q
// entries directly. It uses neither bit-gather geometry nor score tables.
I raw_literal_score(U mask,const Inputs&in,const Tables&t){
 auto edge=[&](int x,int y){int e=q4.ei[x][y];need(e>=0,"literal nonedge requested");return int((mask>>e)&1);};
 int degree[16]={};int ec=0;
 for(auto [x,y]:q4.edges)if(edge(x,y)){++degree[x];++degree[y];++ec;}
 I z=I(in.lin[0])*ec;for(int d:degree)z+=in.lin[1+d];
 int roots[]={0,1,3,6,7};
 for(int a=0;a<4;++a)for(int b=a+1;b<4;++b)for(int base=0;base<16;++base)if(!(base&(1<<a))&&!(base&(1<<b))){
  int rv[4];for(int x=0;x<4;++x)rv[x]=base|((x&1)?1<<a:0)|((x&2)?1<<b:0);
  int r=0;for(int j=0;j<4;++j){auto[x,y]=sqedges[j];r|=edge(rv[x],rv[y])<<j;}
  int flags[2],nf=0;
  for(int d=0;d<4;++d)if(d!=a&&d!=b){int code=0;for(int x=0;x<4;++x)code|=edge(rv[x],rv[x]^(1<<d))<<x;for(int j=0;j<4;++j){auto[x,y]=sqedges[j];code|=edge(rv[x]^(1<<d),rv[y]^(1<<d))<<(4+j);}need(flaglegal(r,code),"raw literal flag legal");flags[nf++]=code;}
  int canonical=16,cg=-1;for(int g=0;g<8;++g){int im=rootmap(r,t.sg[g]);if(im<canonical){canonical=im;cg=g;}}
  int block=0;while(block<5&&roots[block]!=canonical)++block;need(block<5,"raw literal root orbit");
  int s=flagmap(flags[0],t.sg[cg]),u=flagmap(flags[1],t.sg[cg]);I sum=0;int stabilizer=0;
  for(int g=0;g<8;++g)if(rootmap(canonical,t.sg[g])==canonical){++stabilizer;int i=t.fi[block][flagmap(s,t.sg[g])],j=t.fi[block][flagmap(u,t.sg[g])];need(i>=0&&j>=0,"raw literal flag index");int n=in.dim[block];sum+=I(280)*in.q[block][i*n+j]+I(28)*in.q[block][i*n+i]+I(28)*in.q[block][j*n+j];}
  need(8%stabilizer==0,"raw literal stabilizer");z+=sum*(8/stabilizer);
 }
 for(int v=0;v<16;++v){int states[6],dirs[6],k=0;for(int a=0;a<4;++a)for(int b=a+1;b<4;++b){int code=edge(v,v^(1<<a))|(edge(v,v^(1<<b))<<1)|(edge(v^(1<<a),v^(1<<a)^(1<<b))<<2)|(edge(v^(1<<b),v^(1<<a)^(1<<b))<<3);need(code<15,"raw literal vertex C4");states[k]=t.vstate[code];dirs[k++]=(1<<a)|(1<<b);}
  for(int i=0;i<6;++i)for(int j=i;j<6;++j){int weight=i==j?24:((dirs[i]&dirs[j])?144:720);z+=I(weight)*in.q[5][states[i]*9+states[j]];}
 }
 return z;
}

bool common_neighbor_check(U mask){for(int a=0;a<16;++a)for(int b=a+1;b<16;++b){int count=0;for(int v=0;v<16;++v){int e=q4.ei[a][v],f=q4.ei[b][v];if(e>=0&&f>=0&&(mask&(U(1)<<e))&&(mask&(U(1)<<f)))++count;}if(count>=2)return false;}return true;}
int main(int argc,char**argv){try{need(argc==4||argc==5,"usage: independent_q4 matrix.txt --linear linear.txt [representative_limit]");need(std::string(argv[2])=="--linear","explicit --linear required");uint64_t limit=argc==5?std::stoull(argv[4]):0;auto started=std::chrono::steady_clock::now();initialize_edges();Inputs in=readinput(argv[1],argv[3]);std::cout<<"INDEPENDENT_RAW_FUNCTIONAL D_metadata="<<in.D<<" target_metadata="<<in.target<<" denominator_metadata="<<in.den<<"\n";std::cout<<"MATRIX_MAX_ABS face="<<str(in.maxface)<<" vertex="<<str(in.maxvertex)<<"\n";std::cout<<"ABSOLUTE_SCORE_BOUND "<<str(in.absbound)<<" less_than_int64="<<(in.absbound<=std::numeric_limits<L>::max())<<" accumulator_bits=128\n";Tables t=make_scores(in);Geometry geom=make_geometry();auto aut=isometries(q3);need(aut.size()==48,"Q3 automorphism count");std::vector<int>legal;std::array<int,4096>idx;idx.fill(-1);for(int m=0;m<4096;++m)if(q3.legal(m)){idx[m]=int(legal.size());legal.push_back(m);}int n=int(legal.size());std::cout<<"Q3_LEGAL_BY_SIX_SQUARE_TESTS "<<n<<"\n";need(n==2902,"Q3 count comparison");std::vector<std::array<uint16_t,48>>transport(n);for(int i=0;i<n;++i)for(int h=0;h<48;++h){U im=transform(legal[i],aut[h]);need(idx[im]>=0,"legal-domain isometry closure");transport[i][h]=uint16_t(idx[im]);}
 std::vector<uint8_t>seen(size_t(n)*n);std::vector<std::pair<uint16_t,uint16_t>>reps;uint64_t orbit_sum=0;std::vector<uint64_t>orbit_hist(97);for(int i=0;i<n;++i)for(int j=0;j<n;++j){size_t key=size_t(i)*n+j;if(seen[key])continue;reps.push_back({uint16_t(i),uint16_t(j)});uint64_t added=0;for(int h=0;h<48;++h){int a=transport[i][h],b=transport[j][h];size_t p=size_t(a)*n+b,q=size_t(b)*n+a;if(!seen[p]){seen[p]=1;++added;}if(!seen[q]){seen[q]=1;++added;}}need(added>0&&added<=96,"orbit size");orbit_sum+=added;++orbit_hist[added];}need(orbit_sum==uint64_t(n)*n,"complete layer-pair coverage");for(uint8_t x:seen)need(x==1,"uncovered ordered layer pair");std::cout<<"ORDERED_LAYER_PAIRS "<<uint64_t(n)*n<<"\nPAIR_ORBITS "<<reps.size()<<"\nORBIT_CARDINALITY_SUM "<<orbit_sum<<"\nORBIT_HISTOGRAM";for(int s=1;s<=96;++s)if(orbit_hist[s])std::cout<<" "<<s<<":"<<orbit_hist[s];std::cout<<"\n";need(reps.size()==90179,"pair orbit count comparison");
 std::array<std::vector<uint8_t>,4096> independent;for(int m=0;m<4096;++m)for(int s=0;s<256;++s){bool ok=true;for(int e=0;e<12;++e)if(m&(1<<e)){auto[a,b]=q3.edges[e];if((s&(1<<a))&&(s&(1<<b))){ok=false;break;}}if(ok)independent[m].push_back(uint8_t(s));}
 std::array<std::array<uint8_t,8>,4096>degrees{};std::array<int,4096>ec{};for(int m:legal){ec[m]=__builtin_popcount(unsigned(m));for(int e=0;e<12;++e)if(m&(1<<e)){auto[a,b]=q3.edges[e];++degrees[m][a];++degrees[m][b];}}
 I maximum=-(I(1)<<126);U witness=0;uint64_t completions=0,processed=0,ties=0;std::array<uint64_t,33>edgehist{};for(auto[i,j]:reps){if(limit&&processed>=limit)break;int a=legal[i],b=legal[j];U base=U(a)|(U(b)<<12);U facebase[24];uint16_t vbase[16];for(int f=0;f<24;++f)facebase[f]=geom.ft[f][0][base&255]|geom.ft[f][1][(base>>8)&255]|geom.ft[f][2][(base>>16)&255];for(int v=0;v<16;++v)vbase[v]=geom.vt[v][0][base&255]|geom.vt[v][1][(base>>8)&255]|geom.vt[v][2][(base>>16)&255];for(int s:independent[a&b]){I z=I(in.lin[0])*(ec[a]+ec[b]+__builtin_popcount(unsigned(s)));for(int v=0;v<8;++v){int bit=(s>>v)&1;z+=in.lin[1+degrees[a][v]+bit];z+=in.lin[1+degrees[b][v]+bit];}for(int f=0;f<24;++f){U x=facebase[f]|geom.ft[f][3][s];int r=x&15;need(r<15,"enumeration root C4");z+=t.face[r][x>>4];}for(int v=0;v<16;++v){U x=vbase[v]|geom.vt[v][3][s];need(t.vlegal[x],"enumeration vertex C4");z+=t.vertex[x];}U mask=base|(U(s)<<24);if(z>maximum){maximum=z;witness=mask;ties=1;}else if(z==maximum){++ties;if(mask<witness)witness=mask;}++completions;++edgehist[ec[a]+ec[b]+__builtin_popcount(unsigned(s))];}++processed;}
 std::cout<<"PROCESSED_PAIR_ORBITS "<<processed<<"\nLEGAL_MARKED_COMPLETIONS "<<completions<<"\nEDGE_HISTOGRAM";for(int e=0;e<=32;++e)if(edgehist[e])std::cout<<" "<<e<<":"<<edgehist[e];std::cout<<"\n";if(!limit)need(completions==13150453,"marked completion count comparison");I gathered=literal_score(witness,in,t,geom);I literal=raw_literal_score(witness,in,t);need(gathered==maximum&&literal==maximum,"fast versus gathered versus raw literal witness score");need(common_neighbor_check(witness),"literal common-neighbor C4 test");auto aut4=isometries(q4);for(auto&h:aut4){U im=transform(witness,h);need(common_neighbor_check(im),"witness transported legality");need(raw_literal_score(im,in,t)==maximum,"Q4 isometry invariance on witness");}U comparison=3923956094u;need(common_neighbor_check(comparison),"comparison witness legality");I cscore=raw_literal_score(comparison,in,t);std::cout<<"EXACT_RAW_MAX "<<str(maximum)<<"\nWITNESS_MASK "<<witness<<"\nMAXIMIZING_MARKED_COMPLETIONS "<<ties<<"\nLITERAL_WITNESS_SCORE "<<str(literal)<<"\nLITERAL_COMMON_NEIGHBOR_CHECK PASS\nWITNESS_ALL_Q4_ISOMETRIES "<<aut4.size()<<" PASS\nCOMPARISON_WITNESS_MASK "<<comparison<<"\nCOMPARISON_WITNESS_RAW_SCORE "<<str(cscore)<<"\nRAW_MAX_COMPARISON_4924508303670 "<<(maximum==I(4924508303670LL)?"MATCH":"DIFFERENT")<<"\n";std::cout<<"WITNESS_EDGE_LIST";for(int e=0;e<32;++e)if(witness&(U(1)<<e))std::cout<<" "<<q4.edges[e].first<<"-"<<q4.edges[e].second;std::cout<<"\n";double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();std::cout<<"ELAPSED_SECONDS "<<seconds<<"\nSTATUS "<<(limit?"PARTIAL_COST_PROBE":"COMPLETE_LEGAL_Q4_MAXIMUM")<<"\n";return 0;}catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 1;}}
