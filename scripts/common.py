"""Validated, portable inputs for the revision-time replication scripts."""
import csv
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / 'data'
OUTPUT_DIR = ROOT / 'results'
PROFILES = ['baseline','weak_understanding','weak_localization','weak_construction','weak_verification']
GROUPS = [(m,f) for m in ['DeepSeek-V4-Flash','DeepSeek-V4-Pro'] for f in ['OpenHands','PatchTwin','ReProAgent']] + [('GPT-5','OpenHands')]

def read_csv(name):
    # The public instance list is fixed; run results/labels are caller inputs.
    path = (ROOT / 'data' if name == 'instances.csv' else INPUT_DIR) / name
    with path.open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))

def configure():
    global INPUT_DIR,OUTPUT_DIR
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,required=True,help='Directory containing run_outcomes.csv and, for label summaries, baseline_failure_labels.csv')
    parser.add_argument('--output-dir',type=Path,default=OUTPUT_DIR)
    args=parser.parse_args()
    INPUT_DIR=args.data_dir.resolve();OUTPUT_DIR=args.output_dir.resolve()

def load_outcomes():
    rows=read_csv('run_outcomes.csv')
    instances=read_csv('instances.csv')
    ids=sorted(r['instance_id'] for r in instances)
    if len(ids)!=100 or len(set(ids))!=100:
        raise ValueError('Expected 100 unique instances')
    result={}
    for r in rows:
        key=(r['instance_id'],r['model'],r['framework'],int(r['round']),r['profile'])
        if key in result or r['resolved'] not in ('0','1'):
            raise ValueError('Duplicate key or non-binary outcome')
        result[key]=int(r['resolved'])
    expected={(i,m,f,r,p) for i in ids for m,f in GROUPS for r in (1,2,3) for p in PROFILES}
    if set(result)!=expected:
        raise ValueError('Missing or unexpected run keys')
    return ids,result

def output(name,obj):
    directory=OUTPUT_DIR
    directory.mkdir(parents=True,exist_ok=True)
    (directory/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
