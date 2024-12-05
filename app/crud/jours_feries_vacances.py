from app.db.cassandra_session import session
from app.models.schemas import JourFerie
from datetime import datetime
import uuid


def create_vacance(session, vacance):
    query = """
        INSERT INTO jours_feries_vacances (evenement_id, description, date_debut, date_fin, zones, annee_scolaire, type_evenement)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(query, (
        vacance['evenement_id'],  # UUID directement
        vacance['description'],
        vacance['date_debut'],
        vacance['date_fin'],
        vacance['zones'],
        vacance['annee_scolaire'],
        vacance['type_evenement']
    ))

def get_vacance(session, evenement_id):
    try:
        query = "SELECT * FROM jours_feries_vacances WHERE evenement_id = %s"
        row = session.execute(query, (evenement_id,)).one()
        if row:
            # Convertir la ligne en dictionnaire
            return {col: getattr(row, col) for col in row._fields}
        return None
    except Exception as e:
        print(f"Error in get_vacance: {e}")
        raise

def update_vacance(session, evenement_id, vacance):
    try:
        query = """
            UPDATE jours_feries_vacances
            SET description = %s, date_debut = %s, date_fin = %s, zones = %s, annee_scolaire = %s, type_evenement = %s
            WHERE evenement_id = %s
        """
        session.execute(query, (
            vacance['description'],
            vacance['date_debut'],
            vacance['date_fin'],
            vacance['zones'],
            vacance['annee_scolaire'],
            vacance['type_evenement'],
            evenement_id
        ))
        return get_vacance(session, evenement_id)  # Retourner l'événement mis à jour
    except Exception as e:
        print(f"Error in update_vacance: {e}")
        raise


import logging

logger = logging.getLogger(__name__)

def delete_vacance(session, evenement_id):
    logger.info(f"Tentative de suppression de l'événement : {evenement_id}")
    try:
        query = "DELETE FROM jours_feries_vacances WHERE evenement_id = %s"
        session.execute(query, (evenement_id,))
        deleted = get_vacance(session, evenement_id) is None
        logger.info(f"Événement supprimé : {evenement_id}") if deleted else logger.warning(f"Échec de suppression : {evenement_id}")
        return deleted
    except Exception as e:
        logger.error(f"Erreur lors de la suppression : {str(e)}")
        raise
