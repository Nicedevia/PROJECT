from uuid import uuid4
from app.models.schemas import JourFerie, Meteo, Limitation, Vitesse
from app.db.cassandra_session import session
from app.crud.jour_ferie import create_jour_ferie, get_jour_ferie, update_jour_ferie, delete_jour_ferie
from app.crud.meteo import create_meteo, get_meteo, update_meteo, delete_meteo
from app.crud.limitation import create_limitation, get_limitation, update_limitation, delete_limitation
from app.crud.vitesse import create_vitesse, get_vitesse, update_vitesse, delete_vitesse
from datetime import datetime

def test_crud_operations():
    try:
        # Test CRUD pour la table jour_ferie
        print("Testing jour_ferie table...")
        jour_ferie = JourFerie(date=datetime(2024, 11, 7), description="Fête Nationale", zone_1=True, zone_2=False, zone_3=True)
        create_jour_ferie(jour_ferie)
        result = get_jour_ferie(jour_ferie.date)
        assert result is not None, "Failed to insert jour_ferie"
        
        # Update test
        update_jour_ferie(jour_ferie.date, "Nouvelle Description", True, True, False)
        result = get_jour_ferie(jour_ferie.date)
        assert result is not None and result.description == "Nouvelle Description", "Failed to update jour_ferie"
        
        # Delete test
        delete_jour_ferie(jour_ferie.date)
        result = get_jour_ferie(jour_ferie.date)
        assert result is None, "Failed to delete jour_ferie"

        # Test CRUD pour la table meteo
        print("Testing meteo table...")
        capteur_id_meteo = uuid4()
        meteo = Meteo(date=datetime(2024, 11, 7), capteur_id=capteur_id_meteo, visibilite=10.5, precipitation=5.0)
        create_meteo(meteo)
        result = get_meteo(capteur_id_meteo, meteo.date)
        assert result is not None, "Failed to insert meteo"
        
        # Update test
        update_meteo(capteur_id_meteo, meteo.date, 12.0, 3.0)
        result = get_meteo(capteur_id_meteo, meteo.date)
        assert result is not None and result.visibilite == 12.0, "Failed to update meteo"
        
        # Delete test
        delete_meteo(capteur_id_meteo, meteo.date)
        result = get_meteo(capteur_id_meteo, meteo.date)
        assert result is None, "Failed to delete meteo"

        # Test CRUD pour la table limitation
        print("Testing limitation table...")
        capteur_id_limitation = uuid4()
        limitation = Limitation(date=datetime(2024, 11, 7), capteur_id=capteur_id_limitation, limitation=120.0)
        create_limitation(limitation)
        result = get_limitation(capteur_id_limitation, limitation.date)
        assert result is not None, "Failed to insert limitation"
        
        # Update test
        update_limitation(capteur_id_limitation, limitation.date, 100.0)
        result = get_limitation(capteur_id_limitation, limitation.date)
        assert result is not None and result.limitation == 100.0, "Failed to update limitation"
        
        # Delete test
        delete_limitation(capteur_id_limitation, limitation.date)
        result = get_limitation(capteur_id_limitation, limitation.date)
        assert result is None, "Failed to delete limitation"

        # Test CRUD pour la table vitesse
        print("Testing vitesse table...")
        capteur_id_vitesse = uuid4()
        vitesse = Vitesse(date=datetime(2024, 11, 7), capteur_id=capteur_id_vitesse, vitesse=90.0)
        create_vitesse(vitesse)
        result = get_vitesse(capteur_id_vitesse, datetime(2024, 11, 7), datetime(2024, 11, 7))
        assert result is not None and len(result) > 0, "Failed to insert vitesse"
        
        # Update test
        update_vitesse(capteur_id_vitesse, vitesse.date, 110.0)
        result = get_vitesse(capteur_id_vitesse, datetime(2024, 11, 7), datetime(2024, 11, 7))
        assert result is not None and result[0].vitesse == 110.0, "Failed to update vitesse"
        
        # Delete test
        delete_vitesse(capteur_id_vitesse, vitesse.date)
        result = get_vitesse(capteur_id_vitesse, datetime(2024, 11, 7), datetime(2024, 11, 7))
        assert result is not None and len(result) == 0, "Failed to delete vitesse"

        print("All CRUD tests passed successfully!")

    except AssertionError as e:
        print(f"Test failed: {e}")

    except Exception as e:
        print(f"Unexpected error during testing: {e}")

# Appel de la fonction de test
if __name__ == "__main__":
    test_crud_operations()
