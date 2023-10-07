from logger_local.LoggerComponentEnum import LoggerComponentEnum

class LocationProfileLocalConstants:

    LOCATION_PROFILE_LOCAL_COMPONENT_ID = 167
    COMPONENT_NAME = 'location-profile-local'

    OBJECT_FOR_LOGGER_CODE = {
        'component_id': LOCATION_PROFILE_LOCAL_COMPONENT_ID,
        'component_name': COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': 'tal.g@circ.zone'
    }

    OBJECT_FOR_LOGGER_TEST = {
        'component_id': LOCATION_PROFILE_LOCAL_COMPONENT_ID,
        'component_name': COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': 'tal.g@circ.zone'
    }