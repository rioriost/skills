"""Exercise audit boundaries using fake tools, without auditing the host."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/mac-performance-maintenance/skills/mac-performance-maintenance/scripts/audit.sh'
SOURCE = SCRIPT.read_text()
# Load the actual function definitions, before the audit's main entry point.
FUNCTIONS = SOURCE.split("printf '%s\\n' \"# Mac Performance Maintenance Audit\"", 1)[0]


class AuditTests(unittest.TestCase):
    def run_shell(self, code, path):
        return subprocess.run(['/bin/bash', '-c', FUNCTIONS + '\n' + code],
                              env={**os.environ, 'PATH': str(path) + os.pathsep + os.environ['PATH']},
                              text=True, capture_output=True, timeout=10)

    def tool(self, path, name, body):
        file = path / name
        file.write_text('#!/bin/sh\n' + body + '\n')
        file.chmod(0o755)

    def test_partial_size_is_unknown(self):
        with tempfile.TemporaryDirectory(prefix='mac-audit-test-') as directory:
            path = Path(directory)
            self.tool(path, 'du', 'printf "1024\\t%s\\n" "$2"; echo "Permission denied" >&2; exit 1')
            result = subprocess.run(
                ['/bin/bash', '-c', 'audit_fixture=$1\nset --\n' + FUNCTIONS + '\nshow_paths "fixture" "$audit_fixture"', 'test', directory],
                env={**os.environ, 'PATH': directory + os.pathsep + os.environ['PATH']},
                text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0)
            self.assertIn('UNKNOWN', result.stdout)
            self.assertNotIn('1.0 MiB', result.stdout)
            self.assertIn('Permission denied', result.stderr)

    def test_readable_size_is_measured(self):
        with tempfile.TemporaryDirectory(prefix='mac-audit-test-') as directory:
            path = Path(directory)
            self.tool(path, 'du', 'printf "1024\\t%s\\n" "$2"')
            result = subprocess.run(
                ['/bin/bash', '-c', 'audit_fixture=$1\nset --\n' + FUNCTIONS + '\nshow_paths "fixture" "$audit_fixture"', 'test', directory],
                env={**os.environ, 'PATH': directory + os.pathsep + os.environ['PATH']},
                text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0)
            self.assertIn('1.0 MiB', result.stdout)
            self.assertNotIn('UNKNOWN', result.stdout)

    def test_container_inventory_never_queries_daemons(self):
        section = SOURCE.split('section "Container runtimes"', 1)[1].split(
            'show_paths "Focused container storage paths"', 1)[0]
        with tempfile.TemporaryDirectory(prefix='mac-audit-test-') as directory:
            path = Path(directory)
            # Advertise all commands; any daemon command would be visible as FORBIDDEN.
            body = 'case "$*" in --version) echo fixture-version;; --help) printf "system\\ncontainer\\nimage\\nvolume\\nlist\\nmachine\\nnetwork\\nbuilder\\n";; *) echo FORBIDDEN; exit 99;; esac'
            for name in ('docker', 'podman', 'container'):
                self.tool(path, name, body)
            result = self.run_shell(section, path)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.count('fixture-version'), 3)
            self.assertNotIn('FORBIDDEN', result.stdout)
            self.assertIn('UNKNOWN', result.stdout)

    def test_vm_inventory_never_launches_tools(self):
        section = SOURCE.split('section "Virtual machines"', 1)[1].split(
            'show_paths "Focused VM storage paths"', 1)[0]
        with tempfile.TemporaryDirectory(prefix='mac-audit-test-') as directory:
            path = Path(directory)
            for name in ('prlctl', 'utmctl', 'limactl', 'colima', 'VBoxManage'):
                self.tool(path, name, 'echo FORBIDDEN; exit 99')
            result = self.run_shell(section, path)
            self.assertEqual(result.returncode, 0)
            self.assertNotIn('FORBIDDEN', result.stdout)
            self.assertEqual(result.stdout.count('inventory deferred'), 5)

    def test_help_and_bad_arguments_exit_before_audit(self):
        for arguments, status in ((['--help'], 0), (['--top', '0'], 64), (['--unknown'], 64)):
            with self.subTest(arguments=arguments):
                result = subprocess.run(['/bin/bash', str(SCRIPT), *arguments],
                                        text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, status)
                self.assertNotIn('## Platform', result.stdout)


if __name__ == '__main__':
    unittest.main()
