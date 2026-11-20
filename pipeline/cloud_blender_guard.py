"""Run one Blender batch on Linux; stop only this batch on low available RAM."""
import argparse
from pathlib import Path
import os
import signal
import subprocess
import time


def available_kib():
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1])
    raise RuntimeError("Linux MemAvailable is unavailable; not launching an unguarded batch")


def process_rss(pid):
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    except FileNotFoundError:
        pass
    return 0


def stop_batch(process):
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-free-mib", type=int, default=2048)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("blender", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.blender
    if command and command[0] == "--":
        command = command[1:]
    if not command or Path(command[0]).name != "blender" or args.min_free_mib <= 0 or args.timeout <= 0:
        parser.error("supply positive limits and a Blender command after --")
    floor = args.min_free_mib * 1024
    before = available_kib()
    if before < floor:
        raise SystemExit(f"Not launching Blender: only {before // 1024} MiB available")
    proc = subprocess.Popen(command, start_new_session=True)
    start = time.monotonic()
    peak = 0
    try:
        while proc.poll() is None:
            peak = max(peak, process_rss(proc.pid))
            if available_kib() < floor:
                raise RuntimeError("Available RAM below reserve; stopped this Blender batch")
            if time.monotonic() - start >= args.timeout:
                raise RuntimeError("Time limit reached; stopped this Blender batch")
            time.sleep(0.1)
        return proc.returncode if proc.returncode >= 0 else 128 - proc.returncode
    finally:
        stop_batch(proc)
        print(f"BLENDER_BATCH_EXIT pid={proc.pid} sampled_peak_rss_mib={peak // 1024} "
              f"available_before_mib={before // 1024} available_after_mib={available_kib() // 1024}", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
