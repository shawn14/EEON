#!/usr/bin/env python3
"""Real EEON note-menu UI proof. Run through the committed mac-run actions.
Uses a newly created simulator with no Apple account, actual Photos picker,
actual SwiftData store and real files. Never touches an existing simulator.
"""
import argparse
import json
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build' / 'note-menu'
BUNDLE = 'voice.notes.voice-notes'


def run(*args, timeout=60):
    result = subprocess.run(args, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(args)}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def preflight():
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = json.loads(run('xcrun', 'simctl', 'list', '--json'))
    result = {
        'xcode': run('xcodebuild', '-version'),
        'free_gib': round(shutil.disk_usage(ROOT).free / 1024**3, 1),
        'booted': [d for ds in inventory['devices'].values() for d in ds if d['state'] == 'Booted'],
        'runtimes': [{k: r.get(k) for k in ['name', 'identifier', 'version', 'isAvailable', 'availabilityError']} for r in inventory['runtimes']],
        'api_key_file_present': (ROOT / 'voice notes' / 'APIKeys.swift').exists(),
        'head': run('git', '-C', str(ROOT), 'rev-parse', 'HEAD'),
    }
    (OUT / 'preflight.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)
    return inventory, result


def prepare_watch_runtime():
    inventory, state = preflight()
    if any(r.get('isAvailable') and '.watchOS-' in r['identifier'] for r in inventory['runtimes']):
        print('watchOS simulator runtime is already available', flush=True)
        return
    assert state['free_gib'] >= 25, 'Need 25 GiB before installing the required watchOS runtime'
    # Same pinned runtime used by the verified EEON 3.11 Watch screenshot build.
    subprocess.run(['xcodebuild', '-downloadPlatform', 'watchOS', '-buildVersion', '26.2', '-architectureVariant', 'arm64'], check=True, timeout=900)
    inventory, state = preflight()
    assert any(r.get('isAvailable') and '.watchOS-' in r['identifier'] for r in inventory['runtimes']), 'watchOS runtime is still unavailable'
    assert state['free_gib'] >= 15, 'Post-install disk reserve is below 15 GiB'


def proof(mode):
    inventory, state = preflight()
    assert state['free_gib'] >= 15, 'Below the required 15 GiB disk reserve'
    assert any(r.get('isAvailable') and '.watchOS-' in r['identifier'] for r in inventory['runtimes']), 'Embedded Watch target requires a watchOS simulator runtime'
    assert not state['booted'], 'An existing simulator is running; do not touch another session'
    runtimes = [r for r in inventory['runtimes'] if r.get('isAvailable') and r['identifier'].startswith('com.apple.CoreSimulator.SimRuntime.iOS-')]
    assert runtimes, 'No available iOS simulator runtime'
    runtime = max(runtimes, key=lambda r: tuple(int(n) for n in r['version'].split('.')))
    # simctl calls iPod touch an iPhone productFamily too; use the actual model name.
    version = tuple(int(n) for n in runtime['version'].split('.'))
    runtime_number = sum(n << shift for n, shift in zip(version + (0, 0), (16, 8, 0)))
    phones = [d for d in inventory['devicetypes']
              if d['name'].startswith('iPhone')
              and d.get('minRuntimeVersion', 0) <= runtime_number <= d.get('maxRuntimeVersion', 2**32-1)]
    assert phones, 'No iPhone simulator device type'
    phone = next((d for d in phones if 'Pro' not in d['name']), phones[0])
    stamp = str(int(time.time()))
    target = run('xcrun', 'simctl', 'create', 'EEON-menu-proof-'+stamp, phone['identifier'], runtime['identifier'])
    result_dir = OUT / (mode+'-'+stamp)
    result_dir.mkdir()
    (result_dir / 'device.json').write_text(json.dumps({'udid': target, 'type': phone, 'runtime': runtime, 'disposable': True}, indent=2)+'\n')
    try:
        print('Booting disposable '+phone['name'], flush=True)
        run('xcrun', 'simctl', 'boot', target)
        run('xcrun', 'simctl', 'bootstatus', target, '-b', timeout=120)
        if mode != 'picker':
            print('Importing real photo fixture', flush=True)
            run('xcrun', 'simctl', 'addmedia', target, str(ROOT / 'voice notes UITests' / 'Fixtures' / 'whiteboard.png'))
        command = ['xcodebuild', '-project', str(ROOT/'voice notes.xcodeproj'), '-scheme', 'voice notes UITests', '-destination', 'id='+target, '-derivedDataPath', str(OUT/'DerivedData'), '-parallel-testing-enabled', 'NO', 'CODE_SIGNING_ALLOWED=NO', '-resultBundlePath', str(result_dir/'test.xcresult')]
        tests = ['testAddPhotoPresentsPicker'] if mode == 'picker' else ['testAddPhotoFromNoteMenu'] if mode == 'photo' else [
            'testAddPhotoFromNoteMenu', 'testNoteMenuCopyAndAgentBrief',
            'testNoteMenuProjectAndTags', 'testNoteMenuFavoritePersists',
            'testNoteMenuArchiveRoundTrip', 'testNoteMenuDeleteCancelAndRestore',
            'testNoteMenuPlaybackSpeeds', 'testNoteMenuCleanUpRecording',
            'testNoteMenuAskAboutThisNote', 'testNoteMenuShareLinkRequiresRealICloud',
            'testPasteAndExport', 'testNoteMindMap', 'testIdentifySpeakers',
        ]
        command += ['-only-testing:voice notes UITests/ScreenshotTests/'+name for name in tests]
        command += ['test']
        assert not run('git', '-C', str(ROOT), 'status', '--porcelain', '--untracked-files=no'), 'Commit source before native proof'
        build_sha = run('git', '-C', str(ROOT), 'rev-parse', 'HEAD')
        with (result_dir/'test.log').open('w') as log:
            print('Running '+', '.join(tests)+' on disposable '+phone['name'], flush=True)
            code = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=1200).returncode
        assert run('git', '-C', str(ROOT), 'rev-parse', 'HEAD') == build_sha, 'Source changed during native proof; rerun after code settles'
        assert not run('git', '-C', str(ROOT), 'status', '--porcelain', '--untracked-files=no'), 'Source changed during native proof'
        file_proof = None
        if mode == 'all' and code == 0:
            container = run('xcrun', 'simctl', 'get_app_container', target, BUNDLE, 'data')
            file_proof = json.loads(run('xcrun', 'swift', str(ROOT/'scripts/verify-note-menu-files.swift'), container, str(ROOT/'voice notes UITests/Fixtures/two-speakers.m4a'), timeout=120))
        report = {'file_proof': file_proof, 'passed': code == 0, 'exit_code': code, 'tests': tests, 'source_sha': build_sha, 'result': str(result_dir), 'unproven': ['Successful CloudKit share requires a real Apple test account', 'Physical-device Photos and playback behavior require device proof']}
        (result_dir/'summary.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report, indent=2), flush=True)
        if code:
            print('\n'.join((result_dir/'test.log').read_text(errors='replace').splitlines()[-65:]), flush=True)
            raise SystemExit(code)
    finally:
        subprocess.run(['xcrun','simctl','shutdown',target], capture_output=True)
        subprocess.run(['xcrun','simctl','delete',target], capture_output=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['preflight','watch-runtime','picker','photo','all'])
    parser.add_argument('--simulator', action='store_true', help='Explicit simulator run; makes the Mac runner apply its heavy-job resource gate')
    args=parser.parse_args()
    mode=args.mode
    assert mode == 'preflight' or args.simulator, 'UI runs require explicit --simulator'
    if mode == 'preflight':
        preflight()
    elif mode == 'watch-runtime':
        prepare_watch_runtime()
    else:
        proof(mode)
