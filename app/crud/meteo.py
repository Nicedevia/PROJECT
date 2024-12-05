from app.db.cassandra_session import session
from app.models.schemas import Meteo
from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException, Body


def create_meteo(meteo: Meteo):
    query = """
    INSERT INTO meteo (date, capteur_id, visibilite, precipitation)
    VALUES (%s, %s, %s, %s)
    """
    session.execute(query, (meteo.date, meteo.capteur_id, meteo.visibilite, meteo.precipitation))

def get_meteo(capteur_id: uuid.UUID, date: datetime):
    query = "SELECT date, capteur_id, visibilite, precipitation FROM meteo WHERE capteur_id = %s AND date = %s"
    row = session.execute(query, (capteur_id, date)).one()
    return Meteo(date=row.date, capteur_id=row.capteur_id, visibilite=row.visibilite, precipitation=row.precipitation) if row else None

def update_meteo(capteur_id: uuid.UUID, date: datetime, new_visibilite: float, new_precipitation: float):
    query = """
    UPDATE meteo SET visibilite = %s, precipitation = %s
    WHERE capteur_id = %s AND date = %s
    """
    session.execute(query, (new_visibilite, new_precipitation, capteur_id, date))

def delete_meteo(capteur_id: uuid.UUID, date: datetime):
    query = "DELETE FROM meteo WHERE capteur_id = %s AND date = %s"
    session.execute(query, (capteur_id, date))
