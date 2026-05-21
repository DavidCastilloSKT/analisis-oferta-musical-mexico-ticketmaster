import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def run_script(script_name):
    script_path = SCRIPTS_DIR / script_name

    print(f"\nEjecutando {script_name}...")

    subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
    )


def main():
    print("Iniciando pipeline LATAM de Ticketmaster...")

    run_script("extract_ticketmaster_events.py")
    run_script("build_latam_enriched_model.py")

    print("\nPipeline LATAM terminado correctamente.")

if __name__ == "__main__":
    main()