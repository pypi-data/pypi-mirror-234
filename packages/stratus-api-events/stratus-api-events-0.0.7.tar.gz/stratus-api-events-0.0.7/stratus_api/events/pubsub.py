__publisher__ = None
__subscriber__ = None


def create_publisher(refresh=False, credentials=None):
    """ Creates a publisher client
    :param refresh: refresh flag
    :param credentials: credentials
    :return: publisher client """
    from google.cloud.pubsub import PublisherClient
    global __publisher__
    if __publisher__ is None or refresh:
        __publisher__ = PublisherClient()
    return __publisher__


def create_subscriber(refresh=False, credentials=None):
    """ Creates a subscriber client
    :param refresh: refresh flag
    :param credentials: credentials
    :return: subscriber client """
    from google.cloud.pubsub import SubscriberClient
    global __subscriber__
    if __subscriber__ is None or refresh:
        __subscriber__ = SubscriberClient()
    return __subscriber__


def format_pubsub_name(name, project_id=None, pubsub_type='topic'):
    """ Gets the formatted pubsub name
    :param name: name
    :param project_id: project id
    :param pubsub_type: pubsub entity type (topic or subscription)
    :return: formatted pubsub name """
    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    mapping = dict(topic='topics', subscription='subscriptions')
    if pubsub_type not in mapping.keys():
        raise ValueError('Invalid pubsub_type. pubsub_type must be topic or subscription')
    if not project_id:
        project_id = app_settings['project_id']
    return 'projects/{0}/{1}/{2}'.format(project_id, mapping[pubsub_type], name.split('/')[-1])


def get_topic(name, project_id=None):
    """ Gets the topic object
    :param name: topic name
    :param project_id: project id
    :return: topic object """
    publisher = create_publisher()
    topic_name = format_pubsub_name(name=name, pubsub_type='topic', project_id=project_id)
    topic = publisher.get_topic(topic=topic_name)
    return topic


def create_topic(name, project_id=None) -> tuple:
    """ Creates a topic
    :param name: topic name
    :param project_id: project id
    :return: topic name, created timestamp """
    from google.api_core.exceptions import Conflict
    from stratus_api.core.logs import get_logger
    logger = get_logger()
    publisher = create_publisher()
    topic_name = format_pubsub_name(name=name, pubsub_type='topic', project_id=project_id)
    created = False
    try:
        publisher.create_topic(name=topic_name)
    except Conflict as e:
        logger.warning(e)
    else:
        created = True
    return topic_name, created


def delete_topic(name, project_id=None):
    """ Deletes a topic
    :param name: topic name
    :param project_id: project id
    :return: formatted topic name, success flag """
    publisher = create_publisher()
    topic_name = format_pubsub_name(name=name, pubsub_type='topic', project_id=project_id)
    publisher.delete_topic(topic=topic_name)
    return topic_name, True


def get_subscription(name, project_id=None):
    """ Gets the subscription object
    :param name: subscription name
    :param project_id: project id
    :return: subscription object """
    subscriber = create_subscriber()
    subscription_name = format_pubsub_name(name=name, pubsub_type='subscription', project_id=project_id)
    subscription = subscriber.get_subscription(subscription=subscription_name)
    return subscription


def delete_subscription(name, project_id=None):
    """ Deletes a subscription
    :param name: subscription name
    :param project_id: project id
    :return: success flag """
    subscriber = create_subscriber()
    subscription_name = format_pubsub_name(name=name, pubsub_type='subscription', project_id=project_id)
    subscriber.delete_subscription(subscription=subscription_name)
    return True


