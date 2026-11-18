// Independent completeness proof by labelled counting and orbit-stabilizer.
// Inputs: only the proposed sorted Q4 representative list. No normalizer tables.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;
vector<pair<int,int>> cube_edges(int d) {
    vector<pair<int,int>> e;
    for(int j=0;j<d;j++) for(int x=0;x<(1<<d);x++)
        if(!(x&(1<<j))) e.emplace_back(x,x^(1<<j));
    return e;
}
int main(int argc,char**argv) {
    if(argc!=2) {cerr<<"usage: verify_completeness full_masks.bin\n";return 2;}
    ifstream input(argv[1],ios::binary|ios::ate);
    if(!input) throw runtime_error("cannot open mask list");
    auto bytes=input.tellg(); assert(bytes>=0 && bytes%4==0);
    vector<uint32_t> masks(bytes/4); input.seekg(0);
    input.read(reinterpret_cast<char*>(masks.data()),bytes); assert(input);
    auto e3=cube_edges(3); array<pair<int,int>,32> e4;
    for(int x=0;x<8;x++) e4[x]={2*x,2*x+1};
    for(int e=0;e<12;e++) {
        auto[x,y]=e3[e];e4[20+e]={2*x,2*y};e4[8+e]={2*x+1,2*y+1};
    }
    int i3[8][8],i4[16][16];
    for(auto&row:i3) fill(begin(row),end(row),-1);
    for(auto&row:i4) fill(begin(row),end(row),-1);
    for(int e=0;e<12;e++){auto[x,y]=e3[e];i3[x][y]=i3[y][x]=e;}
    for(int e=0;e<32;e++){auto[x,y]=e4[e];i4[x][y]=i4[y][x]=e;}
    auto squares=[&](int d,auto&ix){
        vector<uint32_t> out;
        for(int a=0;a<d;a++)for(int b=a+1;b<d;b++)for(int x=0;x<(1<<d);x++)
            if(!(x&((1<<a)|(1<<b)))) {
                int y=x^(1<<a),z=x^(1<<b),w=y^(1<<b);
                out.push_back((uint32_t(1)<<ix[x][y])|(uint32_t(1)<<ix[x][z])|
                              (uint32_t(1)<<ix[y][w])|(uint32_t(1)<<ix[z][w]));
            }
        return out;
    };
    auto sq3=squares(3,i3),sq4=squares(4,i4);
    vector<int> layers;
    for(int h=0;h<4096;h++) {
        bool valid=true;for(auto s:sq3)if((h&s)==s){valid=false;break;}
        if(valid)layers.push_back(h);
    }
    assert(layers.size()==2902);
    uint16_t independent_count[4096]={};
    for(int h=0;h<4096;h++)for(int c=0;c<256;c++) {
        bool valid=true;
        for(int e=0;e<12;e++)if(h&(1<<e)) {
            auto[x,y]=e3[e];if((c&(1<<x))&&(c&(1<<y))){valid=false;break;}
        }
        if(valid)independent_count[h]++;
    }
    uint64_t labelled_count=0;
    for(int a:layers)for(int b:layers) labelled_count+=independent_count[a&b];
    using Lookup=array<array<uint32_t,256>,4>;
    vector<Lookup> transforms;
    array<int,4> permutation={0,1,2,3};
    do {
        for(int shift=0;shift<16;shift++) {
            int vm[16];for(int x=0;x<16;x++) {
                vm[x]=shift;for(int j=0;j<4;j++)vm[x]^=((x>>j)&1)<<permutation[j];
            }
            Lookup lut{};
            for(int e=0;e<32;e++) {
                auto[x,y]=e4[e];int image=i4[vm[x]][vm[y]];assert(image>=0);
                for(int value=0;value<256;value++)if(value&(1<<(e%8)))
                    lut[e/8][value]|=uint32_t(1)<<image;
            }
            transforms.push_back(lut);
        }
    }while(next_permutation(permutation.begin(),permutation.end()));
    assert(transforms.size()==384);
    uint64_t orbit_sum=0;
    for(size_t k=0;k<masks.size();k++) {
        uint32_t h=masks[k];if(k)assert(h>masks[k-1]);
        for(auto s:sq4)assert((h&s)!=s);
        unsigned stabilizer=0;
        for(const auto&lut:transforms) {
            uint32_t image=lut[0][h&255]|lut[1][(h>>8)&255]|
                           lut[2][(h>>16)&255]|lut[3][h>>24];
            // Distinct sorted minimal representatives have disjoint orbits.
            assert(image>=h);if(image==h)stabilizer++;
        }
        assert(stabilizer && 384%stabilizer==0);orbit_sum+=384/stabilizer;
    }
    assert(orbit_sum==labelled_count);
    cout<<"{\"status\":\"PASS\",\"representatives\":"<<masks.size()
        <<",\"cube_isometries_per_representative\":384,\"labelled_graphs_direct\":"
        <<labelled_count<<",\"sum_of_disjoint_orbit_sizes\":"<<orbit_sum
        <<",\"completeness_proved_by_counting\":true}\n";
}
