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


def proof(mode):
    inventory, state = preflight()
    assert state['free_gib'] >= 15, 'Below the required 15 GiB disk reserve'
    assert not state['booted'], 'An existing simulator is running; do not touch another session'
    runtimes = [r for r in inventory['runtimes'] if r.get('isAvailable') and r['identifier'].startswith('com.apple.CoreSimulator.SimRuntime.iOS-')]
    assert runtimes, 'No available iOS simulator runtime'
    runtime = max(runtimes, key=lambda r: tuple(int(n) for n in r['version'].split('.')))
    phones = [d for d in inventory['devicetypes'] if d.get('productFamily') == 'iPhone']
    assert phones, 'No iPhone simulator device type'
    phone = next((d for d in reversed(phones) if 'Pro' not in d['name']), phones[-1])
    stamp = str(int(time.time()))
    target = run('xcrun', 'simctl', 'create', 'EEON-menu-proof-'+stamp, phone['identifier'], runtime['identifier'])
    result_dir = OUT / ('photo-'+stamp if mode == 'photo' else 'all-'+stamp)
    result_dir.mkdir()
    (result_dir / 'device.json').write_text(json.dumps({'udid': target, 'type': phone, 'runtime': runtime, 'disposable': True}, indent=2)+'\n')
    try:
        run('xcrun', 'simctl', 'boot', target)
        run('xcrun', 'simctl', 'bootstatus', target, '-b', timeout=120)
        run('xcrun', 'simctl', 'addmedia', target, str(ROOT / 'voice notes UITests' / 'Fixtures' / 'whiteboard.png'))
        command = ['xcodebuild', '-project', str(ROOT/'voice notes.xcodeproj'), '-scheme', 'voice notes UITests', '-destination', 'id='+target, '-derivedDataPath', str(OUT/'DerivedData'), '-parallel-testing-enabled', 'NO', 'CODE_SIGNING_ALLOWED=NO', '-resultBundlePath', str(result_dir/'test.xcresult')]
        tests = ['testAddPhotoFromNoteMenu'] if mode == 'photo' else ['testAddPhotoFromNoteMenu']
        command += ['-only-testing:voice notes UITests/ScreenshotTests/'+name for name in tests]
        command += ['test']
        with (result_dir/'test.log').open('w') as log:
            print('Running '+', '.join(tests)+' on disposable '+phone['name'], flush=True)
            code = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=1200).returncode
        report = {'passed': code == 0, 'exit_code': code, 'tests': tests, 'source_sha': state['head'], 'result': str(result_dir)}
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
    parser.add_argument('mode',choices=['preflight','photo','all'])
    mode=parser.parse_args().mode
    if mode == 'preflight':
        preflight()
    else:
        proof(mode)
