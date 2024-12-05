from fastapi import APIRouter, HTTPException
from app.crud.jour_ferie import create_jour_ferie, get_jour_ferie, update_jour_ferie, delete_jour_ferie
from app.models.schemas import JourFerie
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=JourFerie)
async def create_jour_ferie_endpoint(jour_ferie: JourFerie):
    try:
        create_jour_ferie(jour_ferie)
        return jour_ferie
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{date}", response_model=JourFerie)
async def get_jour_ferie_endpoint(date: datetime):
    try:
        result = get_jour_ferie(date)
        if result is None:
            raise HTTPException(status_code=404, detail="Jour férié not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{date}", response_model=JourFerie)
async def update_jour_ferie_endpoint(date: datetime, updated_jour_ferie: JourFerie):
    try:
        # Utiliser l'objet JourFerie complet
        update_jour_ferie(date, updated_jour_ferie)
        return updated_jour_ferie
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{date}")
async def delete_jour_ferie_endpoint(date: datetime):
    try:
        delete_jour_ferie(date)
        return {"message": "Jour férié deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
