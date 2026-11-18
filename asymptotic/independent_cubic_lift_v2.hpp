// Exact signed-cubic reconstruction v2 (supports cyclic_AMGM, symmetric_cubic, slice_PSD, slice_COP).
// Uses the independently enumerated Q3 masks and geometric edge indices of the standalone checker.
struct CubicResult {
    int count = 0;
    int amgm_count = 0;
    int schur_count = 0;
    int slice_psd_count = 0;
    int slice_cop_count = 0;
    I collision = 0;
};

CubicResult add_cubics(const string& path, vector<I>& expected,
                       const int* type, const int* flag, const int* dims,
                       const int* off, const int ix3[8][8]) {
    ifstream file(path);
    string magic;
    int count = -1;
    file >> magic >> count;
    assert(file && (magic == "EDGE_CUBIC_V1" || magic == "EDGE_CUBIC_V2") && count >= 0 && count <= 20000);
    vector<vector<int>> masks(5);
    for (int h = 0; h < 4096; h++) if (type[h] >= 0) {
        assert(flag[h] == int(masks[type[h]].size()));
        masks[type[h]].push_back(h);
    }
    CubicResult result;
    for (int term = 0; term < count; term++) {
        int delta = -1, kind = -1;
        int64_t coefficient = -1;
        file >> delta >> kind >> coefficient;
        assert(file && delta >= 0 && delta <= 1 && kind >= 0 && kind <= 3 && coefficient >= 0 && coefficient < (int64_t(1) << 50));

        I W[8][8][8] = {};
        if (kind == 0 || kind == 1) {
            I f[3][8];
            for (auto& row : f) for (I& x : row) {
                int64_t v = -1;
                file >> v;
                assert(file && v >= 0 && v <= 65535);
                x = v;
            }
            if (delta == 1) for (auto& row : f) assert(row[7] == 0);
            auto unsym = [&](int i, int j, int k) -> I {
                if (kind == 0)
                    return f[0][i] * f[0][j] * f[1][k] + f[1][i] * f[1][j] * f[2][k] + f[2][i] * f[2][j] * f[0][k] - 3 * f[0][i] * f[1][j] * f[2][k];
                I value = 3 * f[0][i] * f[1][j] * f[2][k];
                for (int a = 0; a < 3; a++) {
                    value += f[a][i] * f[a][j] * f[a][k];
                    for (int b = 0; b < 3; b++) if (a != b) value -= f[a][i] * f[a][j] * f[b][k];
                }
                return value;
            };
            for (int i = 0; i < 8; i++) for (int j = 0; j < 8; j++) for (int k = 0; k < 8; k++)
                W[i][j][k] = unsym(i, j, k) + unsym(i, k, j) + unsym(j, i, k) + unsym(j, k, i) + unsym(k, i, j) + unsym(k, j, i);
            if (kind == 0) result.amgm_count++;
            else result.schur_count++;
        } else if (kind == 2) {
            // slice_PSD: P(c) = 6 * c_u * (v^T c)^2 >= 0 for all c in Z_{>=0}^{8-delta}
            int u = -1;
            file >> u;
            assert(file && u >= 0 && u < 8 - delta);
            I v[8];
            for (int i = 0; i < 8; i++) {
                int64_t val = 0;
                file >> val;
                assert(file && val >= -65535 && val <= 65535);
                v[i] = val;
            }
            if (delta == 1) assert(v[7] == 0);
            auto unsym = [&](int i, int j, int k) -> I {
                return (i == u) ? (v[j] * v[k]) : I(0);
            };
            for (int i = 0; i < 8; i++) for (int j = 0; j < 8; j++) for (int k = 0; k < 8; k++)
                W[i][j][k] = unsym(i, j, k) + unsym(i, k, j) + unsym(j, i, k) + unsym(j, k, i) + unsym(k, i, j) + unsym(k, j, i);
            result.slice_psd_count++;
        } else if (kind == 3) {
            // slice_COP: P(c) = 6 * c_u * (c^T Q_cop c) >= 0 where Q_cop is triangle-free COP on {0..7-delta}
            int u = -1, k_sz = 0, edge_count = 0;
            file >> u >> k_sz >> edge_count;
            assert(file && u >= 0 && u < 8 - delta && k_sz >= 1 && k_sz <= 8 - delta && edge_count >= 0 && edge_count <= k_sz * (k_sz - 1) / 2);
            vector<int> ids(k_sz);
            vector<int64_t> scale(k_sz);
            for (int& id : ids) {
                file >> id;
                assert(file && id >= 0 && id < 8 - delta);
            }
            for (int a = 0; a < k_sz; a++) for (int b = 0; b < a; b++) assert(ids[a] != ids[b]);
            for (auto& x : scale) {
                file >> x;
                assert(file && x >= 0 && x <= 65535);
            }
            vector<vector<unsigned char>> adj(k_sz, vector<unsigned char>(k_sz, 0));
            for (int e = 0; e < edge_count; e++) {
                int a = -1, b = -1;
                file >> a >> b;
                assert(file && a >= 0 && a < b && b < k_sz && !adj[a][b]);
                adj[a][b] = adj[b][a] = 1;
            }
            // Verify triangle-free property
            for (int a = 0; a < k_sz; a++) for (int b = 0; b < a; b++) if (adj[a][b])
                for (int c = 0; c < b; c++) assert(!(adj[a][c] && adj[b][c]));
            I qcop[8][8] = {};
            for (int a = 0; a < k_sz; a++) for (int b = 0; b < k_sz; b++)
                qcop[ids[a]][ids[b]] = I(1 - 2 * int(adj[a][b])) * scale[a] * scale[b];
            auto unsym = [&](int i, int j, int k) -> I {
                return (i == u) ? qcop[j][k] : I(0);
            };
            for (int i = 0; i < 8; i++) for (int j = 0; j < 8; j++) for (int k = 0; k < 8; k++)
                W[i][j][k] = unsym(i, j, k) + unsym(i, k, j) + unsym(j, i, k) + unsym(j, k, i) + unsym(k, i, j) + unsym(k, j, i);
            result.slice_cop_count++;
        }

        I collision = 0;
        for (int i = 0; i < 8 - delta; i++) for (int j = 0; j < 8 - delta; j++)
            collision = max(collision, W[i][i][j]);
        result.collision += 8 * I(coefficient) * collision;
        for (int t = 0; t < 5; t++) {
            assert(int(masks[t].size()) == dims[t]);
            for (int x = 0; x < 4; x++) for (int direction = 0; direction < 2; direction++) {
                int y = x ^ (1 << direction), other = 1 - direction;
                auto bit = [&](int h, int a, int b) { assert(ix3[a][b] >= 0); return (h >> ix3[a][b]) & 1; };
                int h0 = masks[t][0], root = bit(h0, x, y);
                int low = bit(h0, x, x ^ (1 << other)) + 2 * bit(h0, y, y ^ (1 << other)) + 4 * bit(h0, x ^ (1 << other), y ^ (1 << other));
                vector<int> extra;
                for (int h : masks[t]) {
                    assert(bit(h, x, y) == root);
                    assert(low == bit(h, x, x ^ (1 << other)) + 2 * bit(h, y, y ^ (1 << other)) + 4 * bit(h, x ^ (1 << other), y ^ (1 << other)));
                    int value = bit(h, x, x ^ 4) + 2 * bit(h, y, y ^ 4) + 4 * bit(h, x ^ 4, y ^ 4);
                    assert(root == 0 || value != 7);
                    extra.push_back(value);
                }
                if (root != delta) continue;
                assert(delta == 0 || low != 7);
                for (int a = 0; a < dims[t]; a++) for (int b = 0; b < dims[t]; b++)
                    expected[off[t] + a * dims[t] + b] += I(coefficient) * W[extra[a]][extra[b]][low];
            }
        }
        result.count++;
    }
    string trailing;
    assert(!(file >> trailing));
    return result;
}
