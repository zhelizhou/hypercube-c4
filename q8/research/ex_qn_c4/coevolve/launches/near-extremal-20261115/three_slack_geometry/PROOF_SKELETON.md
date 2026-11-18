# Analytic complete exclusion of row (0,0,1,4,0,70,52,1,0)

- S01: Same actual683 graph, specified parity with this full profile/opposite unrestricted. C=333+4*177+105=1146, so reviewed actual-face inequality gives Phi_star<=3. L>=4 costs>=6 and L1/3 costs3/2, hence at most two actual odd-L faces.
- S02: For each omitted coordinate pair I, sum its four actual fixed-bit faces modulo2 to t_I. The unique degree2root contributes1, each actual degree3root contributes1 exactly when I meets its retained3mask. All other specified roots remain degree>=3. Thus t_I=1+sum_i 1[I meets A_i] mod2. T={I:t_I=1} has at most two elements because every such pair needs an actual odd-L face, and distinct pairs have disjoint actual faces. This connects actual fixed bits without an independent position normalization.
- S03: At every coordinate a, any3mask meets 7 or3 of the7 incident pairs, always odd. Therefore deg_T(a)=1+4=1 mod2. All8 coordinate degrees positive, so |T|>=4, contradiction. Repeated masks and arbitrary distinct common positions remain covered.
- S04: Exact455126-multiset direction scan (minimum6) is optional calibration only. Analytic |T|>=4 suffices; stop stronger position/completion work. No ordinary/high-star completion remains hidden. All other rows and full upper682 stay open.

Final proof: main.tex. This is author evidence awaiting Root's fresh local review, not a reviewer PASS. Only the existing crowded-face import is used; no historical trace replay, Lean or TeX/PDF compilation.
