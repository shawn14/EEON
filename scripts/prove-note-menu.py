#!/usr/bin/env python3
"""Real EEON note-menu UI proof. Run through the committed mac-run actions.
Uses a newly created simulator with no Apple account, actual Photos picker,
actual SwiftData store and real files. Never touches an existing simulator.
"""
import argparse
import json
import plistlib
import re
import struct
import shutil
import sqlite3
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


def inspect_built_entitlements():
    app = OUT/'DerivedData/Build/Products/Debug-iphonesimulator/voice notes.app'
    if not app.exists():
        return {'app_exists': False}
    result = subprocess.run(['/usr/bin/codesign', '-d', '--entitlements', ':-', str(app)], capture_output=True, text=True, timeout=30)
    xml = result.stdout
    try:
        entitlements = plistlib.loads(xml.encode()) if xml.strip() else {}
    except Exception:
        entitlements = {}
    # Simulator entitlements can be linked into __TEXT instead of the signature.
    info = plistlib.loads((app/'Info.plist').read_bytes())
    binary = (app/info['CFBundleExecutable']).read_bytes()
    simulated = {}
    assert struct.unpack_from('<I', binary)[0] == 0xfeedfacf, 'Expected native arm64 Mach-O artifact'
    position = 32
    for _ in range(struct.unpack_from('<I', binary, 16)[0]):
        command, size = struct.unpack_from('<II', binary, position)
        if command == 0x19:
            for index in range(struct.unpack_from('<I', binary, position+64)[0]):
                section = position+72+index*80
                name = binary[section:section+16].split(b'\0')[0]
                if name == b'__entitlements':
                    length = struct.unpack_from('<Q', binary, section+40)[0]
                    offset = struct.unpack_from('<I', binary, section+48)[0]
                    simulated = plistlib.loads(binary[offset:offset+length].rstrip(b'\0'))
        position += size
    return {'app_exists': True, 'bundle_id': info['CFBundleIdentifier'], 'codesign_exit': result.returncode, 'codesign_message': result.stderr.strip(), 'signed_entitlements': entitlements, 'simulator_entitlements': simulated, 'entitlements': {**entitlements, **simulated}}


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
        'built_artifact': inspect_built_entitlements(),
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



def verify_saved_photo(target):
    container = Path(run('xcrun', 'simctl', 'get_app_container', target, BUNDLE, 'data'))
    group = Path(run('xcrun', 'simctl', 'get_app_container', target, BUNDLE, 'group.com.eeon.voicenotes'))
    store = group/'Library/Application Support/default.store'
    with sqlite3.connect(store.as_uri()+'?mode=ro', uri=True) as db:
        rows = db.execute('SELECT ZIMAGEFILENAMESJSON FROM ZNOTE WHERE ZTITLE = ?', ('Paywall launch call',)).fetchall()
    assert len(rows) == 1, 'Expected exactly one persisted photo-test note'
    names = json.loads(rows[0][0] or '[]')
    assert len(names) == 1 and Path(names[0]).name == names[0], 'Expected one persisted attachment filename'
    photo = container/'Documents'/names[0]
    assert photo.is_file() and photo.stat().st_size > 0, 'Saved photo file is missing or empty'
    result = json.loads(run('xcrun', 'swift', str(ROOT/'scripts/verify-note-menu-photo.swift'), str(photo), str(ROOT/'voice notes UITests/Fixtures/whiteboard.png'), timeout=120))
    return {'persisted_note_attachments': len(names), 'saved_image_bytes': photo.stat().st_size, **result}



