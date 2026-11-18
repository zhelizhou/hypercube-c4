# Edge-root kernels pull back to full-face kernels exactly

This is a new Root derivation for the active whole-Q8 problem. It has not
received a fresh proof review. The edge author must check it before use.

An ambient root edge has retained state r=0 or1. A one-axis Q2 flag has
three bits: two endpoint connectors and the opposite edge. There are8
states if r=0 and7 if r=1. Average an edge kernel Q_r under the common
endpoint flip. At a Q4 root edge there are3 external flags s_a. Define

    T_edge(K) = (1/672) sum_(32 ambient root edges)
                    [6 sum_(3 unordered pairs a,b) Q_r(s_a,s_b)
                     + sum_(3 individual a) Q_r(s_a,s_a)].

At an actual Q8 root edge there are7 flags. Uniform restrictions give
E T_edge = (1/1024) sum_e x_e^T Q_r x_e /49. This follows from the
6/7 distinct-axis and1/7 collision probabilities. Hence PSD or full
integer-seven-count validity gives a nonnegative expectation.

Fix a root face F and one of its four edges e. Let s_0 be F viewed as a
one-axis flag at e. Every external full-face flag g gives a one-axis
flag s(g) at that same edge. In the appropriate edge state space set

    v_g = 6 e_{s(g)} + e_{s_0},
    V_(F,e) = the matrix with columns v_g.

For each full-face root type define

    P_F = sum_(four edges e of F) V_(F,e)^T Q_(r_e) V_(F,e).

Endpoint averaging makes this kernel invariant under the root D4
stabilizer. The exact pointwise identity on every legal labelled Q4 is

    T_face(P)(K) = 196 T_edge(Q)(K),

where T_face is the existing finite-eight face feature (no vertex term).
To verify the constant, fix one root edge of K. Its three incident root
faces select the three possible base external directions. Before the
factor1/(24*196), one base face contributes30 Q(s_a,s_b),6 Q(s_0,s_a),
6 Q(s_0,s_b),3 Q(s_a,s_a),3 Q(s_b,s_b),Q(s_0,s_0). Summing the three
base choices gives42 times every unordered cross pair and7 times every
diagonal. Division by24*196 yields (6 cross + diagonal)/672, as stated.
This calculation uses the existing 5/6 cross and1/12 diagonal law.

If both Q_r are PSD, every P_F is PSD. Thus edge PSD constraints are
already implied by the existing five full-face PSD blocks. Adding them
as separate blocks supplies no new relaxation strength.

If Q_r is only nonnegative on all nonnegative integer seven-count
vectors, P_F is nevertheless valid on all full-face six-count vectors.
Indeed for x>=0 integer, sum x=6,

    V_(F,e) x = 6 z_e,
    z_e = sum_g x_g e_{s(g)} + e_{s_0},
    z_e>=0 integer, sum z_e=7.

Therefore x^T P_F x =36 sum_e z_e^T Q_(r_e) z_e>=0. A new non-PSD
finite7 edge cut can supply another finite6 full-face cut beyond the
two presently found. It cannot be advertised as evidence that a new
PSD block escapes the fixed six-PSD-family obstruction.
