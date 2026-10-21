#!/usr/bin/env python3
"""EEON Mac-run wrapper around the canonical central Fastlane pipeline."""
import argparse, json, os, re, shutil, subprocess, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FASTLANE = ROOT.parent / 'fastlane-configs'
OUTPUT = ROOT / 'build/apple-release'
def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)
def main():
    mode = argparse.ArgumentParser()
    mode.add_argument('mode', choices=['beta', 'metadata', 'submit'])
    args = mode.parse_args()
    project = (ROOT / 'voice notes.xcodeproj/project.pbxproj').read_text()
    def value(key):
        values = set(re.findall(r'\b' + key + r' = ([^;]+);', project))
        assert len(values) == 1, f'Inconsistent {key}: {values}'
        return values.pop().strip('" ')
    version, build = value('MARKETING_VERSION'), value('CURRENT_PROJECT_VERSION')
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()
    assert git('branch', '--show-current') == 'main', 'Release requires main'
    assert not git('status', '--porcelain'), 'Release requires clean source'
    run(['git', 'fetch', 'origin'], cwd=ROOT)
    assert git('rev-parse', 'HEAD') == git('rev-parse', 'origin/main'), 'Main differs from GitHub'
    for source in ['appstore/voice-notes/3.10.0-build171', 'abfdd41a425acf668ef6c3417a472bd1a625a69e']:
        run(['git', 'merge-base', '--is-ancestor', source, 'HEAD'], cwd=ROOT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    run(['node', str(ROOT / 'scripts/apple-preflight.mjs')], cwd=ROOT)
    apple = json.loads(max(OUTPUT.glob('apple-*.json'), key=lambda p:p.stat().st_mtime).read_text())['result']
    env = {**os.environ, 'VOICE_NOTES_ROOT': str(ROOT), 'FASTLANE_SKIP_DOCS': '1', 'FASTLANE_SKIP_UPDATE_CHECK': '1'}
    fastlane = shutil.which('fastlane')
    assert fastlane, 'Installed Fastlane required'
    if args.mode == 'beta':
        assert shutil.disk_usage(ROOT).free >= 15 * 1024**3, 'Need 15 GiB free before archive'
        assert not any(b['version'] == build for b in apple['builds']), 'Build already uploaded; do not rebuild'
        env.update(GYM_OUTPUT_DIRECTORY=str(OUTPUT / 'artifact'), GYM_ARCHIVE_PATH=str(OUTPUT / 'EEON.xcarchive'), GYM_BUILDLOG_PATH=str(OUTPUT / 'logs'))
        # Reuse the October16 Vercel credential path; never commit or print the environment.
        website = ROOT.parent / 'v0-eeon-app-design'
        link = json.loads((website / '.vercel/project.json').read_text())
        assert link['projectName'] == website.name, 'Unexpected Vercel project link'
        with tempfile.TemporaryDirectory(prefix='eeon-release-env-') as scratch:
            secret_file = Path(scratch) / '.env.production'
            run(['vercel', 'env', 'pull', str(secret_file), '--environment=production', '--yes'], cwd=website, stdout=subprocess.DEVNULL)
            os.chmod(secret_file, 0o600)
            assert any(line.startswith('EEON_CLOUDKIT_API_TOKEN=') and line.split('=',1)[1].strip().strip('"') for line in secret_file.read_text().splitlines()), 'Production CloudKit API token missing'
            run([fastlane, 'beta', 'app:voice-notes', f'version:{version}', f'build:{build}'], cwd=FASTLANE, env={**env,'EEON_CLOUDKIT_ENV_FILE':str(secret_file)})
    elif args.mode == 'metadata':
        assert not any(v['version'] == version and v['state'] not in ['PREPARE_FOR_SUBMISSION','DEVELOPER_REJECTED','REJECTED','METADATA_REJECTED'] for v in apple['versions']), 'Target version is not editable'
        run([fastlane, 'metadata', 'app:voice-notes', f'version:{version}'], cwd=FASTLANE, env=env)
    else:
        active = [r for r in apple['reviews'] if r.get('platform') == 'IOS' and r['state'] in ['READY_FOR_REVIEW','WAITING_FOR_REVIEW','IN_REVIEW','UNRESOLVED_ISSUES']]
        assert not active, 'Active review exists; never let recovery cancel it implicitly'
        candidates = [b for b in apple['builds'] if b['version'] == build]
        assert len(candidates) == 1 and candidates[0]['processingState'] == 'VALID', 'Exact uploaded build must be VALID'
        prerelease_id = candidates[0]['relationships']['preReleaseVersion']['data']['id']
        train = next(v for v in apple['included'] if v['type'] == 'preReleaseVersions' and v['id'] == prerelease_id)
        assert train['attributes'] == {'version': version, 'platform': 'IOS'}, 'Wrong build train'
        assert all(s['state'] == 'APPROVED' for s in apple['subscriptions']), 'Unexpected subscription state'
        launcher = Path(fastlane).read_text()
        libexec = re.search(r'(/[^:"\n]+/fastlane/[^/]+/libexec)/bin', launcher).group(1)
        ruby = shutil.which('ruby', path='/opt/homebrew/opt/ruby/bin:' + os.environ['PATH'])
        env.update(GEM_HOME=str(Path.home()/'.local/share/fastlane/4.0.0'), GEM_PATH=str(Path.home()/'.local/share/fastlane/4.0.0')+':'+libexec, PHASE='submit', APP_VERSION=version, BUILD_NUMBER=build)
        script = str(FASTLANE / 'scripts/submit_app_review_fix.rb')
        run([ruby, script, 'voice-notes'], cwd=FASTLANE, env={**env, 'APPLY':'0'})
        run([ruby, script, 'voice-notes'], cwd=FASTLANE, env={**env, 'APPLY':'1'})
if __name__ == '__main__':
    main()
