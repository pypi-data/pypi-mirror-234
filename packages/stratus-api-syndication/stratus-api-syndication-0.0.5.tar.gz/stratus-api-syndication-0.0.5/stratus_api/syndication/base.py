MAPPER = None
CONTRACT = None


def extract_attributes(body: dict) -> tuple:
    """Convenience function to extract common attributes from PubSub messages

    :param body:
    :return: Tuple of external_id, external service name, and the promise results
    """
    import base64
    import json

    message = body.get('message', dict())
    attributes = message.get('attributes', dict())
    action = attributes['action']
    service_name = attributes['service_name']
    object_type = attributes.get('object_type', attributes.get('collection_name'))
    data = json.loads(base64.b64decode(message['data']).decode('utf-8'))
    if 'properties' in data.keys() and 'id' in data.keys():
        object_id = data['id']
        properties = data['properties']
    else:
        object_id = attributes['object_id']
        properties = data
    return service_name, object_type, action, object_id, properties, attributes['timestamp']


def configure_syndication_mappings(subscriptions, refresh=False):
    global MAPPER
    if MAPPER is None or refresh:
        MAPPER = dict()
        for subscription in subscriptions:
            if MAPPER is None or subscription['service_name'] not in MAPPER.keys():
                MAPPER[subscription['service_name']] = dict()
            MAPPER[subscription['service_name']][subscription['object_type']] = subscription['function']
    return MAPPER


def process_syndication_update_request(body):
    global MAPPER
    service_name, object_type, action, object_id, properties, timestamp = extract_attributes(body=body)
    MAPPER[service_name][object_type](action=action, object_id=object_id, properties=properties, timestamp=timestamp)
    return dict(active=True)


def validate_payload(properties, object_contract):
    import jsonschema
    try:
        jsonschema.validate(properties, object_contract)
    except jsonschema.ValidationError:
        return False
    else:
        return True


def publish_object_update(object_id, object_type, properties, action, service_name=None, project_id=None):
    from stratus_api.events.pubsub import push_to_topic, generate_topic_name
    from stratus_api.core.exceptions import ApiError
    assert action in {'add', 'update', 'delete'}
    global CONTRACT
    if CONTRACT is not None and service_name in CONTRACT.keys() and CONTRACT[service_name].get(object_type):
        object_contract = CONTRACT[service_name][object_type]
        if not validate_payload(properties=properties, object_contract=object_contract):
            raise ApiError('Payload not valid with defined contract: ' + str(properties))

    push_to_topic(
        topic_name=generate_topic_name(name=object_type, service_name=service_name),
        attributes=format_object_update_attibutes(
            object_id=object_id, object_type=object_type, action=action, service_name=service_name,
            project_id=project_id
        ), payload=properties
    )


def format_object_update_attibutes(object_id, object_type, action, service_name=None, project_id=None):
    from datetime import datetime
    from stratus_api.core.settings import get_settings
    if service_name is None:
        service_name = get_settings()['service_name']
    if project_id is None:
        project_id = get_settings()['project_id']
    return dict(
        object_id=object_id,
        project_id=project_id,
        service_name=service_name,
        timestamp=str(int(datetime.utcnow().timestamp())),
        action=action,
        object_type=object_type,
    )


def define_syndication_contracts(contracts, refresh=False):
    global CONTRACT
    if CONTRACT is None or refresh:
        CONTRACT = dict()
        for object_contract in contracts:
            if object_contract['service_name'] not in CONTRACT.keys():
                CONTRACT[object_contract['service_name']] = dict()
            CONTRACT[object_contract['service_name']][object_contract['object_type']] = object_contract['contract_json']
    return CONTRACT


def get_syndication_contract_request(service_name, object_type):
    global CONTRACT

    result_contract = dict()
    if CONTRACT and service_name in CONTRACT.keys() and CONTRACT[service_name].get(object_type):
        result_contract = CONTRACT[service_name][object_type]
    return dict(active=True, response=result_contract)
