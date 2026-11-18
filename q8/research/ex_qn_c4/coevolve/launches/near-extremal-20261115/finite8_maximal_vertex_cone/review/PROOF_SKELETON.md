# Proof skeleton and semantic obligations

Canonical source: `PROOF.md`; 25 source units covered and 29 extracted semantic obligations checked. No uncovered source unit or dependency cycle. Receipt coverage is not itself a validity proof.

The exact quantified scope, typed symbols, assumption usage and every application are in `OBLIGATION_LEDGER.json`. All sums are finite. There are no asymptotic or limit-order claims.

| ID | Obligation | Depends on | Discharge |
|---|---|---|---|
| MV01-OB01 | The nonfull square patterns modulo swapping axes have exactly the stated nine IDs and groups |  | GEOMETRY_RESULT.json, independent_check.py:geometry_checks |
| MV01-OB02 | Every 4-cycle is a coordinate square |  | REVIEW.md: MV01 derivation |
| MV01-OB03 | X0=C(8-d,2), X1=d(8-d), X2=C(d,2) | MV01-OB01 | REVIEW.md, GEOMETRY_RESULT.json |
| MV01-OB04 | Every missing root direction has a state-8 completion, and each state-8 square has one missing direction | MV01-OB01, MV01-OB02 | REVIEW.md: MV01 derivation |
| MV01-OB05 | x8>=8-d, d0 impossible; d1 forces x8=7 | MV01-OB03, MV01-OB04 | REVIEW.md, GRAPH_RESULT.json |
| MV02-OB01 | Subtracting 8-d from x8 is a bijection to independent weak compositions | MV01-OB03 | REVIEW.md, DOMAIN_RESULT.json |
| MV02-OB02 | Complete refined domain sizes are the listed counts, total253440; original total674172 | MV02-OB01, MV01-OB05 | DOMAIN_RESULT.json, independent_check.py:weak/domain_checks |
| MV02-OB03 | Each refined histogram appears exactly once, including d1/d8 boundaries; no d0 minimum | MV02-OB01, MV02-OB02 | DOMAIN_RESULT.json, REVIEW.md |
| MV03-OB01 | State at the transported marked root is unchanged | MV01-OB01 | GEOMETRY_RESULT.json:Q4_root_transports_checked, REVIEW.md |
| MV03-OB02 | Disjoint/overlap/equal probabilities15/28,12/28,1/28 and Q4 completion multiplicities1,5,15 |  | GEOMETRY_RESULT.json, REVIEW.md: bridge derivation |
| MV03-OB03 | E_lambda T_Q=tr(Q sum_v x_vx_vT/(256*784)) with same actual restriction lambda | MV03-OB01, MV03-OB02 | REVIEW.md: bridge derivation, GRAPH_RESULT.json |
| MV03-OB04 | Uii=2cii,Uij=cij; true trace pairing and generator upper coordinates agree | MV03-OB03 | PAIRING_RESULT.json, REVIEW.md |
| MV03-OB05 | M5=sum gamma xxT/784, gamma>=0 and degree marginals Nd/256 | MV01-OB05, MV03-OB03 | REVIEW.md, GRAPH_RESULT.json |
| MV03-OB06 | sum_p alpha_p n_d(p)=Nd/2, hence degree mass=sum alpha nd/128 | MV03-OB05 | REVIEW.md, GRAPH_RESULT.json |
| MV03-OB07 | M5 is PSD; no graph realization converse asserted | MV03-OB05 | REVIEW.md |
| MV04-OB01 | E_lambda T_Q+sum_alpha sum_d Bd nd/(128*784)>=0 | MV03-OB03, MV03-OB05, MV03-OB06 | REVIEW.md |
| MV04-OB02 | Bd=-finite_min is valid for1<=d<=8; B0=0 is merely a convention | MV02-OB02, MV01-OB05 | DOMAIN_RESULT.json, REVIEW.md |
| MV04-OB03 | Signed128 scoring is exact and overflow-free, including INT64_MIN | MV02-OB03 | DOMAIN_RESULT.json, RESULT.json:compiler_sanitizer, REVIEW.md |
| MV04-OB04 | Exactly90 in-range integer tokens, symmetric Q; malformed/asymmetric/extra/missing inputs rejected; default queryzero |  | PARSER_RESULT.json, DOMAIN_RESULT.json |
| MV05-OB01 | lTx=7[x8-(8-d)]>=0 | MV01-OB03, MV02-OB01 | DOMAIN_RESULT.json, REVIEW.md |
| MV05-OB02 | Q^(i)=ei lT+l eiT gives xTQx=2xi lTx>=0 and 2(M5 l)i>=0 | MV05-OB01, MV04-OB01 | DOMAIN_RESULT.json:RLT_matrices_exact, GRAPH_RESULT.json, REVIEW.md |
| MV06-OB01 | Each saved Q is symmetric; every Bd cancels its degree minimum, hence the cuts are valid | MV02-OB03, MV04-OB01, MV04-OB02, MV04-OB03 | DOMAIN_RESULT.json |
| MV06-OB02 | All local masks are legal; all profile rows are nonnegative integer128 counts; exact separate rational normalizations produce degree0 masszero |  | PAIRING_RESULT.json, independent_check.py:exact_pairing |
| MV06-OB03 | Exact pairing is the stated strictly negative rational number; smoke cut negative too | MV03-OB04, MV06-OB01, MV06-OB02 | PAIRING_RESULT.json |
| MV06-OB04 | Both graphs C4-free and maximal; exact degree/gamma/completion counts and all81 moment entries match | MV01-OB05, MV03-OB03, MV05-OB02 | GRAPH_RESULT.json |
| MV06-OB05 | Without maximality x8>=8-d and RLT can fail, including empty RLT0=-4 | MV01-OB01, MV05-OB02 | GEOMETRY_RESULT.json |
| CALLER-OB01 | CUT_FOUND is accepted only after complete exact pricing, repaired biases and negative rational pairing | MV06-OB01, MV06-OB03 | PAIRING_RESULT.json, PROVENANCE_RESULT.json, REVIEW.md |
| CALLER-OB02 | Bad limits, changed existing input, existing history and nonzero degree0 mass reject before LP; no-cut inconclusive |  | CLI_CONTRACT_RESULT.json, cli_contract_check.py |
| SCOPE-OB01 | Package proves a universal maximal-only necessary cone and concrete abstract separation, not ex<=682/fullNO/graph realization | MV04-OB01, MV06-OB03, CALLER-OB02 | REVIEW.md |
