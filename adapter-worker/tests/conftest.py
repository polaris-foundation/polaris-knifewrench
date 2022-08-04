import json
import os
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest
from kombu import Connection, Message

from dhos_knifewrench_adapter_worker.config import Config
from dhos_knifewrench_adapter_worker.knifewrench import ErrorQueueConsumer


@pytest.fixture()
def knifewrench_sample_env_vars() -> Dict[str, str]:
    return {
        "RABBITMQ_HOST": "localhost",
        "RABBITMQ_USERNAME": "user",
        "RABBITMQ_PASSWORD": "password",
        "DHOS_KNIFEWRENCH_API_HOST": "http://dhos-knifewrench-api",
    }


@pytest.fixture()
def error_message() -> Message:
    message: Message = Message()
    message.headers = {
        "x-death": [
            {
                "time": "2019-06-11 12:50:56",
                "count": 1,
                "queue": "dhos-pdf-adapter-task-queue",
                "reason": "rejected",
                "exchange": "dhos",
                "routing-keys": ["dhos.DM000008"],
            }
        ],
        "x-first-death-queue": "dhos-pdf-adapter-task-queue",
        "x-first-death-reason": "rejected",
        "x-first-death-exchange": "dhos",
    }
    message.body = json.dumps(
        {
            "patient": {
                "dob": "1973-01-03",
                "dod": None,
                "sex": None,
                "uuid": "ac679787-7e22-41b9-a55e-9bb82821acf2",
                "record": {
                    "uuid": "3165c3b1-381f-45b6-80ca-77d2a07ae00d",
                    "notes": [],
                    "visits": [],
                    "created": "2019-06-11T12:50:51.881Z",
                    "history": {
                        "uuid": "d1c2e03b-f207-460f-93db-1f807fc71579",
                        "parity": None,
                        "created": "2019-06-11T12:50:51.880Z",
                        "modified": "2019-06-11T12:50:51.880Z",
                        "gravidity": None,
                        "created_by": {
                            "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "last_name": "StandardClinician",
                            "first_name": "Postman Clinician",
                        },
                        "modified_by": {
                            "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "last_name": "StandardClinician",
                            "first_name": "Postman Clinician",
                        },
                    },
                    "modified": "2019-06-11T12:50:51.881Z",
                    "diagnoses": [],
                    "created_by": {
                        "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                        "last_name": "StandardClinician",
                        "first_name": "Postman Clinician",
                    },
                    "modified_by": {
                        "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                        "last_name": "StandardClinician",
                        "first_name": "Postman Clinician",
                    },
                    "pregnancies": [],
                },
                "created": "2019-06-11T12:50:51.889Z",
                "modified": "2019-06-11T12:50:51.889Z",
                "ethnicity": None,
                "last_name": "Patient",
                "locations": [],
                "bookmarked": False,
                "created_by": {
                    "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                    "last_name": "StandardClinician",
                    "first_name": "Postman Clinician",
                },
                "first_name": "Postman Patient",
                "nhs_number": "0257451831",
                "dh_products": [
                    {
                        "uuid": "11fdbcb0-3c5d-4c90-8c11-7ad98a1f6076",
                        "created": "2019-06-11T12:50:51.880Z",
                        "modified": "2019-06-11T12:50:51.880Z",
                        "created_by": {
                            "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "last_name": "StandardClinician",
                            "first_name": "Postman Clinician",
                        },
                        "closed_date": None,
                        "modified_by": {
                            "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "last_name": "StandardClinician",
                            "first_name": "Postman Clinician",
                        },
                        "opened_date": "2019-01-09",
                        "product_name": "SEND",
                        "closed_reason": None,
                        "closed_reason_other": None,
                    }
                ],
                "modified_by": {
                    "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                    "last_name": "StandardClinician",
                    "first_name": "Postman Clinician",
                },
                "other_notes": None,
                "phone_number": None,
                "email_address": None,
                "allowed_to_text": False,
                "ethnicity_other": None,
                "hospital_number": "560257451831",
                "terms_agreement": None,
                "allowed_to_email": None,
                "clinician_bookmark": False,
                "personal_addresses": [],
                "has_been_bookmarked": False,
                "highest_education_level": None,
                "accessibility_considerations": [],
                "highest_education_level_other": None,
                "accessibility_considerations_other": None,
            },
            "location": {
                "uuid": "cdc1a860-7709-4746-adf3-88d702750d3f",
                "active": False,
                "region": None,
                "country": None,
                "created": "2019-06-11T12:50:52.011Z",
                "parents": [],
                "locality": None,
                "modified": "2019-06-11T12:50:53.269Z",
                "ods_code": "1560257451983",
                "postcode": None,
                "bookmarked": [],
                "created_by": {
                    "uuid": "dhos-robot",
                    "last_name": "system",
                    "first_name": "system",
                },
                "dh_products": [
                    {
                        "uuid": "5578f839-7ee7-40c9-9a70-f3b307c8ed97",
                        "created": "2019-06-11T12:50:52.011Z",
                        "closed_date": None,
                        "opened_date": "2019-01-09",
                        "product_name": "SEND",
                    }
                ],
                "modified_by": {
                    "uuid": "dhos-robot",
                    "last_name": "system",
                    "first_name": "system",
                },
                "display_name": "Postman location",
                "location_type": "225746001",
                "address_line_1": None,
                "address_line_2": None,
                "address_line_3": None,
                "address_line_4": None,
                "clinician_bookmark": False,
            },
            "encounter": {
                "uuid": "c3b34001-59dd-4406-9fcd-c694f174461c",
                "created": "2019-06-11T12:50:52.130Z",
                "deleted_at": None,
                "dh_product": [
                    {
                        "uuid": "11fdbcb0-3c5d-4c90-8c11-7ad98a1f6076",
                        "created": "2019-06-11T12:50:51.880Z",
                    }
                ],
                "spo2_scale": 2,
                "admitted_at": "2019-06-11T12:50:52.076Z",
                "discharged_at": "2019-06-11T12:50:53.077Z",
                "location_uuid": "cdc1a860-7709-4746-adf3-88d702750d3f",
                "encounter_type": "INPATIENT",
                "epr_encounter_id": None,
                "spo2_scale_history": [
                    {
                        "changed_by": {
                            "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "last_name": "StandardClinician",
                            "first_name": "Postman Clinician",
                        },
                        "spo2_scale": 2,
                        "changed_time": "2019-06-11T12:50:52.416Z",
                        "previous_spo2_scale": 1,
                    }
                ],
                "patient_record_uuid": "3165c3b1-381f-45b6-80ca-77d2a07ae00d",
            },
            "aggregation_time": "2019-06-11T12:50:53.394+00:00",
            "observation_sets": [
                {
                    "uuid": "10ce1ad3-5e5b-45a9-8026-e19afa2641cf",
                    "created": "2019-06-11T12:50:52.528Z",
                    "ranking": "000010,2019-06-11T12:50:52.490Z",
                    "modified": "2019-06-11T12:50:52.693Z",
                    "empty_set": None,
                    "created_by": {
                        "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                        "last_name": "StandardClinician",
                        "first_name": "Postman Clinician",
                    },
                    "is_partial": True,
                    "spo2_scale": 2,
                    "modified_by": "dhos-observations-adapter-worker",
                    "record_time": "2019-06-11T12:50:52.490Z",
                    "score_value": 0,
                    "encounter_id": "c3b34001-59dd-4406-9fcd-c694f174461c",
                    "observations": [
                        {
                            "uuid": "d316f22e-e6d6-4d14-991f-1b3b47a02bc5",
                            "created": "2019-06-11T12:50:52.526Z",
                            "modified": "2019-06-11T12:50:52.695Z",
                            "created_by": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "modified_by": "dhos-observations-adapter-worker",
                            "score_value": 0,
                            "measured_time": "2019-06-11T12:50:52.490Z",
                            "patient_refused": False,
                            "observation_type": "temperature",
                            "observation_unit": "celsius",
                            "observation_value": 38,
                            "observation_string": None,
                            "observation_metadata": None,
                        }
                    ],
                    "score_string": "0",
                    "score_system": "news2",
                    "score_severity": "low",
                    "obx_abnormal_flags": "N",
                    "obx_reference_range": "0-4",
                    "time_next_obs_set_due": "2019-06-12T00:50:52.490Z",
                    "monitoring_instruction": "routine_monitoring",
                },
                {
                    "uuid": "a7e27e7b-b368-4c55-9b1d-bebaef7bd523",
                    "created": "2019-06-11T12:50:53.015Z",
                    "ranking": "010110,2019-06-11T12:50:52.490Z",
                    "modified": "2019-06-11T12:50:53.154Z",
                    "empty_set": None,
                    "created_by": {
                        "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                        "last_name": "StandardClinician",
                        "first_name": "Postman Clinician",
                    },
                    "is_partial": True,
                    "spo2_scale": 2,
                    "modified_by": "dhos-observations-adapter-worker",
                    "record_time": "2019-06-11T12:50:52.490Z",
                    "score_value": 1,
                    "encounter_id": "c3b34001-59dd-4406-9fcd-c694f174461c",
                    "observations": [
                        {
                            "uuid": "0be64754-fbf1-451f-abf8-b4f7a3ec51ba",
                            "created": "2019-06-11T12:50:53.013Z",
                            "modified": "2019-06-11T12:50:53.156Z",
                            "created_by": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "modified_by": "dhos-observations-adapter-worker",
                            "score_value": 1,
                            "measured_time": "2019-06-11T12:50:52.490Z",
                            "patient_refused": False,
                            "observation_type": "temperature",
                            "observation_unit": "celsius",
                            "observation_value": 39,
                            "observation_string": None,
                            "observation_metadata": None,
                        }
                    ],
                    "score_string": "1",
                    "score_system": "news2",
                    "score_severity": "low",
                    "obx_abnormal_flags": "N",
                    "obx_reference_range": "0-4",
                    "time_next_obs_set_due": "2019-06-11T16:50:52.490Z",
                    "monitoring_instruction": "low_monitoring",
                },
                {
                    "uuid": "bdb00a4d-7cc6-42aa-af5d-42887feeb232",
                    "created": "2019-06-11T12:50:52.975Z",
                    "ranking": "000010,2019-06-11T12:50:52.490Z",
                    "modified": "2019-06-11T12:50:53.111Z",
                    "empty_set": None,
                    "created_by": {
                        "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                        "last_name": "StandardClinician",
                        "first_name": "Postman Clinician",
                    },
                    "is_partial": True,
                    "spo2_scale": 2,
                    "modified_by": "dhos-observations-adapter-worker",
                    "record_time": "2019-06-11T12:50:52.490Z",
                    "score_value": 0,
                    "encounter_id": "c3b34001-59dd-4406-9fcd-c694f174461c",
                    "observations": [
                        {
                            "uuid": "6a6aac7b-0566-49ba-b4f4-b9cbc7c03493",
                            "created": "2019-06-11T12:50:52.973Z",
                            "modified": "2019-06-11T12:50:53.113Z",
                            "created_by": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "modified_by": "dhos-observations-adapter-worker",
                            "score_value": 0,
                            "measured_time": "2019-06-11T12:50:52.490Z",
                            "patient_refused": False,
                            "observation_type": "temperature",
                            "observation_unit": "celsius",
                            "observation_value": 38,
                            "observation_string": None,
                            "observation_metadata": None,
                        }
                    ],
                    "score_string": "0",
                    "score_system": "news2",
                    "score_severity": "low",
                    "obx_abnormal_flags": "N",
                    "obx_reference_range": "0-4",
                    "time_next_obs_set_due": "2019-06-12T00:50:52.490Z",
                    "monitoring_instruction": "routine_monitoring",
                },
                {
                    "uuid": "04d2bb83-ce15-44e9-b298-5f24f183efb2",
                    "created": "2019-06-11T12:50:52.249Z",
                    "ranking": "000010,2019-06-11T12:50:52.204Z",
                    "modified": "2019-06-11T12:50:52.496Z",
                    "empty_set": None,
                    "created_by": {
                        "uuid": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                        "last_name": "StandardClinician",
                        "first_name": "Postman Clinician",
                    },
                    "is_partial": True,
                    "spo2_scale": 1,
                    "modified_by": "dhos-observations-adapter-worker",
                    "record_time": "2019-06-11T12:50:52.204Z",
                    "score_value": 0,
                    "encounter_id": "c3b34001-59dd-4406-9fcd-c694f174461c",
                    "observations": [
                        {
                            "uuid": "a4f91843-e732-4107-b6a0-e69a7179eb72",
                            "created": "2019-06-11T12:50:52.247Z",
                            "modified": "2019-06-11T12:50:52.497Z",
                            "created_by": "fe61f8f4-2a1a-4a6f-bea7-57a36aabf6cf",
                            "modified_by": "dhos-observations-adapter-worker",
                            "score_value": 0,
                            "measured_time": "2019-06-11T12:50:52.204Z",
                            "patient_refused": False,
                            "observation_type": "temperature",
                            "observation_unit": "celsius",
                            "observation_value": 38,
                            "observation_string": None,
                            "observation_metadata": None,
                        }
                    ],
                    "score_string": "0",
                    "score_system": "news2",
                    "score_severity": "low",
                    "obx_abnormal_flags": "N",
                    "obx_reference_range": "0-4",
                    "time_next_obs_set_due": "2019-06-12T00:50:52.204Z",
                    "monitoring_instruction": "routine_monitoring",
                },
            ],
        }
    )

    return message


