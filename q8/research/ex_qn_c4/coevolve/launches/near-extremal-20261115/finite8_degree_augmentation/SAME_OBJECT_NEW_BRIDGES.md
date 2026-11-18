# Two actual same-object additions

These are local necessities used by the current maximal-counterexample relaxation. They do not constitute a full Q8 bound. The worker's arithmetic reconstruction/calibration is separate from Root's pending fresh semantic audits of the new modules.

For maximal C4-free H⊆Q8 and a vertex v of global degree d, let x be its28 coordinate-Q2 histogram in the fixed nine rooted states. State ID8 is the canonical class of codes13/14 in edge order(01,02,13,23). It has exactly one root-incident edge missing and the other three edges retained. Every missing edge v(v+e_j) must close a C4 upon addition, since H is maximal; this requires some retained direction i and hence a Q2(i,j) of ID8 at v. That square's unique missing root edge determines j, so witnesses selected for different missing directions are distinct. Therefore x8≥8−d. A maximal graph has no degree-zero vertex, since a new edge at an isolated vertex could not close a C4.

The root-incidence groups are I0=(0,3,7), I1=(1,4,5,8), I2=(2,6), with histogram totals F0(d)=C(8−d,2), F1(d)=d(8−d), F2(d)=C(d,2). Subtracting8−d from x8 leaves a free I1 total(d−1)(8−d). For d1..8 the numbers of unrestricted integer histograms under these exact totals and this necessary lower bound are

253,22848,75504,89180,50050,13728,1848,29,

summing to253440; the d0 domain is empty. These are necessary frequency domains, not actual global graph classifications. An integer Q9/B kernel verified on this restricted domain is MAXIMAL_ONLY. Existing kernels verified on the larger674172 domains remain valid. Root's independent specific checker verifies every new parameter and its exact pairing before the LP consumes it; bounded NoCut is not cone membership. Root's structural proof and fresh-review status remain separately tracked.

For the edge–vertex bridge, each ambient edge has retention r and seven flag counts y_s. In the fixed edge-flag code s=(a,b,c), its endpoint global degrees are r+Σa y_s and r+Σb y_s. The corresponding vertex-rooted Q2 codes are r+2a+4b+8c and r+2b+4a+8c. Canonicalizing only by the common root-direction transposition gives one of the same nine vertex states. C[r,d,j] counts, over both endpoints and all seven flags, endpoint degree d and vertex state j. This is an integer function of the SAME histogram y; its sum is14. Reversing endpoints preserves C, and every current raw-to-dedup class was checked to preserve all162 coordinates.

For a mixed vertex state j∈I1, each(v,Q2) of degree d is seen once through its retained incident edge and once through its missing incident edge. Therefore C[1,d,j]β−C[0,d,j]β=0 for all9×4 rows. This conditioning is on the actual global endpoint degree, not on a local-Q4 degree. Dropping d would lose the newly retained information.

Let x_vi denote the28-Q2 counts at vertex v. Since beta is normalized over1024 ambient edges, summing both edge retention types counts every(v,Q2) twice:

Σ_r C[r,d,i]β = (1/512) Σ_{v:deg(v)=d} x_vi.

Define B[g,i]β=Σ_d F_g(d) Σ_r C[r,d,i]β. Since Σ_{j∈I_g}x_vj=F_g(deg(v)) and the actual vertex moment is M5=(1/(256·784))Σ_v x_v x_vᵀ,

B[g,i]β=392 Σ_{j∈I_g} M5_ij.

Under the reviewed common-Q4 bridge, M5=E_lambda M5(K). For the existing packed upper coefficients c/64512, let W[g,i] have coefficient2 on c_ii when i∈I_g and coefficient1 on c_min(i,j),max(i,j) for j∈I_g,j≠i. Thus Wc=2·64512 Σ_{j∈I_g}M5_ij(K), and the exact integer equality is

2304 Bβ = 7 W F_vertexᵀ λ.

There are27 such rows; together with the36 mixed balance rows these are63 supplied equations, without a claim of linear independence. They hold for any actual C4-free Q8, irrespective of m or maximality. The current1751 beta domain is maximal/leaf-filtered for the separate counterexample-cover caller. No local Q4 column is required to be maximal, and the full oracle still scans all legal common Q4 slices.

The consumer independently reconstructed all1751 C columns, checked all3432 raw histogram dedup groups, and exactly matched the supplied balance,B,W matrices. For the same actual682 seed, the1024 integer beta counts satisfy every balance row exactly. Its1120 true Q4-slice integer packed sum satisfies WΣc=360 B beta_counts exactly, equivalent to the normalized27 equations. The actual682 graph is a calibration outside the683..688 alpha cover. Inputs, order and checks are frozen under pool_profile1409_vertex_priced/edge_vertex_bridge_inputs and SCOPE_INCREMENT_002_EDGE_VERTEX.json.
