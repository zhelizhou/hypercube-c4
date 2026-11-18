from pathlib import Path
p=Path('native_leaf_simplex.py');s=p.read_text();a=s.index(' # Active seed818')
s=s[:a]+''' # On continuation reconstruct every actual appended valid row in order.
 if resume:
  for row in json.loads((R/'CUT_ROW_METADATA.json').read_text()):
   if row['kind']=='PSD':add_psd(row['block'],row['q'],row.get('origin','continued'))
   elif row['kind']=='INTEGER_ROUNDING':add_round(row,row.get('origin','continued'))
''' + s[a:]
a=s.index(" (R/'INITIAL_ALIAS_MAP.json')")
s=s[:a]+''' if resume:
  active=json.loads((R/'ACTIVE_COLUMNS.json').read_text())['indices'];keys={fkey(i):i for i in active}
''' + s[a:]
s=s.replace('st=time.monotonic();history=[];outer=0;final={};','st=time.monotonic();history=json.loads((R/\'MASTER_HISTORY.json\').read_text()) if resume else [];outer=0;final={};')
a=s.index(' lp=hs.HighsLp()')
s=s[:a]+''' if resume:
  maps=json.loads((R/'NATIVE_COLUMN_MAP.json').read_text());lambda_cols={int(i):j for i,j in maps['lambda'].items()};alpha_cols=np.array(maps['alpha']);beta_cols=np.array(maps['beta']);artcols=maps['artificial'];ncol=max(list(lambda_cols.values())+alpha_cols.tolist()+beta_cols.tolist()+artcols)+1
  assert len(artcols)==2*neq+m
  colmap=np.array([lambda_cols[i] for i in active]+alpha_cols.tolist()+beta_cols.tolist());realmat=sparse.vstack([EE,AA],format='coo');rr=realmat.row.tolist();cc=colmap[realmat.col].tolist();vv=realmat.data.tolist()
  for k in range(neq):rr.extend([k,k]);cc.extend([artcols[k],artcols[neq+k]]);vv.extend([1.,-1.])
  for k in range(m):rr.append(neq+k);cc.append(artcols[2*neq+k]);vv.append(-1.)
  MAT=sparse.csc_matrix((vv,(rr,cc)),shape=(neq+m,ncol));cost=np.zeros(ncol);cost[artcols]=1
''' + s[a:]
a=s.index(' # A genuine feasible phaseI primal');b=s.index(' def checkpoint():',a)
s=s[:a]+''' # Restore the actual appended-column/row basis by index. Its file names
 # can differ after native addRows; positions are pinned by NATIVE_COLUMN_MAP.
 if resume:
  lines=(R/'checkpoint.bas').read_text().splitlines();k=lines.index(next(x for x in lines if x.startswith('# Columns ')));nc=int(lines[k].split()[-1]);cv=[hs.HighsBasisStatus(int(x.split()[-1])) for x in lines[k+1:k+1+nc]];k=lines.index(next(x for x in lines if x.startswith('# Rows ')));nr=int(lines[k].split()[-1]);rv=[hs.HighsBasisStatus(int(x.split()[-1])) for x in lines[k+1:k+1+nr]];assert nc==ncol and nr==neq+m
  basis=hs.HighsBasis();basis.col_status=cv;basis.row_status=rv;basis.valid=True;assert h.setBasis(basis)!=hs.HighsStatus.kError;print('RESTORED_FULL_NATIVE_CHECKPOINT',nc,nr,flush=True)
 else:
  basis=hs.HighsBasis();cb=[hs.HighsBasisStatus.kLower]*ncol;rb=[hs.HighsBasisStatus.kUpper]*(neq+m)
  for k in range(neq):cb[nreal+k]=hs.HighsBasisStatus.kBasic
  for k in range(m):cb[nreal+2*neq+k]=hs.HighsBasisStatus.kBasic
  basis.col_status=cb;basis.row_status=rb;basis.valid=True;assert h.setBasis(basis)!=hs.HighsStatus.kError
''' + s[b:]
s=s.replace("h.writeBasis(str(R/'checkpoint.bas'))", "h.writeBasis(str(R/'checkpoint.bas'));h.writeModel(str(R/'checkpoint.mps'))")
s=s.replace(' for master in range(args.max_masters):',' startmaster=max([z.get(\'master\',-1) for z in history]+[-1])+1\n for master in range(startmaster,startmaster+args.max_masters):')
s=s.replace("'initialization':'crossover prior point then native primal simplex; artificial slacks are numerical not accepted'", "'initialization':'explicit feasible artificial basis or actual full native checkpoint; no crossover'")
p.write_text(s)