@pytest.fixture()
def systemauth_sample_jwt() -> str:
    return "YV9tb2NrX2p3dA=="


@pytest.fixture()
def knifewrench_sample_config(knifewrench_sample_env_vars: Dict) -> Config:
    with patch.dict(os.environ, knifewrench_sample_env_vars):
        return Config()


@pytest.fixture()
def knifewrench_200(requests_mock: Any, knifewrench_sample_config: Config) -> MagicMock:
    _url = f"{knifewrench_sample_config.DHOS_KNIFEWRENCH_API}/dhos/v1/amqp_message"
    return requests_mock.post(_url, text="", status_code=200)


@pytest.fixture()
def knifewrench_503(requests_mock: Any, knifewrench_sample_config: Config) -> MagicMock:
    _url = f"{knifewrench_sample_config.DHOS_KNIFEWRENCH_API}/dhos/v1/amqp_message"
    return requests_mock.post(_url, text="", status_code=503)


@pytest.fixture
def mock_api_jwt(mocker: Any, systemauth_sample_jwt: str) -> Any:
    from dhos_knifewrench_adapter_worker import auth_token

    return mocker.patch.object(
        auth_token, "get_api_jwt", return_value=systemauth_sample_jwt
    )


@pytest.fixture()
def knifewrench_consumer(knifewrench_sample_env_vars: Dict) -> ErrorQueueConsumer:
    with patch.dict(os.environ, knifewrench_sample_env_vars):
        return ErrorQueueConsumer(Connection(), [])
