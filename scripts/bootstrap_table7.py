"""Paired instance-cluster percentile bootstrap for Table 7.

Same estimator, seed, draw order and 50,000 resamples as the saved revision
analysis. Each sampled instance carries all three repeats, configurations
and seven fixed model-framework combinations. Intervals are marginal, not
simultaneous, and do not by themselves establish causal stage effects.
"""
import numpy as np
from common import GROUPS,PROFILES,load_outcomes,output,configure

def estimate(seed=20261003,resamples=50000):
    ids,data=load_outcomes()
    outcomes=np.empty((100,7,3,5),dtype=np.int8)
    for i,iid in enumerate(ids):
        for g,(m,f) in enumerate(GROUPS):
            for ri,r in enumerate((1,2,3)):
                for pi,p in enumerate(PROFILES):outcomes[i,g,ri,pi]=data[iid,m,f,r,p]
    differences=(outcomes[:,:,:,1:]-outcomes[:,:,:,:1]).mean(axis=2)*100
    values=np.concatenate([differences.reshape(100,28),differences.mean(axis=1)],axis=1)
    rng=np.random.default_rng(seed);draws=np.empty((resamples,32))
    for start in range(0,resamples,500):
        count=min(500,resamples-start)
        indices=rng.integers(0,100,size=(count,100))
        draws[start:start+count]=values[indices].mean(axis=1)
    limits=np.quantile(draws,[0.025,0.975],axis=0)
    points=values.mean(axis=0);successes=outcomes.sum(axis=(0,2));rows=[]
    for g,(m,f) in enumerate(GROUPS):
        rows.append(dict(model=m,framework=f,baseline_sr=100*int(successes[g,0])/300,
                         success_counts={p:int(successes[g,j]) for j,p in enumerate(PROFILES)},
                         deltas={p:dict(point=float(points[4*g+j]),lower=float(limits[0,4*g+j]),upper=float(limits[1,4*g+j])) for j,p in enumerate(PROFILES[1:])}))
    return dict(seed=seed,n_resamples=resamples,ci_level=0.95,multiplicity_adjusted=False,units='percentage points',
                rows=rows,pooled_fixed_combinations=[dict(profile=p,point=float(points[28+j]),lower=float(limits[0,28+j]),upper=float(limits[1,28+j])) for j,p in enumerate(PROFILES[1:])])

if __name__=='__main__':
    configure()
    result=estimate();output('table7_ci.json',result);print('Saved 28 combination-specific and 4 pooled intervals.')
