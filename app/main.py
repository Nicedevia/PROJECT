from fastapi import FastAPI
from app.routes import limitation, jour_ferie, meteo, vitesse, jours_feries_vacances

from fastapi import FastAPI

# Initialisation de l'application FastAPI
app = FastAPI(
    title="API de Gestion des Données",
    description="Une API pour gérer les données de limitation, jours fériés, météo et vitesse",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



# Inclure les routes pour chaque module, avec préfixes et tags pour faciliter la documentation
app.include_router(limitation.router, prefix="/limitation", tags=["limitation"])
app.include_router(jour_ferie.router, prefix="/jour_ferie", tags=["jour_ferie"])
app.include_router(meteo.router, prefix="/meteo", tags=["meteo"])
app.include_router(vitesse.router, prefix="/vitesse", tags=["vitesse"])
app.include_router(jours_feries_vacances.router, prefix="/jours_feries_vacances", tags=["Jours Feries Vacances"])

