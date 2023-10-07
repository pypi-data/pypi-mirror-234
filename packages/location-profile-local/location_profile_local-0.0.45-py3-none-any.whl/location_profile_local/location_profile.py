import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))

from circles_local_database_python.generic_crud import GenericCRUD
from dotenv import load_dotenv
from typing import List
from logger_local.LoggerComponentEnum import LoggerComponentEnum
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

LOCATION_PROFILE_LOCAL_COMPONENT_ID = 167
COMPONENT_NAME = 'location_profile_local/location_profile.py'

object_to_insert = {
    'payload': 'method get_location_id_by_profile_id in location-profile-local',
    'component_id': LOCATION_PROFILE_LOCAL_COMPONENT_ID,
    'component_name': COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'sahar.g@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)

class Location:
    def __init__(self, location_id, profile_id):
        self.profile_id = profile_id 
        self.location_id = location_id

    def __dict__(self):
        return {
            'profile_id': self.profile_id,
            'location_id': self.location_id
        }

class LocationProfiles(GenericCRUD):
    def __init__(self):
        INIT_METHOD_NAME = '__init__'
        logger.start(INIT_METHOD_NAME)
        super().__init__(schema_name="location_profile")
        logger.end(INIT_METHOD_NAME)

    def get_last_location_id_by_profile_id(self, profile_id: int) -> int:
        GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME = "get_last_location_id_by_profile_id"
        logger.start(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})
        location_id = self.select_multi_by_where(view_table_name="location_profile_view", select_clause_value="location_id", where=f"profile_id = {profile_id}",limit=1,order_by="start_timestamp desc")
        logger.end(GET_LAST_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME,
                   object={'location_id': location_id})
        return location_id[0]

    def get_location_ids_by_profile_id(self, profile_id: int) -> List[Location]:
        GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME = "get_location_ids_by_profile_id"
        logger.start(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})
        location_ids = self.select_multi_by_id(view_table_name="location_profile_view", select_clause_value="location_id",
                                   id_column_name="profile_id", id_column_value=profile_id)
        
        location_ids = [Location(location_id=location_id, profile_id=profile_id) for location_id in location_ids]
        location_dicts = [loc.__dict__() for loc in location_ids]
        logger.end(GET_LOCATION_IDS_BY_PROFILE_ID_METHOD_NAME,
                   object={'location_ids': location_dicts})
        return location_ids

    def insert_location_profile(self, profile_id: int, location_id: int, lang_code: str = 'en', title: str = 'Home', title_approved=True):
        INSERT_LOCATION_PROFILE_METHOD_NAME = 'insert_location_profile'
        logger.start(INSERT_LOCATION_PROFILE_METHOD_NAME,
                     object={"location_id": location_id})
        data = {
            "profile_id": profile_id,
            "location_id": location_id
        }
        self.insert(table_name="location_profile_table", json_data=data)
        reaction_id = self.cursor.lastrowid()
        data = {
            "location_profile_id": reaction_id,
            "lang_code": lang_code,
            "title": title,
            "title_approved": title_approved
        }
        self.insert(table_name="location_profile_ml_table", json_data=data)
        logger.end(INSERT_LOCATION_PROFILE_METHOD_NAME)

