def get_allowed_promise_states():
    return ['active', 'completed', 'failed', 'pending']


def start_task_signature(sig, **task_parameters):
    from stratus_api.core.settings import get_settings
    celery_settings = get_settings(settings_type='celery')
    if not celery_settings.get('broker_url'):
        return sig.apply()
    else:
        return sig.apply_async(**task_parameters)


def generate_job_topic_name(job_type, service_name=None):
    from stratus_api.core.settings import get_settings
    settings = get_settings(settings_type='app')
    if service_name is None:
        service_name = settings['service_name']
    return '{service_name}-{environment}-{job_type}'.format(service_name=service_name,
                                                            environment=settings['environment'], job_type=job_type)


def generate_job_subscription_name(job_type, service_name):
    from stratus_api.core.settings import get_settings
    settings = get_settings(settings_type='app')
    return '{subscriber}-{topic_name}'.format(
        subscriber=settings['service_name'],
        topic_name=generate_job_topic_name(service_name=service_name, job_type=job_type)
    )


def extract_attributes(body: dict) -> tuple:
    """Convenience function to extract common attributes from PubSub messages

    :param body:
    :return: Tuple of external_id, external service name, and the promise results
    """
    import base64
    import json
    message = body.get('message', dict())
    attributes = message.get('attributes', dict())

    service_name = attributes.get('service_name', body.get('subscription', '').split('/')[-1].split('-')[1])
    external_id = attributes.get('job_id')
    status = attributes.get('status', 'failed')
    results = json.loads(base64.b64decode(message['data']).decode('utf-8'))

    return external_id, service_name, results, status


def process_promise_update_request(body):
    from stratus_api.jobs.promises import update_promise
    external_id, service_name, results, status = extract_attributes(body=body)

    update_promise(status=status, service_name=service_name, external_id=external_id, results=results)
    return dict(active=True)
