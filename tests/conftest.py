"""Pytest fixtures for California Housing Dashboard tests."""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

# Ensure project root and src are on Python path
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

E2E_PORT = 8765
E2E_URL = f"http://127.0.0.1:{E2E_PORT}"


def _app_is_reachable():
    """Check if the Shiny app is responding."""
    try:
        req = urllib.request.Request(E2E_URL, method="HEAD")
        urllib.request.urlopen(req, timeout=2)
        return True
    except Exception:
        return False


@pytest.fixture(scope="session")
def shiny_server():
    """
    Start the Shiny app for E2E tests. Skips if already running.
    """
    if _app_is_reachable():
        yield E2E_URL
        return
    proc = subprocess.Popen(
        ["shiny", "run", "src/app.py", "--port", str(E2E_PORT)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(60):
        time.sleep(1)
        if _app_is_reachable():
            break
    else:
        proc.terminate()
        pytest.skip("Shiny app failed to start (e.g. missing GITHUB_TOKEN for AI tab)")
    try:
        yield E2E_URL
    finally:
        proc.terminate()
