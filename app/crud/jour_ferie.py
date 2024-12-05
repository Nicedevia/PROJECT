from app.db.cassandra_session import session
from app.models.schemas import JourFerie
from datetime import datetime

def create_jour_ferie(jour_ferie: JourFerie):
    query = """
    INSERT INTO jour_ferie (date, description, zone_1, zone_2, zone_3)
    VALUES (%s, %s, %s, %s, %s)
    """
    session.execute(query, (jour_ferie.date, jour_ferie.description, jour_ferie.zone_1, jour_ferie.zone_2, jour_ferie.zone_3))

def get_jour_ferie(date: datetime):
    query = "SELECT date, description, zone_1, zone_2, zone_3 FROM jour_ferie WHERE date = %s"
    row = session.execute(query, (date,)).one()
    return JourFerie(date=row.date, description=row.description, zone_1=row.zone_1, zone_2=row.zone_2, zone_3=row.zone_3) if row else None

def update_jour_ferie(date: datetime, jour_ferie: JourFerie):
    query = """
    UPDATE jour_ferie 
    SET description = %s, zone_1 = %s, zone_2 = %s, zone_3 = %s
    WHERE date = %s
    """
    session.execute(query, (jour_ferie.description, jour_ferie.zone_1, jour_ferie.zone_2, jour_ferie.zone_3, date))

def delete_jour_ferie(date: datetime):
    query = "DELETE FROM jour_ferie WHERE date = %s"
    session.execute(query, (date,))
