from fastapi import APIRouter, HTTPException
from app.crud.vitesse import create_vitesse, get_vitesse, update_vitesse, delete_vitesse
from app.models.schemas import Vitesse
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Body
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Vitesse)
async def create_vitesse_endpoint(vitesse: Vitesse):
    try:
        create_vitesse(vitesse)
        return vitesse
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{capteur_id}/{date}", response_model=Vitesse)
async def get_vitesse_endpoint(capteur_id: uuid.UUID, date: datetime):
    try:
        result = get_vitesse(capteur_id, date)
        if result is None:
            raise HTTPException(status_code=404, detail="Vitesse not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{capteur_id}/{date}", response_model=Vitesse)
async def update_vitesse_endpoint(capteur_id: uuid.UUID, date: datetime, vitesse: float = Body(..., embed=True)):
    try:
        update_vitesse(capteur_id, date, vitesse)
        return {"capteur_id": capteur_id, "date": date, "vitesse": vitesse}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.delete("/{capteur_id}/{date}")
async def delete_vitesse_endpoint(capteur_id: uuid.UUID, date: datetime):
    try:
        delete_vitesse(capteur_id, date)
        return {"message": "Vitesse deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
