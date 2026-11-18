// Standalone exact checker v2: reconstructs embeddings directly, verifies PSD + triangle-free COP +
// signed edge-cubics (AMGM, Schur, Slice-PSD, Slice-COP), and optionally writes exact per-degree-profile maxima.
#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
using I = __int128_t;

template<class T> vector<T> read(const string& p) {
    ifstream f(p, ios::binary | ios::ate);
    if (!f) throw runtime_error("read " + p);
    auto n = f.tellg();
    assert(n % sizeof(T) == 0);
    vector<T> a(n / sizeof(T));
    f.seekg(0);
    f.read(reinterpret_cast<char*>(a.data()), n);
    return a;
}

string dec(I n) {
    if (!n) return "0";
    bool sign = n < 0;
    if (sign) n = -n;
    string s;
    while (n) { s.push_back('0' + n % 10); n /= 10; }
    if (sign) s.push_back('-');
    reverse(s.begin(), s.end());
    return s;
}

vector<pair<int, int>> edges(int d) {
    vector<pair<int, int>> e;
    for (int j = 0; j < d; j++)
        for (int x = 0; x < (1 << d); x++)
            if (!(x & (1 << j))) e.emplace_back(x, x ^ (1 << j));
    return e;
}

struct Extract {
    array<array<uint16_t, 256>, 4> tab{};
    uint16_t operator()(uint32_t h) const {
        return tab[0][h & 255] | tab[1][(h >> 8) & 255] | tab[2][(h >> 16) & 255] | tab[3][h >> 24];
    }
};

#include "independent_cubic_lift_v2.hpp"

