# Exact valid-row reconstruction and complete local maximization

This is a Root-authored mechanical interface, with actual replay on frozen B
enriched3. It has not yet received a fresh independent semantic audit. Its
current replay **fails** the sufficient strict-certificate criterion. The
upper682 Goal remains OPEN.

Run `reconstruct_exact_dual.py SCOPE NEW_OUTPUT` from the parent directory.
Neither solver optimality nor an accepted primal point is a premise. The
script rounds the equality multipliers and nonpositive inequality multipliers
to explicit rationals with denominator 10^9. It reconstructs each selected
integer PSD ray, integer rounding matrix, finite-count matrix and conditional
degree bias from the scientific parameters, preserving its actual positive
normalization. Every selected inequality multiplier has the valid sign.
Inactive weights may be zero. A final proof must establish the scope and
validity of every selected row; this numerical reconstruction does not replace
that obligation.

For the rounding rows, with even n equal to6 or28, integer q,t and total-n
integer counts x, the actual matrix is

    Qij=n² qi qj - (n/2)(2t+1)(qi+qj) + t(t+1).

Writing L=sum_i qi xi gives xᵀQx=n²(L-t)(L-t-1)>=0. This includes the vertex
total28 case directly, rather than claiming an earlier total6-only audit
implicitly proved it.

The full packed local coefficient vector includes the edge-to-face numerator
over784, the edge/vertex group-moment contribution7/2, and the edge3 lift over80.
The five ordinary degree-histogram coefficients and all finite alpha/beta
coefficients are also reconstructed as rational numbers from integer arrays.
All356 equalities use their actual row order and normalizations. Native sparse
exports are used only for a diagnostic comparison, not as the exact definition.

Let D be the common exact denominator. Round each exact packed kernel and
histogram numerator to a new integer query at scale T=10^9. For every legal Q4,
the folded face coefficients are nonnegative and sum to64512; independently,
the folded vertex coefficients are nonnegative and sum to64512. The former
follows from24 roots and (10+1+1)/288 per root. The latter follows from the
normalized total28 vertex moment. The raw five degree-histogram coordinates
are nonnegative and sum to16. Therefore a uniform exact bound is

    eps = max_face |NW/D-qW/T|
        + max_vertex |NW/D-qW/T|
        + (16/64512) max_hist |NH/D-qh/T|.

It applies to every legal Q4, including all columns outside the stored library.
Exact nearest-integer rounding bounds eps<=1/T+8/(64512T). No floating
reconstruction error or library-only maximum is used for this universal bound.

The independent complete oracle must then maximize the integer query over all
legal Q4. If its raw maximum is M, the exact local functional is at most
M/(64512T)+eps. Write delta=y.b, and compute exact maxima Amax/Bmax over the
complete case-specific finite alpha and beta domains. The sufficient criterion
is

    delta > M/(64512T)+eps+Amax+Bmax.

Separate maxima need not be individually nonpositive. For B enriched3, the
actual independent traversal covered13150453 marked completions and found
M=61473687284. The exact safe margin is

    -2826818780018833/3699376128000000000 < 0.

Hence that exact combination does not establish the desired contradiction.
Its legal maximizing Q4 mask2121429215 is a local missing column, not an actual
Q8 counterexample. The actual records, including one corrected executable-path
attempt, are in `B_enriched3_replay001/`. Later candidate combinations require
new output directories, actual full-domain maxima, and fresh independent
verification of the final assembled certificate.
