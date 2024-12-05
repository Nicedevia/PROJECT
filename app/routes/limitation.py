from fastapi import APIRouter, HTTPException
from app.crud.limitation import create_limitation, get_limitation, update_limitation, delete_limitation
from app.models.schemas import Limitation
import uuid
from fastapi import APIRouter, HTTPException, Body
import uuid

router = APIRouter()

@router.post("/", response_model=Limitation)
async def create_limitation_endpoint(limitation: Limitation):
    try:
        create_limitation(limitation)
        return limitation
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{capteur_id}", response_model=Limitation)
async def get_limitation_endpoint(capteur_id: uuid.UUID):
    try:
        result = get_limitation(capteur_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Limitation not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.put("/{capteur_id}", response_model=Limitation)
async def update_limitation_endpoint(capteur_id: uuid.UUID, limitation: float = Body(..., embed=True)):
    try:
        # Fonction synchrone ici pour éviter les avertissements d'attente
        update_limitation(capteur_id, limitation)
        return {"capteur_id": capteur_id, "limitation": limitation}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{capteur_id}")
async def delete_limitation_endpoint(capteur_id: uuid.UUID):
    try:
        delete_limitation(capteur_id)
        return {"message": "Limitation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
