# All edge-three-flag counts lie in the existing full-face quadratic span

Fix the existing common-Q4 encoding, root-preserving five face blocks(240,212,190,187,170), folded upper coefficients c/64512 and nine-state vertex block. We prove a pointwise identity on EVERY legal Q4, not a positivity statement about its local moment matrices. No PSD assumption is used. The resulting kernels generally have signed entries and are not asserted PSD.

For a root ambient edge e of a Q4, its other three directions give three edge-flag states s=(first connector,second connector,opposite edge). For retention r there are8−r labels. For each integer histogram z of three labels let L_(r,z)(K) count the ambient roots whose three-flag histogram is z, counting both endpoint orientations. There are204 rows:120 for r0 and84 for r1, in lexicographic multiset order. The sum of their counts on K is64.

For a canonical root square R and full flag states i,j on its two outside directions, define A_z(i,j) as follows. Sum over all four edges e of R. The remaining direction in R gives e's base flag b_e, determined by R's other three edge bits. The two full outside flags i,j determine e's two other edge-flag labels a_e(i),a_e(j): their endpoint connector bits and their translated copy of e. Add1 if(b_e,a_e(i),a_e(j)) has histogram z; also add1 for the endpoint-reversed three labels, using flip(s)=((s&1)<<1)|((s&2)>>1)|(s&4). Include the edge retention in the row key.

A_z is symmetric in i,j. Every edge datum used is present in the root square and the two full outside flags. Both-orientation counting makes the summand independent of root-edge orientation. Summing the four root edges makes A_z invariant under the simultaneous root stabilizer on the two full flags. Thus it defines a kernel in the EXISTING five full-state blocks; separate normalization of the two flags is neither needed nor allowed. The diagonal A_z(i,i) is defined by the same formula, even though the two external observations then coincide.

For a fixed actual Q4, choose each root face F and its two actual outside flags i_F,j_F. Each ambient root edge of K is in exactly three root faces, one for each choice of a base outside direction. Each such choice observes the same three edge flags. Hence

    L_z(K)=(1/3) Σ_(24 faces F) A_z(i_F,j_F).              (1)

The exact finite-eight functional for an invariant face kernel Q is, directly from the existing folded coefficient convention,

    T_Q(K)=Σ_(b,i<=j)c_(b,i,j)(K)Q_(b,i,j)/64512
          =(1/288) Σ_F [10Q(i_F,j_F)+Q(i_F,i_F)+Q(j_F,j_F)]. (2)

The collision terms in(2) are essential. Set the integer symmetric kernel

    K_z(i,j)=12 A_z(i,j)−A_z(i,i)−A_z(j,j).

Its diagonal is10A_z(i,i), so

    10K_z(i,j)+K_z(i,i)+K_z(j,j)=120 A_z(i,j).

Combining(1) and(2) gives

    T_(K_z)(K)=(5/12)Σ_F A_z(i_F,j_F)=(5/4)L_z(K),

or the pointwise integer identity

    5·64512·L_z(K)=4 Σ_(b,i<=j)c_(b,i,j)(K)K_(z,b,i,j).   (3)

The vertex-block coefficients of K_z are zero. Thus arbitrary linear combinations of all204 L rows are covered by the existing full-Q4 oracle on the same six quadratic blocks. No arbitrary-tensor extension is necessary for this particular family. For an equation normalized as Eλ L_z/64−Eβ H_z/70=0, a dual multiplier y_z contributes original packed quadratic weights K_z*y_z/80, since L_z/64=T_(K_z)/80.

As a normalization check, summing all204 row indicators gives A=8 on every valid full-state pair: four root edges, two orientations each. Therefore Σ_z K_z is the constant80 kernel in all five face blocks. Its score is80 because total face moment mass is1. Formula(3) then gives total L=(4/5)80=64, as required.

The implementation builds all204 integer kernels using only the original root-square edges, root masks and full-state order. It compares the original packed feature score against independently counted literal edge-three histograms of every one of the14090 current actual Q4 graph columns. Every one of the2,874,360 integer residuals in(3) is exactly zero. This is a complete check on that stored library; the universal coverage of(3) is the preceding pointwise combinatorial proof, not a claim that the library classifies all Q4s. CHECK_RESULT.json binds actual scripts/data hashes. Root separately derived the same collision cancellation and is reviewing the lift with the edge3 sampling bridge.

For the parent global bridge, H_z(y) counts all35 triples among the seven edge flags, with both endpoint orientations. Counting the same ambient-edge/three-other-directions objects in an actual Q8 gives Σ_(1120 slices)L_z=Σ_(1024 edges)H_z. Therefore 35 EλL_z=32 EβH_z, equivalently EλL_z/64=EβH_z/70. These observations must use the same actual lambda and beta. The identity holds at any m; the parent uses its separate maximal-counterexample cover, degree constraints and other valid kernels. A numerical pool dual, integer local score, or this span identity alone does not prove the original upper682 theorem.
