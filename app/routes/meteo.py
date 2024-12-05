from fastapi import APIRouter, HTTPException
from app.crud.meteo import create_meteo, get_meteo, update_meteo, delete_meteo
from app.models.schemas import Meteo
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Body
import uuid
from datetime import datetime


router = APIRouter()

@router.post("/", response_model=Meteo)
async def create_meteo_endpoint(meteo: Meteo):
    try:
        create_meteo(meteo)
        return meteo
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{capteur_id}/{date}", response_model=Meteo)
async def get_meteo_endpoint(capteur_id: uuid.UUID, date: datetime):
    try:
        result = get_meteo(capteur_id, date)
        if result is None:
            raise HTTPException(status_code=404, detail="Météo not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



from fastapi.concurrency import run_in_threadpool

from logging_config import logger

@router.put("/{capteur_id}/{date}", response_model=Meteo)
async def update_meteo(capteur_id: uuid.UUID, date: datetime, visibilite: float = Body(...), precipitation: float = Body(...)):
    logger.info(f"Requête reçue pour mise à jour du capteur {capteur_id} à la date {date}.")
    try:
        update_meteo(capteur_id, date, visibilite, precipitation)
        logger.info(f"Mise à jour réussie pour le capteur {capteur_id} à la date {date}.")
        return {"capteur_id": capteur_id, "date": date, "visibilite": visibilite, "precipitation": precipitation}
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour du capteur {capteur_id} : {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.delete("/{capteur_id}/{date}")
async def delete_meteo_endpoint(capteur_id: uuid.UUID, date: datetime):
    try:
        delete_meteo(capteur_id, date)
        return {"message": "Météo deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
