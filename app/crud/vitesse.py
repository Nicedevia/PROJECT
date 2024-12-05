from app.db.cassandra_session import session
from app.models.schemas import Vitesse
from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException, Body


def create_vitesse(vitesse: Vitesse):
    query = "INSERT INTO vitesse (date, capteur_id, vitesse) VALUES (%s, %s, %s)"
    session.execute(query, (vitesse.date, vitesse.capteur_id, vitesse.vitesse))

def get_vitesse(capteur_id: uuid.UUID, date: datetime):
    try:
        query = "SELECT date, capteur_id, vitesse FROM vitesse WHERE capteur_id = %s AND date = %s"
        row = session.execute(query, (capteur_id, date)).one()
        if row:
            return Vitesse(date=row.date, capteur_id=row.capteur_id, vitesse=row.vitesse)
        return None
    except Exception as e:
        print(f"Error retrieving vitesse: {e}")
        raise  # This will re-raise the exception for visibility in logs

def update_vitesse(capteur_id: uuid.UUID, date: datetime, new_vitesse: float):
    query = "UPDATE vitesse SET vitesse = %s WHERE capteur_id = %s AND date = %s"
    session.execute(query, (new_vitesse, capteur_id, date))

def delete_vitesse(capteur_id: uuid.UUID, date: datetime):
    query = "DELETE FROM vitesse WHERE capteur_id = %s AND date = %s"
    session.execute(query, (capteur_id, date))
