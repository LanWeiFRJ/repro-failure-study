"""Public tests use generated synthetic outcomes, never private run results."""
import csv
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import common
from analyze_outcomes import analyze,summarize
from bootstrap_table7 import estimate
from taxonomy import TAXONOMY

class MethodTests(unittest.TestCase):
    def test_instance_list(self):
        rows=common.read_csv('instances.csv')
        self.assertEqual(len(rows),100)
        self.assertEqual(len({r['instance_id'] for r in rows}),100)
        self.assertEqual(len({r['repo'] for r in rows}),9)
        self.assertEqual(Counter(r['repo_language'] for r in rows),{'python':45,'go':32,'js':23})

    def test_transition_formula(self):
        result=summarize(Counter(SS=2,SF=3,FS=1,FF=4))
        self.assertEqual(result['turnover_percent'],40)
        self.assertEqual(result['net_change_pp'],-20)

    def test_taxonomy(self):
        self.assertEqual(len({x['code'] for x in TAXONOMY}),15)
        self.assertEqual(len({x['parent_mode'] for x in TAXONOMY}),6)
        self.assertEqual({x['stage'] for x in TAXONOMY},{'S1','S2','S3','S4'})

    def test_synthetic_complete_design(self):
        ids=[r['instance_id'] for r in common.read_csv('instances.csv')]
        prior=common.INPUT_DIR
        with tempfile.TemporaryDirectory(prefix='repro-study-test-') as directory:
            common.INPUT_DIR=Path(directory)
            try:
                rows=[dict(instance_id=i,model=m,framework=f,round=r,profile=p,resolved=int(p!='baseline')) for i in ids for m,f in common.GROUPS for r in (1,2,3) for p in common.PROFILES]
                file=common.INPUT_DIR/'run_outcomes.csv'
                def save(values):
                    with file.open('w',newline='') as stream:
                        w=csv.DictWriter(stream,fieldnames=list(rows[0]));w.writeheader();w.writerows(values)
                save(rows)
                result=analyze()
                self.assertEqual(result['configuration_pairs']['n_pairs'],8400)
                self.assertEqual(result['configuration_pairs']['net_change_pp'],100)
                self.assertEqual(result['baseline_pairs']['n_pairs'],2100)
                self.assertEqual(result['baseline_pairs']['turnover_percent'],0)
                intervals=estimate(resamples=100)
                for g in intervals['rows']:
                    for values in g['deltas'].values():
                        self.assertEqual(values,dict(point=100.,lower=100.,upper=100.))
                save(rows[:-1])
                with self.assertRaises(ValueError):common.load_outcomes()
                save(rows+[rows[0]])
                with self.assertRaises(ValueError):common.load_outcomes()
            finally:common.INPUT_DIR=prior

if __name__=='__main__':unittest.main()
