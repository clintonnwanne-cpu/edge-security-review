import copy
import unittest
from edge_review import review
NOW='2026-10-08T12:00:00Z'
BASE={'rules':[{'id':'r1','owner':'demo-team','environment':'demo','enabled':True,'path':'/api/session','token_expires_at':'2026-12-01T00:00:00Z'}]}
class EdgeTests(unittest.TestCase):
 def changed(self,**kw):
  d=copy.deepcopy(BASE); d['rules'][0].update(kw); return review(BASE,d,NOW)
 def test_clean_requires_review(self): self.assertEqual(review(BASE,BASE,NOW)['decision'],'REVIEW_REQUIRED')
 def test_expired(self): self.assertEqual(self.changed(token_expires_at=NOW)['remaining_findings'][0]['code'],'EXPIRED_TOKEN_METADATA')
 def test_wildcard(self): self.assertEqual(self.changed(path='/api/*')['decision'],'BLOCKED')
 def test_encoded(self): self.assertEqual(self.changed(path='/api/%2e')['decision'],'BLOCKED')
 def test_owner(self): self.assertEqual(self.changed(owner=' ')['decision'],'BLOCKED')
 def test_disabled(self): self.assertEqual(self.changed(enabled=False)['decision'],'BLOCKED')
 def test_removal(self): self.assertEqual(review(BASE,{'rules':[]},NOW)['removed_rule_ids'],['r1'])
 def test_environment(self): self.assertEqual(self.changed(environment='other')['environment_changes'],['r1'])
 def test_bad_expiry(self): self.assertEqual(self.changed(token_expires_at='bad')['decision'],'BLOCKED')
 def test_duplicate_id(self):
  d=copy.deepcopy(BASE); d['rules']*=2
  with self.assertRaises(ValueError): review(BASE,d,NOW)
 def test_proposed_fix(self):
  bad=copy.deepcopy(BASE); bad['rules'][0]['owner']=''
  r=review(bad,BASE,NOW); self.assertEqual(r['proposed_resolutions'],[('r1','MISSING_OWNER')]); self.assertEqual(r['decision'],'REVIEW_REQUIRED')
 def test_diff(self): self.assertIn('+',self.changed(owner='new-team')['diff'])
if __name__=='__main__': unittest.main()
