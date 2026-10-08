"""SR, configuration matched pairs (TR/NC), and baseline repeated-run turnover.

Uses observed binary outcomes; does not re-run agents or infer causal effects.
Baseline pairs are chronological (1,2), (1,3), (2,3), counted once each.
Pairs reuse runs and are not independent observations.
"""
from collections import Counter
from itertools import combinations
from common import GROUPS,PROFILES,load_outcomes,output,configure

def summarize(c):
    n=sum(c.values());sf=c['SF'];fs=c['FS']
    return dict(n_pairs=n,counts={k:c[k] for k in ['SS','SF','FS','FF']},
                turnover_percent=100*(sf+fs)/n,net_change_pp=100*(fs-sf)/n)

def analyze():
    ids,data=load_outcomes();groups=[];base_all=Counter();config_all=Counter()
    profile_totals={p:Counter() for p in PROFILES[1:]}
    for model,framework in GROUPS:
        base=Counter();pairs_by_profile={};successes={}
        for p in PROFILES:
            successes[p]=sum(data[i,model,framework,r,p] for i in ids for r in (1,2,3))
        for a,b in combinations((1,2,3),2):
            for i in ids:
                base[('S' if data[i,model,framework,a,'baseline'] else 'F')+('S' if data[i,model,framework,b,'baseline'] else 'F')]+=1
        for p in PROFILES[1:]:
            c=Counter()
            for r in (1,2,3):
                for i in ids:
                    c[('S' if data[i,model,framework,r,'baseline'] else 'F')+('S' if data[i,model,framework,r,p] else 'F')]+=1
            pairs_by_profile[p]=summarize(c);config_all.update(c)
            profile_totals[p].update(c)
        base_all.update(base)
        groups.append(dict(model=model,framework=framework,runs_per_profile=300,
                           successes=successes,sr_percent={p:100*v/300 for p,v in successes.items()},
                           delta_sr_pp={p:100*(successes[p]-successes['baseline'])/300 for p in PROFILES[1:]},
                           baseline_pairs=summarize(base),configuration_pairs=pairs_by_profile))
    return dict(groups=groups,baseline_pairs=summarize(base_all),configuration_pairs=summarize(config_all),
                configuration_pairs_by_profile={p:summarize(c) for p,c in profile_totals.items()})

if __name__=='__main__':
    configure()
    result=analyze();output('outcomes.json',result)
    print(result['baseline_pairs']);print(result['configuration_pairs'])
