from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable

FREQUENTATION_SOURCE = ROOT / "nettoyage" / "frequentation-gares.csv"
FREQUENTATION_CLEAN = ROOT / "nettoyage" / "frequentation-gares-clean.csv"

PROPRETE_SOURCES = [
    ROOT / "nettoyage" / "proprete-en-gare-22.csv",
    ROOT / "nettoyage" / "proprete-en-gare-23.csv",
    ROOT / "nettoyage" / "proprete-en-gare-24.csv",
]
PROPRETE_CLEANS = [
    ROOT / "nettoyage" / "proprete-en-gare-22-clean.csv",
    ROOT / "nettoyage" / "proprete-en-gare-23-clean.csv",
    ROOT / "nettoyage" / "proprete-en-gare-24-clean.csv",
]

NETTOYAGE_FREQUENTATION_SCRIPT = ROOT / "nettoyage" / "nettoyage_frequentation_gares.py"
NETTOYAGE_PROPRETE_SCRIPT = ROOT / "nettoyage" / "nettoyage_proprete_gare.py"
CREATION_BDD_SCRIPT = ROOT / "bdd" / "creation_bdd.py"
DB_PATH = ROOT / "bdd" / "gares.db"


def run_script(script_path: Path) -> None:
    print(f"[build] Exécution de {script_path.relative_to(ROOT)}")
    subprocess.run([PYTHON, str(script_path)], cwd=ROOT, check=True)


def needs_regeneration(source_paths: list[Path], output_paths: list[Path]) -> bool:
    if not all(path.exists() for path in output_paths):
        return True

    newest_source = max(path.stat().st_mtime for path in source_paths if path.exists())
    oldest_output = min(path.stat().st_mtime for path in output_paths)
    return newest_source > oldest_output


def main() -> int:
    print("[build] Démarrage de la préparation du projet")

    if needs_regeneration([FREQUENTATION_SOURCE], [FREQUENTATION_CLEAN]):
        run_script(NETTOYAGE_FREQUENTATION_SCRIPT)
    else:
        print("[build] Nettoyage fréquentation déjà à jour")

    if needs_regeneration(PROPRETE_SOURCES, PROPRETE_CLEANS):
        run_script(NETTOYAGE_PROPRETE_SCRIPT)
    else:
        print("[build] Nettoyage propreté déjà à jour")

    run_script(CREATION_BDD_SCRIPT)

    if DB_PATH.exists():
        print(f"[build] Base créée : {DB_PATH.relative_to(ROOT)}")
    else:
        print("[build] Attention : la base n'a pas été trouvée après exécution")

    print("[build] Terminé")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
