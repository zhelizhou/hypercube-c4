"""Additional bounded source/consumer and forbidden-converse adversaries."""
import independent_check as c
import numpy as np

def main():
    manifest=c.js(c.P/'FILES_SHA256.json')
    for name,want in manifest.items():
        assert c.hashlib.sha256(c.read(c.P/name)).hexdigest()==want,name
    interface=c.js(c.P/'INTERFACE.json')
    for name,want in interface['source_hashes'].items():
        assert c.hashlib.sha256(c.read(c.P/name)).hexdigest()==want,name
    layout=c.js(c.SCOPE/'EXTRA_EDGE3_LAYOUT.json')
    assert layout['start_equality_index']==152 and layout['rows']==204
    assert layout['original_quadratic_weight_factor']=='1/80'
    consumerK=c.mat(c.SCOPE/layout['lift_packed'])
    authorK=c.mat(c.LIFT/'EDGE3_LIFT_PACKED_KERNELS.npz')
    assert (consumerK!=authorK).nnz==0
    consumerH=c.mat(c.SCOPE/layout['beta_hypergeom'])
    assert (consumerH!=c.mat(c.P/'BETA_HYPERGEOM_CURRENT_204x1751.npz')).nnz==0
    # Individual normalization changes the shared root frame. Locate a small
    # literal counterexample rather than treating the warning as a slogan.
    counterexample=None;nonPSD=None
    for block,(root,states) in enumerate(zip(c.ROOTS,c.STATES)):
        AA=c.A_full(root,states);n=len(states)
        stabilizer=[fm for rm,fm in c.ACTIONS if rm[root]==root]
        norm=[c.SID[block][min(fm[f] for fm in stabilizer)] for f in states]
        wrong=AA[:,norm,:][:,:,norm]
        if counterexample is None and np.any(AA!=wrong):
            row,i,j=map(int,np.argwhere(AA!=wrong)[0])
            counterexample=dict(block=block,root=root,row=row,flags=[states[i],states[j]],individually_minimized_flags=[states[norm[i]],states[norm[j]]],actual_A=int(AA[row,i,j]),wrong_A=int(wrong[row,i,j]))
        diagonal=AA[:,np.arange(n),np.arange(n)]
        KK=12*AA-diagonal[:,:,None]-diagonal[:,None,:]
        # Negative 2x2 principal determinant is an exact non-PSD witness.
        if nonPSD is None:
            for row in range(204):
                d=np.diag(KK[row]).astype(np.int64)
                det=d[:,None]*d[None,:]-KK[row].astype(np.int64)**2
                if det.min()<0:
                    i,j=map(int,np.argwhere(det<0)[0]);nonPSD=dict(block=block,row=row,flags=[states[i],states[j]],principal_matrix=[[int(KK[row,i,i]),int(KK[row,i,j])],[int(KK[row,j,i]),int(KK[row,j,j])]],determinant=int(det[i,j]));break
    assert counterexample and nonPSD
    # Degenerate complete histograms: no root-mass division; r=1 rows vanish.
    emptyH=c.H_value(0,(7,0,0,0,0,0,0,0));emptyL=c.literal_L(0)
    assert emptyH[0]==70 and emptyL[0]==64 and not emptyH[120:].any() and not emptyL[120:].any()
    out=dict(status='PASS_BOUND_CONSUMER_AND_ADVERSARIES',frozen_manifest_all_entries_match=True,interface_source_hashes_match=True,actual_consumer_kernel_all_entries_match=True,actual_consumer_H_all_entries_match=True,equality_start=152,dual_normalization='K/80 with beta -H/70',separate_flag_normalization_counterexample=counterexample,exact_nonPSD_kernel_witness=nonPSD,empty_root1_mass_zero_adversary=True,scope='Source/consumer binding and adversarial checks only; no LP/full scan/global dual claim.')
    c.output('CONSUMER_ADVERSARIES.json',out)
    c.output('CONSUMER_INPUT_RECEIPT.json',dict(files=c.INPUTS))
    print(c.json.dumps(out,indent=2))
if __name__=='__main__':main()