def create_subscription(topic, subscription, path=None, project_id=None, expiration_in_days: int = None):
    """ Creates a subscription
    :param topic: topic name
    :param subscription: subscription name
    :param path: path
    :param project_id: project id
    :param expiration_in_days: expiration in days
    :return: subscriber client, created timestamp """
    from google.api_core.exceptions import Conflict
    from google.protobuf.duration_pb2 import Duration
    from google.pubsub_v1 import Subscription
    from stratus_api.core.logs import get_logger
    from stratus_api.core.settings import get_settings
    from urllib.parse import urljoin
    from datetime import timedelta
    logger = get_logger()
    app_settings = get_settings(settings_type='app')
    subscriber = create_subscriber()
    push_config = dict()
    created = False
    topic_name = format_pubsub_name(name=topic, pubsub_type='topic', project_id=project_id)
    subscription_name = format_pubsub_name(
        name=subscription, pubsub_type='subscription', project_id=project_id,
    )
    if app_settings.get('service_url'):
        push_config['push_endpoint'] = urljoin(app_settings['service_url'], path)
    if expiration_in_days:
        time_to_live = Duration()
        time_to_live.FromTimedelta(timedelta(days=expiration_in_days))
        expiration_policy = dict(ttl=time_to_live)
    elif app_settings['environment'] in {'local', 'test'}:
        # In the local & test environments, subscriptions are expired after 7 days
        time_to_live = Duration()
        time_to_live.FromTimedelta(timedelta(days=7))
        expiration_policy = dict(ttl=time_to_live)
    else:
        # In the qa & prod environments, subscriptions are never expired
        expiration_policy = dict()
    try:
        request = Subscription(
            name=subscription_name,
            topic=topic_name,
            push_config=push_config,
            expiration_policy=expiration_policy
        )
        subscriber.create_subscription(request=request)
    except Conflict as e:
        logger.warning(e)
    else:
        created = True
    return subscription, created


def push_to_topic(topic_name, attributes, payload: dict, use_raw_name=True):
    """ Pushes payload to a topic
    :param topic_name: topic name
    :param attributes: attributes
    :param payload: payload
    :param use_raw_name: flag to use raw name
    :return: success flag """
    import json
    publisher = create_publisher()
    name = generate_topic_name(name=topic_name, use_raw_name=use_raw_name)
    topic = format_pubsub_name(name=name)
    publisher.publish(
        topic=topic, data=json.dumps(payload).encode('utf-8'),
        **{k: v for k, v in attributes.items() if v is not None and k not in {'data', 'topic'}}
    ).result()
    return True


def generate_pubsub_push_message(subscription, attributes, message):
    """ Generates pubsub push message
    :param subscription: subscription
    :param attributes: attributes
    :param message: message
    :return: push message details """
    from stratus_api.core.common import generate_random_id
    import base64
    import json
    if not isinstance(message, bytes):
        message = json.dumps(message).encode('utf-8')
    return dict(
        subscription=subscription,
        message=dict(
            messageId=generate_random_id(),
            attributes=attributes,
            data=base64.b64encode(message).decode('utf-8')
        )
    )


def generate_topic_name(name, service_name=None, use_raw_name=False):
    """ Generates the topic name based on the service name
    :param name: topic name
    :param service_name: service name
    :param use_raw_name: flag to use raw name
    :return: formatted topic name """
    from stratus_api.core.settings import get_settings
    if service_name is None:
        service_name = get_settings()['service_name']
    if not use_raw_name:
        name = '{service_name}-{environment}-{name}'.format(service_name=service_name,
                                                            environment=get_settings()['environment'], name=name)
    return name


def generate_subscription_name(topic_name):
    """ Generates the subscription name based on the topic name
    :param topic_name: topic name
    :return: formatted subscription name """
    from stratus_api.core.settings import get_settings
    service_name = get_settings()['service_name']
    return '{service_name}-{topic_name}-subscription'.format(service_name=service_name, topic_name=topic_name)


def create_topics(topics):
    """ Creates topics for the list of topic details
    :param topics: list of topic details
    :return: list of topic names """
    topic_names = list()
    for topic in topics:
        topic_name = generate_topic_name(
            name=topic['name'], service_name=topic.get('service_name'),
            use_raw_name=topic.get('use_raw_name', False)
        )
        create_topic(name=topic_name, project_id=topic.get('project_id'))
        topic_names.append(topic_name)
    return topic_names


def create_subscriptions(topics):
    """ Create subscriptions for the list of topic details
    :param topics: list of topic details
    :return: list of subscription names """
    subscription_names = list()
    for topic in topics:
        topic_name = generate_topic_name(
            name=topic['name'], service_name=topic.get('service_name'),
            use_raw_name=topic.get('use_raw_name', False)
        )
        subscription_name = generate_subscription_name(topic_name=topic_name)
        create_subscription(topic=topic_name, subscription=subscription_name, path=topic.get('path'),
                            project_id=topic.get('project_id'))
        subscription_names.append(subscription_name)
    return subscription_names
