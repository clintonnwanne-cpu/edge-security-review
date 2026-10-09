"""Review fictional edge metadata and proposals offline; never apply changes."""
import argparse
import difflib
import json
from datetime import datetime


def stamp(value):
    d = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if d.tzinfo is None: raise ValueError('timezone required')
    return d


def findings(config, now):
    now = stamp(now)
    result, ids = [], set()
    for rule in config['rules']:
        rid = rule['id']
        if not isinstance(rid, str) or not rid.strip() or rid in ids:
            raise ValueError('rule IDs must be nonempty and unique')
        ids.add(rid)
        def add(code): result.append({'rule_id': rid, 'code': code})
        if not isinstance(rule.get('owner'), str) or not rule['owner'].strip(): add('MISSING_OWNER')
        if rule.get('enabled') is not True: add('DISABLED_OR_UNKNOWN')
        path = rule.get('path')
        if not isinstance(path, str) or not path.startswith('/') or '*' in path or '..' in path or '%' in path:
            add('BROAD_OR_UNSUPPORTED_PATH')
        if not isinstance(rule.get('environment'), str) or not rule['environment'].strip(): add('MISSING_ENVIRONMENT')
        try:
            if stamp(rule['token_expires_at']) <= now: add('EXPIRED_TOKEN_METADATA')
        except (KeyError, ValueError, TypeError, AttributeError): add('INVALID_TOKEN_EXPIRY')
    return sorted(result, key=lambda x: (x['rule_id'], x['code']))


def review(before, after, now):
    old, new = findings(before, now), findings(after, now)
    old_ids = {r['id'] for r in before['rules']}
    new_ids = {r['id'] for r in after['rules']}
    removed = sorted(old_ids - new_ids)
    old_pairs = {(f['rule_id'], f['code']) for f in old}
    new_pairs = {(f['rule_id'], f['code']) for f in new}
    old_rules = {r['id']: r for r in before['rules']}
    environment_changes = sorted(r['id'] for r in after['rules'] if r['id'] in old_rules and r.get('environment') != old_rules[r['id']].get('environment'))
    diff = '\n'.join(difflib.unified_diff(json.dumps(before, indent=2, sort_keys=True).splitlines(), json.dumps(after, indent=2, sort_keys=True).splitlines(), fromfile='before', tofile='proposed', lineterm=''))
    return {'decision': 'BLOCKED' if new or removed or environment_changes else 'REVIEW_REQUIRED',
            'remaining_findings': new, 'introduced': sorted(new_pairs-old_pairs),
            'proposed_resolutions': sorted(old_pairs-new_pairs), 'removed_rule_ids': removed,
            'environment_changes': environment_changes, 'diff': diff,
            'limitation': 'Fictional metadata only. No token secrets, real traffic, vendor rule semantics, deployment or validation. Every proposal needs human review.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('before'); p.add_argument('after'); p.add_argument('--now', required=True)
    a = p.parse_args()
    try:
        with open(a.before) as f: before = json.load(f)
        with open(a.after) as f: after = json.load(f)
        print(json.dumps(review(before, after, a.now), indent=2))
    except (ValueError, KeyError, TypeError, OSError) as e: p.exit(2, f'Invalid input: {e}\n')

if __name__ == '__main__': main()
