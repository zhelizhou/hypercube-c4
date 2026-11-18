"""Complete endpoint-averaged integer7 generators, exact CSR contract."""
from pathlib import Path
from itertools import combinations_with_replacement
from collections import Counter
import hashlib
import json
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'finite8_flags/deps'))
import numpy as np
from scipy import sparse
import edge_flags

ROW_ORDER = [(r, i, j) for r, d in enumerate((8, 7)) for i in range(d) for j in range(i, d)]


def pool_moment_numerators(graphs):
    """64xNgraph CSR, trueM upper entries=returned integers/129024.

    Same originallambda must be used on these columns and parent constraints.
    This is not the packed linearQ coefficient convention off diagonal.
    """
    row_index = {tuple(row): k for k, row in enumerate(ROW_ORDER)}
    rows, columns, values = [], [], []
    for column, graph in enumerate(graphs):
        coeff = edge_flags.local_coefficients(edge_flags.from_mask(int(graph)))
        for (r, i, j), value in coeff.items():
            rows.append(row_index[r, i, j])
            columns.append(column)
            values.append(value * (2 if i == j else 1))
    return sparse.csr_matrix((np.asarray(values, dtype=np.int32), (rows, columns)), shape=(64, len(graphs)))


def main():
    ri = {tuple(row): k for k, row in enumerate(ROW_ORDER)}
    rows, columns, values, histograms = [], [], [], []
    counts = []
    for root, d in enumerate((8, 7)):
        before = len(histograms)
        for multiset in combinations_with_replacement(range(d), 7):
            c = Counter(multiset)
            x = [c.get(i, 0) for i in range(d)]
            column = len(histograms)
            histograms.append({'root_retained': root, 'counts': x})
            ordered_mass = 0
            for i in range(d):
                for j in range(i, d):
                    numerator = x[i] * x[j] + x[edge_flags.flip(i)] * x[edge_flags.flip(j)]
                    ordered_mass += numerator * (1 if i == j else 2)
                    if numerator:
                        rows.append(ri[root, i, j])
                        columns.append(column)
                        values.append(numerator)
            assert ordered_mass == 98
        counts.append(len(histograms) - before)
    assert counts == [3432, 1716]
    G = sparse.csr_matrix((np.asarray(values, dtype=np.int32), (rows, columns)), shape=(64, 5148))
    sparse.save_npz(HERE / 'GENERATOR_NUMERATOR.npz', G)
    sparse.save_npz(HERE / 'GENERATOR_NORMALIZED.npz', G.astype(float) / 98)
    csr = {'shape': list(G.shape), 'denominator': 98, 'indptr': G.indptr.tolist(), 'indices': G.indices.tolist(), 'data': G.data.tolist()}
    (HERE / 'GENERATOR_CSR_INTEGER.json').write_text(json.dumps(csr, separators=(',', ':')) + '\n')
    (HERE / 'GENERATOR_HISTOGRAMS.json').write_text(json.dumps(histograms, separators=(',', ':')) + '\n')
    interface = {
        'scope': 'Complete necessary integer7 frequencycones under commonendpoint C2, samegraphlambda. NoPSD orgraphrealization claim.',
        'generator_shape': [64, 5148], 'generator_counts_missing_retained': counts,
        'row_order': ROW_ORDER, 'column_order': 'All3432 missingroot weakcompositions first, then1716 retainedroot; lexicographic multisetof7 labels.',
        'generator': 'H_x=(xxT+Pflip xxT PflipT)/98; CSR valuesstore integernumerator, fullnormalized NPZ also included.',
        'root_column_ranges_halfopen': [[0, 3432], [3432, 5148]],
        'local_moment': 'pool_moment_numerators(graphs) returns64xN integerCSR U; trueM_upper=U/(2*64512)=U/129024. Diag=2packedlinearcoefficient; offdiag=packedlinearcoefficient.',
        'same_lambda_equation': '(U/129024) @ lambda == (GENERATOR_NUMERATOR/98) @ beta, beta>=0; keep sameoriginal lambda in everyparent constraint.',
        'mass': 'Diagonal+2offdiagonal sumof eachgenerator=1; sum beta_perroot=ambientroottypeprobability, automatically.',
        'generator_nnz': int(G.nnz), 'coverage': 'Noorbitreduction used; every3432+1716 rawinteger7 histogram included.',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    (HERE / 'GENERATOR_INTERFACE.json').write_text(json.dumps(interface, indent=2) + '\n')
    print(json.dumps(interface, indent=2))


if __name__ == '__main__':
    main()
