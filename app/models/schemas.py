# app/models/schemas.py

from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class Vitesse(BaseModel):
    date: datetime
    capteur_id: uuid.UUID
    vitesse: float = Field(..., gt=0, description="La vitesse doit être positive")

    class Config:
        schema_extra = {
            "example": {
                "date": "2023-01-01T00:00:00",
                "capteur_id": "123e4567-e89b-12d3-a456-426614174000",
                "vitesse": 50.5
            }
        }

class JourFerie(BaseModel):
    date: datetime
    description: str
    zone_1: bool
    zone_2: bool
    zone_3: bool

    class Config:
        schema_extra = {
            "example": {
                "date": "2023-12-25T00:00:00",
                "description": "Noël",
                "zone_1": True,
                "zone_2": False,
                "zone_3": True
            }
        }

class Limitation(BaseModel):
    capteur_id: uuid.UUID
    limitation: float = Field(..., gt=0, description="La limitation doit être positive")

    class Config:
        schema_extra = {
            "example": {
                "capteur_id": "123e4567-e89b-12d3-a456-426614174000",
                "limitation": 120.0
            }
        }

class Meteo(BaseModel):
    date: datetime
    capteur_id: uuid.UUID
    visibilite: float = Field(..., ge=0, le=100, description="Visibilité en pourcentage entre 0 et 100")
    precipitation: float = Field(..., ge=0, description="Quantité de précipitations, ne peut pas être négative")

    class Config:
        schema_extra = {
            "example": {
                "date": "2023-01-01T00:00:00",
                "capteur_id": "123e4567-e89b-12d3-a456-426614174000",
                "visibilite": 75.0,
                "precipitation": 12.5
            }
        }

# Add the JourFerieVacances class below

class JourFerieVacances(BaseModel):
    evenement_id: str  # Utilisez une chaîne pour UUID, la conversion sera effectuée avant la requête
    description: str = Field(..., description="Description de l'événement, par exemple 'Vacances d'Été'")
    date_debut: datetime = Field(..., description="Date de début de l'événement")
    date_fin: datetime = Field(..., description="Date de fin de l'événement")
    zones: str = Field(..., description="Zone concernée, par exemple 'Zone A'")
    annee_scolaire: str = Field(..., description="Année scolaire, par exemple '2024-2025'")
    type_evenement: str = Field(..., description="Type d'événement, par exemple 'vacances'")