def cleanup_owned_simulators():
    inventory = json.loads(run('xcrun', 'simctl', 'list', 'devices', '--json'))
    devices = {device['udid']: device for group in inventory['devices'].values() for device in group}
    removed = []
    for receipt in OUT.glob('*/device.json'):
        owned = json.loads(receipt.read_text())
        target = owned['udid']
        device = devices.get(target)
        if device is None:
            continue
        assert owned.get('disposable') and device['name'].startswith('EEON-menu-proof-'), 'Refusing unowned simulator cleanup'
        if device['state'] == 'Booted':
            run('xcrun', 'simctl', 'shutdown', target)
        run('xcrun', 'simctl', 'delete', target)
        removed.append(target)
    print(json.dumps({'removed_owned_devices': removed}), flush=True)


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
        if mode in ('photo', 'all'):
            print('Initializing the real Photos app before fixture import', flush=True)
            photos_info = Path(runtime['runtimeRoot'])/'Applications/Photos.app/Info.plist'
            photos_bundle = plistlib.loads(photos_info.read_bytes())['CFBundleIdentifier']
            stage = 'Photos launch'
            try:
                run('xcrun', 'simctl', 'launch', target, photos_bundle)
                stage = 'Photos fixture import'
                print('Importing real photo fixture (one attempt, 180s limit)', flush=True)
                run('xcrun', 'simctl', 'addmedia', target, str(ROOT / 'voice notes UITests' / 'Fixtures' / 'whiteboard.png'), timeout=180)
            except Exception as error:
                # Launch failed before the old import-only catch. Preserve runtime
                # evidence before finally removes this disposable device.
                (result_dir/'photos-failure.json').write_text(json.dumps({
                    'stage': stage, 'error': str(error), 'source_sha': state['head'],
                    'device': target, 'app_tests_ran': False,
                }, indent=2)+'\n')
                diagnostics = {
                    'photos-system.log': ['xcrun', 'simctl', 'spawn', target, 'log', 'show', '--last', '5m', '--style', 'compact', '--predicate', 'process CONTAINS[c] "photo" OR process CONTAINS[c] "asset" OR process == "SpringBoard" OR process == "runningboardd"'],
                    'simulator-services.log': ['xcrun', 'simctl', 'spawn', target, 'launchctl', 'list'],
                }
                for filename, diagnostic_command in diagnostics.items():
                    try:
                        diagnostic = run(*diagnostic_command, timeout=30)
                        (result_dir/filename).write_text(diagnostic)
                    except Exception as diagnostic_error:
                        (result_dir/filename).write_text('Diagnostic failed: '+str(diagnostic_error)+'\n')
                simulator_logs = Path.home()/'Library/Logs/CoreSimulator'/target
                if simulator_logs.exists():
                    shutil.copytree(simulator_logs, result_dir/'simulator-logs')
                raise
        command = ['xcodebuild', '-project', str(ROOT/'voice notes.xcodeproj'), '-scheme', 'voice notes UITests', '-destination', 'id='+target, '-derivedDataPath', str(OUT/'DerivedData'), '-parallel-testing-enabled', 'NO', 'CODE_SIGNING_ALLOWED=YES', 'CODE_SIGN_IDENTITY=-']
        tests = ['testAddPhotoPresentsPicker'] if mode == 'picker' else ['testAddPhotoFromNoteMenu'] if mode == 'photo' else [
            'testAddPhotoFromNoteMenu', 'testNoteMenuCopyAndAgentBrief',
            'testNoteMenuProjectAndTags', 'testNoteMenuFavoritePersists',
            'testNoteMenuArchiveRoundTrip', 'testNoteMenuDeleteCancelAndRestore',
            'testNoteMenuPlaybackSpeeds', 'testNoteMenuCleanUpRecording',
            'testNoteMenuAskAboutThisNote', 'testNoteMenuShareLinkRequiresRealICloud',
            'testPasteAndExport', 'testNoteMindMap', 'testIdentifySpeakers',
        ]
        if mode == 'menu':
            tests.remove('testAddPhotoFromNoteMenu')
        command += ['-only-testing:voice notes UITests/ScreenshotTests/'+name for name in tests]
        assert not run('git', '-C', str(ROOT), 'status', '--porcelain', '--untracked-files=no'), 'Commit source before native proof'
        build_sha = run('git', '-C', str(ROOT), 'rev-parse', 'HEAD')
        with (result_dir/'build.log').open('w') as log:
            print('Building with simulator signing and real entitlements', flush=True)
            build_code = subprocess.run(command+['-resultBundlePath', str(result_dir/'build.xcresult'), 'build-for-testing'], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=1200).returncode
        if build_code:
            print('\n'.join((result_dir/'build.log').read_text(errors='replace').splitlines()[-40:]), flush=True)
            raise SystemExit(build_code)
        artifact = inspect_built_entitlements()
        (result_dir/'built-entitlements.json').write_text(json.dumps(artifact, indent=2)+'\n')
        expected = plistlib.loads((ROOT/'voice notes/voice notes.entitlements').read_bytes())
        assert artifact['codesign_exit'] == 0 and artifact['bundle_id'] == BUNDLE, 'Built app signature/identity check failed'
        for key in ['com.apple.developer.icloud-container-identifiers', 'com.apple.developer.icloud-services', 'com.apple.security.application-groups']:
            assert artifact['entitlements'].get(key) == expected[key], 'Built app is missing required entitlement: '+key
        print('Built artifact CloudKit and app-group entitlements verified', flush=True)
        with (result_dir/'test.log').open('w') as log:
            print('Running '+', '.join(tests)+' on disposable '+phone['name'], flush=True)
            code = subprocess.run(command+['-resultBundlePath', str(result_dir/'test.xcresult'), 'test-without-building'], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=1200).returncode
        test_log = (result_dir/'test.log').read_text(errors='replace')
        test_results = {name: ('passed' if re.search(re.escape(name)+r"\]' passed", test_log) else 'failed' if re.search(re.escape(name)+r"\]' failed", test_log) else 'not-run') for name in tests}
        if not all(result == 'passed' for result in test_results.values()):
            code = code or 1
        try:
            run('xcrun', 'xcresulttool', 'export', 'attachments', '--path', str(result_dir/'test.xcresult'), '--output-path', str(result_dir/'attachments'), timeout=60)
        except Exception as attachment_error:
            print('Result attachments unavailable: '+str(attachment_error), flush=True)
        assert run('git', '-C', str(ROOT), 'rev-parse', 'HEAD') == build_sha, 'Source changed during native proof; rerun after code settles'
        assert not run('git', '-C', str(ROOT), 'status', '--porcelain', '--untracked-files=no'), 'Source changed during native proof'
        file_proof = verify_saved_photo(target) if mode == 'photo' and code == 0 else None
        if mode in ('all', 'menu') and code == 0:
            container = run('xcrun', 'simctl', 'get_app_container', target, BUNDLE, 'data')
            file_proof = json.loads(run('xcrun', 'swift', str(ROOT/'scripts/verify-note-menu-files.swift'), container, str(ROOT/'voice notes UITests/Fixtures/two-speakers.m4a'), timeout=120))
        report = {'test_results': test_results, 'file_proof': file_proof, 'passed': code == 0, 'exit_code': code, 'tests': tests, 'source_sha': build_sha, 'result': str(result_dir), 'excluded_tests': ['testAddPhotoFromNoteMenu'] if mode == 'menu' else [], 'unproven': ['Successful CloudKit share requires a real Apple test account', 'Physical-device Photos and playback behavior require device proof']}
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
    parser.add_argument('mode',choices=['preflight','watch-runtime','picker','photo','all','menu','cleanup'])
    parser.add_argument('--simulator', action='store_true', help='Explicit simulator run; makes the Mac runner apply its heavy-job resource gate')
    args=parser.parse_args()
    mode=args.mode
    assert mode in ('preflight', 'cleanup') or args.simulator, 'UI runs require explicit --simulator'
    if mode == 'preflight':
        preflight()
    elif mode == 'cleanup':
        cleanup_owned_simulators()
    elif mode == 'watch-runtime':
        prepare_watch_runtime()
    else:
        proof(mode)
