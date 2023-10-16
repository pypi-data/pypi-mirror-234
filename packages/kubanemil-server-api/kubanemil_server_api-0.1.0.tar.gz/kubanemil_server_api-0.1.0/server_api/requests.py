import logging
import requests
from json import loads
from .config import SERVER_API_HOST, SERVER_API_PORT
from .models import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationUpdate,
    EventCreate,
    EventRead,
    EventUpdate,
    MetricCreate,
    MetricRead,
    MetricUpdate,
    ModelCreate,
    ModelRead,
    ModelUpdate,
    PipelineCreate,
    PipelineRead,
    PipelineUpdate,
)

server_api_url = f"http://{SERVER_API_HOST}:{SERVER_API_PORT}"

class ServerAPIException(Exception):
    pass

def handle_response(response: requests.Response):
    if response.status_code != 200:
        logging.error(f"response ({response.status_code}): {response.json()}")
        raise ServerAPIException(f"response ({response.status_code}): {response.json()}")

def get_application(application_id: str) -> ApplicationRead:
    response = requests.get(f"{server_api_url}/application/{application_id}")
    handle_response(response)
    application_data = response.json()
    return ApplicationRead(**application_data)

def get_applications_for_account(account_id: str) -> list[ApplicationRead]:
    response = requests.get(
        f"{server_api_url}/application", headers={"account_id": account_id}
    )
    handle_response(response)
    application_data = response.json()
    return [ApplicationRead(**x) for x in application_data]

def create_application(application_create: ApplicationCreate) -> ApplicationRead:
    response = requests.post(
        f"{server_api_url}/application", json=loads(application_create.json())
    )
    handle_response(response)
    application_data = response.json()
    return ApplicationRead(**application_data)

def update_application(
    application_id: str, application_update: ApplicationUpdate
) -> ApplicationRead:
    response = requests.put(
        f"{server_api_url}/application/{application_id}", json=loads(application_update.json())
    )
    handle_response(response)
    application_data = response.json()
    return ApplicationRead(**application_data)


def get_event(event_id: str) -> EventRead:
    response = requests.get(f"{server_api_url}/event/{event_id}")
    handle_response(response)
    event_data = response.json()
    return EventRead(**event_data)

def get_events_for_application(application_id: str) -> list[EventRead]:
    response = requests.get(
        f"{server_api_url}/event", params={"application_id": application_id}
    )
    handle_response(response)
    event_data = response.json()
    return [EventRead(**x) for x in event_data]

def create_event(event_create: EventCreate) -> EventRead:
    response = requests.post(
        f"{server_api_url}/event", json=loads(event_create.json())
    )
    handle_response(response)
    event_data = response.json()
    return EventRead(**event_data)

def update_event(event_id: str, event_update: EventUpdate) -> EventRead:
    response = requests.put(
        f"{server_api_url}/event/{event_id}", json=loads(event_update.json())
    )
    handle_response(response)
    event_data = response.json()
    return EventRead(**event_data)


def get_metric(metric_id: str) -> MetricRead:
    response = requests.get(f"{server_api_url}/metric/{metric_id}")
    handle_response(response)
    metric_data = response.json()
    return MetricRead(**metric_data)

def get_metrics_for_application(application_id: str) -> list[MetricRead]:
    response = requests.get(
        f"{server_api_url}/metric", params={"application_id": application_id}
    )
    handle_response(response)
    metric_data = response.json()
    return [MetricRead(**x) for x in metric_data]

def create_metric(metric_create: MetricCreate) -> MetricRead:
    response = requests.post(
        f"{server_api_url}/metric", json=loads(metric_create.json())
    )
    handle_response(response)
    metric_data = response.json()
    return MetricRead(**metric_data)

def update_metric(metric_id: str, metric_update: MetricUpdate) -> MetricRead:
    response = requests.put(
        f"{server_api_url}/metric/{metric_id}", json=loads(metric_update.json())
    )
    handle_response(response)
    metric_data = response.json()
    return MetricRead(**metric_data)


def get_pipeline(pipeline_id: str) -> PipelineRead:
    response = requests.get(f"{server_api_url}/pipeline/{pipeline_id}")
    handle_response(response)
    pipeline_data = response.json()
    return PipelineRead(**pipeline_data)


def create_pipeline(pipeline_create: PipelineCreate) -> PipelineRead:
    response = requests.post(
        f"{server_api_url}/pipeline", json=loads(pipeline_create.json())
    )
    handle_response(response)
    pipeline_data = response.json()
    return PipelineRead(**pipeline_data)


def update_pipeline(pipeline_id: str, pipeline_update: PipelineUpdate) -> PipelineRead:
    response = requests.put(
        f"{server_api_url}/pipeline/{pipeline_id}", json=loads(pipeline_update.json())
    )
    handle_response(response)
    pipeline_data = response.json()
    return PipelineRead(**pipeline_data)


def get_model(model_id: str) -> ModelRead:
    response = requests.get(f"{server_api_url}/model/{model_id}")
    handle_response(response)
    model_data = response.json()
    return ModelRead(**model_data)


def get_models_for_pipeline(pipeline_id: str) -> list[ModelRead]:
    response = requests.get(
        f"{server_api_url}/model", params={"pipeline_id": pipeline_id}
    )
    handle_response(response)
    model_data = response.json()
    return [ModelRead(**x) for x in model_data]


def get_pipelines_for_application(application_id: str) -> list[PipelineRead]:
    response = requests.get(
        f"{server_api_url}/pipeline", params={"application_id": application_id}
    )
    handle_response(response)
    pipeline_data = response.json()
    return [PipelineRead(**x) for x in pipeline_data]


def get_models_for_event(event_id: str) -> list[ModelRead]:
    response = requests.get(
        f"{server_api_url}/model", params={"event_id": event_id}
    )
    handle_response(response)
    model_data = response.json()
    return [ModelRead(**x) for x in model_data]

def get_models_for_metric(metric_id: str) -> list[ModelRead]:
    response = requests.get(
        f"{server_api_url}/model", params={"metric_id": metric_id}
    )
    handle_response(response)
    model_data = response.json()
    return [ModelRead(**x) for x in model_data]

def create_model(model_create: ModelCreate) -> ModelRead:
    response = requests.post(
        f"{server_api_url}/model", json=loads(model_create.json())
    )
    handle_response(response)
    model_data = response.json()
    return ModelRead(**model_data)

def update_model(model_id: str, model_update: ModelUpdate) -> ModelRead:
    response = requests.put(
        f"{server_api_url}/model/{model_id}", json=loads(model_update.json())
    )
    handle_response(response)
    model_data = response.json()
    return ModelRead(**model_data)
