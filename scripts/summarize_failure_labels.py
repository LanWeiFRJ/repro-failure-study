"""Aggregate existing paper-used labels, not re-annotate or validate their truth.

Supports Figures 5--7 and language-level distributions. The derived stage
is tied to the primary family, not an independently measured causal stage.
"""
from collections import Counter
from common import GROUPS,read_csv,load_outcomes,output,configure
from taxonomy import TAXONOMY

def summarize():
    ids,data=load_outcomes();rows=read_csv('baseline_failure_labels.csv')
    taxonomy=TAXONOMY
    bycode={r['code']:r for r in taxonomy};seen=set()
    for r in rows:
        if r['profile']!='baseline':raise ValueError('Only baseline labels belong in this input')
        key=(r['instance_id'],r['model'],r['framework'],int(r['round']),'baseline')
        if key in seen or data.get(key)!=0:raise ValueError('Non-failure, missing or duplicate label key')
        seen.add(key)
        t=bycode[r['fine_mode_code']]
        if (t['stage'],t['parent_mode'])!=(r['primary_stage'],r['parent_mode']):raise ValueError('Taxonomy mismatch')
    if seen!={k for k,v in data.items() if k[-1]=='baseline' and v==0}:raise ValueError('Incomplete failure labels')
    def counts(sub):
        n=len(sub)
        return dict(n_failures=n,fine_mode_counts=dict(Counter(r['fine_mode_code'] for r in sub)),
                    parent_mode_counts=dict(Counter(r['parent_mode'] for r in sub)),
                    stage_counts=dict(Counter(r['primary_stage'] for r in sub)),
                    fine_mode_percent={t['code']:100*sum(r['fine_mode_code']==t['code'] for r in sub)/n if n else None for t in taxonomy},
                    parent_mode_percent={p:100*sum(r['parent_mode']==p for r in sub)/n if n else None for p in sorted({t['parent_mode'] for t in taxonomy})},
                    stage_percent={s:100*sum(r['primary_stage']==s for r in sub)/n if n else None for s in ['S1','S2','S3','S4']})
    groups=[dict(model=m,framework=f,**counts([r for r in rows if (r['model'],r['framework'])==(m,f)])) for m,f in GROUPS]
    langs={r['instance_id']:r['repo_language'] for r in read_csv('instances.csv')}
    return dict(overall=counts(rows),groups=groups,languages={lang:counts([r for r in rows if langs[r['instance_id']]==lang]) for lang in sorted(set(langs.values()))})

if __name__=='__main__':
    configure()
    result=summarize();output('failure_counts.json',result);print(result['overall'])
