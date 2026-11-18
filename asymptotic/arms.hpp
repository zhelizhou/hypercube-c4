#pragma once
struct Attachments {
    struct Slice {u32 tab[4][256]{}; u32 operator()(u32 x)const{return tab[0][x&255]|tab[1][(x>>8)&255]|tab[2][(x>>16)&255]|tab[3][x>>24];}};
    array<array<Slice,2>,4> slice;
    vector<uint16_t> labels;
    Attachments(const vector<pair<int,int>>& edge_list):labels(1u<<20,65535) {
        for(int d=0;d<4;d++)for(int t=0;t<2;t++){
            auto &s=slice[d][t];
            auto drop=[&](int v){return (v&((1<<d)-1))|((v>>(d+1))<<d);};
            for(int b=0;b<32;b++){
                auto [x,y]=edge_list[b];int e=-1;
                if((x^y)==(1<<d))e=12+drop(x);
                else if((x>>d&1)==t)e=idx3[drop(x)][drop(y)];
                if(e<0)continue;
                for(int j=0;j<256;j++)if(j&(1<<(b%8)))s.tab[b/8][j]|=1u<<e;
            }
        }
        vector<array<uint16_t,4096>> trans3;vector<array<uint8_t,256>> trans8;
        array<int,3> p{0,1,2};vector<int> squares;
        for(int i=0;i<3;i++)for(int j=i+1;j<3;j++)for(int x=0;x<8;x++)if(!(x&((1<<i)|(1<<j)))){
            int a=x^(1<<i),b=x^(1<<j),c=a^(1<<j);squares.push_back((1<<idx3[x][a])|(1<<idx3[x][b])|(1<<idx3[a][c])|(1<<idx3[b][c]));
        }
        do{for(int shift=0;shift<8;shift++){
            int v[8];for(int x=0;x<8;x++){v[x]=shift;for(int k=0;k<3;k++)v[x]^=(x>>k&1)<<p[k];}
            array<uint16_t,4096> tr{};array<uint8_t,256> tv{};
            for(int m=1;m<4096;m++){auto[x,y]=edges3[countr_zero((u32)m)];tr[m]=tr[m&(m-1)]|(1<<idx3[v[x]][v[y]]);}
            for(int m=1;m<256;m++)tv[m]=tv[m&(m-1)]|(1<<v[countr_zero((u32)m)]);
            trans3.push_back(tr);trans8.push_back(tv);
        }}while(next_permutation(p.begin(),p.end()));
        vector<int> canon(4096,-1);int next=0;
        for(int h=0;h<4096;h++){
            if(any_of(squares.begin(),squares.end(),[&](int q){return (h&q)==q;}))continue;
            int mn=h;for(auto&t:trans3)mn=min<int>(mn,t[h]);if(mn==h)canon[h]=next++;
            for(int m=0;m<256;m++){int best=256;for(int j=0;j<48;j++)if(trans3[j][h]==mn)best=min<int>(best,trans8[j][m]);labels[h+(m<<12)]=canon[mn]*256+best;}
        }
        assert(next==99);
    }
    void unary(u32 h,uint16_t out[8])const{
        for(int d=0;d<4;d++)for(int t=0;t<2;t++){out[2*d+t]=labels[slice[d][t](h)];assert(out[2*d+t]!=65535);}
    }
    void keys(const u32 f[10],u32 out[40])const {
        int z=0;
        for(int i=0;i<10;i++)for(int j=i+1;j<10;j++)if(i/2!=j/2){
            int a=labels[slice[j/2-1][j&1](f[i])],b=labels[slice[i/2][i&1](f[j])];
            assert(a/256==b/256 && a!=65535);out[z++]=u32(min(a,b))*256+max(a,b)%256;
        }
        assert(z==40);
    }
};
