from app.db.cassandra_session import session
from app.models.schemas import Limitation
import uuid
from fastapi import APIRouter, HTTPException, Body


def create_limitation(limitation: Limitation):
    query = "INSERT INTO limitation (capteur_id, limitation) VALUES (%s, %s)"
    session.execute(query, (limitation.capteur_id, limitation.limitation))

def get_limitation(capteur_id: uuid.UUID):
    query = "SELECT capteur_id, limitation FROM limitation WHERE capteur_id = %s"
    row = session.execute(query, (capteur_id,)).one()
    return Limitation(capteur_id=row.capteur_id, limitation=row.limitation) if row else None

def update_limitation(capteur_id: uuid.UUID, limitation: float):
    query = "UPDATE limitation SET limitation = %s WHERE capteur_id = %s"
    session.execute(query, (limitation, capteur_id))


def delete_limitation(capteur_id: uuid.UUID):
    query = "DELETE FROM limitation WHERE capteur_id = %s"
    session.execute(query, (capteur_id,))
