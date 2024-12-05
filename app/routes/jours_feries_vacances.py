from fastapi import APIRouter, Depends, HTTPException
from app.crud.jours_feries_vacances import create_vacance, get_vacance, update_vacance, delete_vacance
from cassandra.cluster import Session
import uuid
import logging


router = APIRouter()

# Dependency injection for Cassandra session
def get_session():
    from app.db.cassandra_session import session
    return session

logger = logging.getLogger(__name__)

@router.post("/")
async def create_vacance_endpoint(vacance: dict, session: Session = Depends(get_session)):
    try:
        logger.info(f"Requête reçue : {vacance}")
        vacance['evenement_id'] = uuid.UUID(vacance['evenement_id'])  # Convertir en UUID
        create_vacance(session, vacance)
        logger.info("Vacance créée avec succès")
        return {"message": "Vacance créée avec succès"}
    except Exception as e:
        logger.error(f"Erreur lors de la création : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")

import logging

logger = logging.getLogger(__name__)
@router.get("/{evenement_id}", response_model=dict)
async def get_vacance_endpoint(evenement_id: str, session: Session = Depends(get_session)):
    logger.info(f"GET request for evenement_id: {evenement_id}")
    try:
        uuid_evenement_id = uuid.UUID(evenement_id)
        vacance = get_vacance(session, uuid_evenement_id)
        if not vacance:
            logger.warning(f"No vacation found for ID: {evenement_id}")
            raise HTTPException(status_code=404, detail="Vacation event not found")
        logger.info(f"Found vacation: {vacance}")
        return vacance
    except Exception as e:
        logger.error(f"Error in GET request for evenement_id {evenement_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{evenement_id}", response_model=dict)
async def update_vacance_endpoint(evenement_id: str, vacance: dict, session: Session = Depends(get_session)):
    logger.info(f"PUT request for evenement_id: {evenement_id} with data: {vacance}")
    try:
        uuid_evenement_id = uuid.UUID(evenement_id)
        updated_vacance = update_vacance(session, uuid_evenement_id, vacance)
        if not updated_vacance:
            logger.warning(f"No vacation found to update for ID: {evenement_id}")
            raise HTTPException(status_code=404, detail="Vacation event not found")
        logger.info(f"Updated vacation: {updated_vacance}")
        return updated_vacance
    except Exception as e:
        logger.error(f"Error in PUT request for evenement_id {evenement_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{evenement_id}")
async def delete_vacance_endpoint(evenement_id: str, session: Session = Depends(get_session)):
    try:
        evenement_id = uuid.UUID(evenement_id)  # Convertir en UUID
        deleted = delete_vacance(session, evenement_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Vacance introuvable pour suppression")
        return {"message": "Vacance supprimée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression : {str(e)}")
