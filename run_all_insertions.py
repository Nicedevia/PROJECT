import os
import subprocess
import sys



def run_script(script_name):
    try:
        print(f"Running {script_name}...")
        # Utilisation de subprocess pour exécuter chaque script Python
        subprocess.run(["python", f"app/donnée/{script_name}"], check=True)
        print(f"Finished {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")

if __name__ == "__main__":
    # Liste des scripts à exécuter
    scripts = [
        "insert_meteo.py",
        "insert_vacances.py",
        # "update_database.py"  # Ajoutez les autres scripts nécessaires ici
        "insert_speedlimite.py",
        "insert_jours.py",
        "insert_vitesse.py"
    ]

    # Exécute chaque script
    for script in scripts:
        run_script(script)
