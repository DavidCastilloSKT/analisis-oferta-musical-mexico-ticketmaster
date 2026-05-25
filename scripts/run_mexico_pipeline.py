import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def run_script(script_name):
    script_path = SCRIPTS_DIR / script_name

    print(f"\nEjecutando {script_name}...")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    return result


def main():
    print("Iniciando pipeline Mexico de Ticketmaster...")

    run_script("extract_ticketmaster_events_mx.py")
    run_script("prepare_powerbi_dataset.py")

    print("\nPipeline Mexico terminado correctamente.")


if __name__ == "__main__":
    main()