# Analytic full row exclusion

Original domain: any actual C4-free683 graph/either specified parity profile (0,0,0,2,2,80,40,3,1), opposite unrestricted.

- T01: C=1146; accepted actual-face loss gives Phi_star<=3, hence at most2 actual odd-L Q6 faces. Four distinct same-parity low roots are exactly two degree3 plus two degree4 roots. All other roots remain degree>=3 in every Q6.
- T02: Literal actual face sets U,V have size18, P,Q size6; odd faces O=U xor V xor P xor Q. If A!=B, two distinct same-parity root positions agree in at most6 coordinates; the common omittedpairs must meet both different3masks. In any6 coordinates this gives at most10 pairs (if a truncation has size<=2, at most9; if both3, inclusion-exclusion 9+C(intersection,2)<=10). Thus |U xor V|>=16 and |O|>=16-12=4, impossible.
- T03: If A=B, sum each omittedpair's four actual fixed-bit faces modulo2. Direction parity is kR xor kS. If R!=S its support size12-2*C(|R∩S|,2)>=6, each requiring an actual odd face. Thus R=S.
- T04: Equal masks: translate entire marked cube once, x1=0,x2=D. Distance>=4 gives |U∩V|<=6 and |O|>=12. At distance2, h=|D∩A|=1/2 gives intersections9/5 and |O|>=6. At h0, U xor V consists of exactly two actual fixed-bit faces for each of6 pairs A×D. A4mask R cannot contain all5 coordinates A∪D; at least2 crosspairs are missing from R, leaving at least4 actual odd faces uncancellable. Full common-position domain closed.
- T05: Independent complete direction rebuild and two 2,000,250-position checks are optional calibration, not proof imports. Root's short t3 suggestion was checked; the stronger distinct-A intersection lemma closes all other cases analytically and removes computation dependence.

Final proof: main.tex. No original683 graph or completing ordinary/high stars is assumed. This is an author candidate awaiting fresh review; full upper682 and other rows remain OPEN.
