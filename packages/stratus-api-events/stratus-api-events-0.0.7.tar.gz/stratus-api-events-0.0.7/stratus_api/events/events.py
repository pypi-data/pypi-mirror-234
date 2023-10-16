__schemas__ = None


def publish_event(topic_name, attributes, event_type, payload, status=None):
    """ Publishes a validated payload to a topic
    :param topic_name: topic name
    :param attributes: attributes
    :param event_type: event type
    :param payload: payload
    :param status: status
    :return: topic name, payload """
    from .pubsub import push_to_topic
    # validate_event_schema(topic_name=topic_name, data=payload, status=status)
    push_to_topic(topic_name=topic_name, attributes=attributes, payload=payload)
    return topic_name, payload


# def get_topic_schemas(refresh=False):
#     global __schemas__
#     if __schemas__ is None or refresh:
#         __schemas__ = dict()
#     return __schemas__
#
#
# def get_topic_schema(topic_name):
#     schemas = get_topic_schemas()
#     return schemas.get(topic_name)
#
#
# def validate_event_schema(topic_name, data, status=None):
#     from jsonschema import validate
#     schema = get_topic_schema(topic_name=topic_name)
#     validate(instance=data, schema=schema)
#     return True
