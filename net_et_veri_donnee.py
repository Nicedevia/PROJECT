import os
import subprocess

def run_script(script_name):
    """
    Exécute un script Python et affiche son état.
    """
    try:
        print(f"Running {script_name}...")
        # Utilisation de subprocess pour exécuter chaque script Python
        subprocess.run(["python", f"app/nettoye/{script_name}"], check=True)
        print(f"Finished {script_name}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}\n")
        # Arrête l'exécution si une erreur est rencontrée
        raise

if __name__ == "__main__":
    # Liste des scripts à exécuter
    scripts = [
        "vacances.py",
        "veri_speed.py"
    ]

    # Exécute chaque script
    for script in scripts:
        run_script(script)

    print("All scripts executed successfully!")