int main(int argc, char** argv) {
    if (argc < 7) {
        cerr << "Usage: full_masks.bin q_int64.bin factors_int64.bin denominator_exponent cop_terms_general.txt cubic_terms.txt [profiles_out.tsv]\n";
        return 2;
    }
    auto masks = read<uint32_t>(argv[1]);
    auto q = read<I>(argv[2]); auto r = read<int64_t>(argv[3]);
    int exponent = stoi(argv[4]);
    assert(exponent >= 0 && exponent <= 90);
    I den = I(1) << exponent;

    auto e2 = edges(2), e3 = edges(3);
    array<pair<int, int>, 32> e4;
    for (int x = 0; x < 8; x++) e4[x] = {2 * x, 2 * x + 1};
    for (int j = 0; j < 12; j++) {
        auto [x, y] = e3[j];
        e4[20 + j] = {2 * x, 2 * y};
        e4[8 + j] = {2 * x + 1, 2 * y + 1};
    }
    int ix2[4][4], ix3[8][8], ix4[16][16];
    for (auto& row : ix2) fill(row, row + 4, -1);
    for (auto& row : ix3) fill(row, row + 8, -1);
    for (auto& row : ix4) fill(row, row + 16, -1);
    for (int j = 0; j < 4; j++) { auto [x, y] = e2[j]; ix2[x][y] = ix2[y][x] = j; }
    for (int j = 0; j < 12; j++) { auto [x, y] = e3[j]; ix3[x][y] = ix3[y][x] = j; }
    for (int j = 0; j < 32; j++) { auto [x, y] = e4[j]; ix4[x][y] = ix4[y][x] = j; }

    uint32_t v_inc_mask[16] = {};
    for (int j = 0; j < 32; j++) {
        auto [x, y] = e4[j];
        v_inc_mask[x] |= (1u << j);
        v_inc_mask[y] |= (1u << j);
    }

    int canon2[16], aut2[16] = {};
    for (int h = 0; h < 16; h++) {
        canon2[h] = 100;
        for (int sw = 0; sw < 2; sw++) for (int shift = 0; shift < 4; shift++) {
            int vm[4];
            for (int x = 0; x < 4; x++) vm[x] = (sw ? ((x & 1) << 1) | ((x >> 1) & 1) : x) ^ shift;
            int z = 0;
            for (int j = 0; j < 4; j++) { auto [x, y] = e2[j]; z |= ((h >> j) & 1) << ix2[vm[x]][vm[y]]; }
            canon2[h] = min(canon2[h], z);
            if (z == h) aut2[h]++;
        }
    }
    vector<int> roots;
    for (int h = 0; h < 15; h++) if (canon2[h] == h) roots.push_back(h);
    assert(roots == vector<int>({0, 1, 3, 5, 7}));

    vector<int> square3;
    for (int j = 0; j < 3; j++) for (int k = j + 1; k < 3; k++) for (int x = 0; x < 8; x++) if (!(x & ((1 << j) | (1 << k)))) {
        int a = x ^ (1 << j), b = x ^ (1 << k), c = a ^ (1 << k);
        square3.push_back((1 << ix3[x][a]) | (1 << ix3[x][b]) | (1 << ix3[a][c]) | (1 << ix3[b][c]));
    }
    int type[4096], flag[4096], dims[6] = {}, off[7] = {};
    fill(type, type + 4096, -1);
    for (int h = 0; h < 4096; h++) {
        bool ok = true;
        for (int sq : square3) if ((h & sq) == sq) { ok = false; break; }
        if (!ok) continue;
        int root = (h & 1) | ((h >> 0) & 2) | ((h >> 2) & 4) | ((h >> 2) & 8);
        auto at = find(roots.begin(), roots.end(), root);
        if (at == roots.end()) continue;
        int t = at - roots.begin();
        type[h] = t;
        flag[h] = dims[t]++;
    }
    int vflag[16];
    vector<int> vlist;
    for (int h = 0; h < 15; h++) {
        int swapped = ((h & 3) << 2) | ((h >> 2) & 3), canonical = min(h, swapped);
        auto at = find(vlist.begin(), vlist.end(), canonical);
        if (at == vlist.end()) { vlist.push_back(canonical); vflag[h] = vlist.size() - 1; }
        else vflag[h] = at - vlist.begin();
    }
    assert(vlist.size() == 9);
    dims[5] = 9;
    for (int t = 0; t < 6; t++) off[t + 1] = off[t] + dims[t] * dims[t];
    assert(vector<int>(dims, dims + 6) == vector<int>({240, 212, 187, 190, 170, 9}));
    assert(q.size() == size_t(off[6]) && r.size() == q.size());
    for (int64_t x : r) assert(x > -(int64_t(1) << 50) && x < (int64_t(1) << 50));

    vector<I> expected(q.size());
    for (int t = 0; t < 6; t++) for (int a = 0; a < dims[t]; a++) for (int b = 0; b < dims[t]; b++) {
        I sum = 0;
        for (int k = 0; k < dims[t]; k++) sum += I(r[off[t] + a * dims[t] + k]) * r[off[t] + b * dims[t] + k];
        expected[off[t] + a * dims[t] + b] = sum;
    }

    int cop_terms_checked = 0, largest_graph_order = 0;
    {
        ifstream terms(argv[5]);
        assert(terms);
        string magic;
        terms >> magic;
        assert(terms && magic == "TRIANGLEFREE_COP_V1");
        int count = 0;
        terms >> count;
        assert(terms && count >= 0 && count <= 100000);
        for (int term = 0; term < count; term++) {
            int t = -1, k = 0, edge_count = 0;
            terms >> t >> k >> edge_count;
            assert(terms && t >= 0 && t < 6 && k >= 1 && k <= dims[t] && edge_count >= 0 && edge_count <= k * (k - 1) / 2);
            vector<int> ids(k);
            vector<int64_t> scale(k);
            for (int& id : ids) { terms >> id; assert(terms && id >= 0 && id < dims[t]); }
            for (int a = 0; a < k; a++) for (int b = 0; b < a; b++) assert(ids[a] != ids[b]);
            for (auto& x : scale) { terms >> x; assert(terms && x >= 0 && x < (int64_t(1) << 50)); }
            vector<vector<unsigned char>> adj(k, vector<unsigned char>(k, 0));
            for (int e = 0; e < edge_count; e++) {
                int a = -1, b = -1;
                terms >> a >> b;
                assert(terms && a >= 0 && a < b && b < k && !adj[a][b]);
                adj[a][b] = adj[b][a] = 1;
            }
            for (int a = 0; a < k; a++) for (int b = 0; b < a; b++) if (adj[a][b])
                for (int c = 0; c < b; c++) assert(!(adj[a][c] && adj[b][c]));
            for (int a = 0; a < k; a++) for (int b = 0; b < k; b++)
                expected[off[t] + ids[a] * dims[t] + ids[b]] += I(1 - 2 * int(adj[a][b])) * scale[a] * scale[b];
            cop_terms_checked++;
            largest_graph_order = max(largest_graph_order, k);
        }
        string trailing;
        assert(!(terms >> trailing));
    }

    I df = 0, dv = 0;
    for (int t = 0; t < 6; t++) for (int a = 0; a < dims[t]; a++) {
        I value = expected[off[t] + a * dims[t] + a];
        if (t < 5) df = max(df, value);
        else dv = max(dv, value);
    }

    auto cubic = add_cubics(argv[6], expected, type, flag, dims, off, ix3);
    for (size_t j = 0; j < q.size(); j++) assert(expected[j] == q[j]);

    auto make_extract = [&](const vector<pair<int, int>>& es, auto lift) {
        Extract out;
        for (int bit = 0; bit < int(es.size()); bit++) {
            auto [a, b] = es[bit];
            int old = ix4[lift(a)][lift(b)];
            assert(old >= 0);
            for (int byte = 0; byte < 256; byte++)
                if (byte & (1 << (old % 8))) out.tab[old / 8][byte] |= 1 << bit;
        }
        return out;
    };
    vector<pair<Extract, Extract>> fs;
    for (int a = 0; a < 4; a++) for (int b = a + 1; b < 4; b++) {
        int c = -1, d = -1;
        for (int k = 0; k < 4; k++) if (k != a && k != b) { if (c < 0) c = k; else d = k; }
        for (int bc = 0; bc < 2; bc++) for (int bd = 0; bd < 2; bd++)
            for (int sw = 0; sw < 2; sw++) for (int ra = 0; ra < 2; ra++) for (int rb = 0; rb < 2; rb++) {
                auto build = [&](int ext, int fix, int be, int bf) {
                    return make_extract(e3, [&](int x) {
                        int xa = (x >> (sw ? 1 : 0)) & 1, xb = (x >> (sw ? 0 : 1)) & 1, xe = (x >> 2) & 1;
                        return ((xa ^ ra) << a) | ((xb ^ rb) << b) | ((xe ^ be) << ext) | (bf << fix);
                    });
                };
                fs.emplace_back(build(c, d, bc, bd), build(d, c, bd, bc));
            }
    }
    assert(fs.size() == 192);
    vector<Extract> vs;
    for (int x = 0; x < 16; x++) for (int a = 0; a < 4; a++) for (int b = a + 1; b < 4; b++)
        vs.push_back(make_extract(e2, [&](int y) { return x ^ ((y & 1) << a) ^ (((y >> 1) & 1) << b); }));
    int vpairs[3][2] = {{0, 5}, {1, 4}, {2, 3}};

    I maximum = -(I(1) << 125), second = maximum;
    uint32_t arg = 0, second_arg = 0;
    uint64_t square_checks = 0;
    vector<uint32_t> sq4;
    for (int a = 0; a < 4; a++) for (int b = a + 1; b < 4; b++) for (int x = 0; x < 16; x++) if (!(x & ((1 << a) | (1 << b)))) {
        int y = x ^ (1 << a), z = x ^ (1 << b), w = y ^ (1 << b);
        sq4.push_back((uint32_t(1) << ix4[x][y]) | (uint32_t(1) << ix4[x][z]) | (uint32_t(1) << ix4[y][w]) | (uint32_t(1) << ix4[z][w]));
    }

    struct ProfInfo { I max_num; uint32_t best_id; uint64_t count; };
    map<array<int, 5>, ProfInfo> profiles;
    bool write_profiles = (argc >= 8);

    ofstream dump("scaled_scores.bin",ios::binary);
    for (uint32_t h = 0; h < masks.size(); h++) {
        uint32_t mask = masks[h];
        if (h) assert(masks[h] > masks[h - 1]);
        for (uint32_t sq : sq4) { assert((mask & sq) != sq); square_checks++; }
        I numerator = I(popcount(mask)) * 6 * den;
        int normalization = 0;
        for (auto& [ea, eb] : fs) {
            int fa = ea(mask), t = type[fa];
            if (t < 0) continue;
            int fb = eb(mask);
            assert(type[fb] == t);
            int weight = 8 / aut2[roots[t]];
            normalization += weight;
            numerator += I(weight) * q[off[t] + flag[fa] * dims[t] + flag[fb]];
        }
        assert(normalization == 192);
        for (int x = 0; x < 16; x++) for (auto& pair : vpairs) {
            int a = vs[6 * x + pair[0]](mask), b = vs[6 * x + pair[1]](mask);
            assert(a != 15 && b != 15);
            numerator += I(4) * q[off[5] + vflag[a] * 9 + vflag[b]];
        }
        I common=192*den;
        I scaled=numerator*70368744177664LL;
        I ceiling=scaled/common+(scaled%common>0);
        assert(ceiling>-(I(1)<<60) && ceiling<(I(1)<<60));
        int64_t entry=ceiling;
        dump.write(reinterpret_cast<const char*>(&entry),sizeof(entry));
        if (numerator > maximum) { second = maximum; second_arg = arg; maximum = numerator; arg = h; }
        else if (numerator > second) { second = numerator; second_arg = h; }

        if (write_profiles) {
            array<int, 5> hist = {0, 0, 0, 0, 0};
            for (int v = 0; v < 16; v++) {
                int deg = popcount(mask & v_inc_mask[v]);
                hist[deg]++;
            }
            auto it = profiles.find(hist);
            if (it == profiles.end()) profiles[hist] = {numerator, h, 1};
            else {
                it->second.count++;
                if (numerator > it->second.max_num) {
                    it->second.max_num = numerator;
                    it->second.best_id = h;
                }
            }
        }
    }

    if (write_profiles) {
        ofstream pf(argv[7]);
        pf << dec(192 * den) << "\t" << dec(maximum) << "\n";
        for (auto& [hist, info] : profiles) {
            pf << hist[0] << "\t" << hist[1] << "\t" << hist[2] << "\t" << hist[3] << "\t" << hist[4]
               << "\t" << dec(info.max_num) << "\t" << info.best_id << "\t" << info.count << "\n";
        }
    }

    cout << "{\"status\":\"PASS\",\"independent_geometry\":true"
         << ",\"copositive_trianglefree_graphs_verified\":true,\"COP_terms_checked\":" << cop_terms_checked
         << ",\"largest_COP_graph_order\":" << largest_graph_order
         << ",\"integer_PSD_base_Gram_verified\":true"
         << ",\"matrix_component_decomposition_verified\":true"
         << ",\"signed_cubic_decomposition_verified\":true"
         << ",\"cubic_terms_checked\":" << cubic.count
         << ",\"cubic_breakdown\":{\"cyclic_AMGM\":" << cubic.amgm_count
         << ",\"symmetric_cubic\":" << cubic.schur_count
         << ",\"slice_PSD\":" << cubic.slice_psd_count
         << ",\"slice_COP\":" << cubic.slice_cop_count << "}"
         << ",\"D_cubic_numerator\":\"" << dec(cubic.collision)
         << "\",\"D_face_numerator\":\"" << dec(df)
         << "\",\"D_vertex_numerator\":\"" << dec(dv)
         << "\",\"graphs_checked\":" << masks.size()
         << ",\"square_checks\":" << square_checks
         << ",\"maximum_numerator\":\"" << dec(maximum)
         << "\",\"common_denominator\":\"" << dec(192 * den)
         << "\",\"maximizing_id\":" << arg << ",\"maximizing_mask\":" << masks[arg]
         << ",\"second_maximum_numerator\":\"" << dec(second)
         << "\",\"second_maximizing_id\":" << second_arg << "}\n";
    return 0;
}
