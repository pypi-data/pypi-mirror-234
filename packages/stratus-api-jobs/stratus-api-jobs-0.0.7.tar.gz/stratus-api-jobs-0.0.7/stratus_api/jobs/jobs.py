def create_job(job_id: str, job_type: str, parameters: dict, task=None, task_kwargs: dict = None, promises: list = None,
               status: str = 'pending', results: dict = None, trace_id: str = None) -> dict:
    """ Create and store an an internal job. Create jobs when integrating with long running tasks or external services.

    :param job_id: the uuid4 job id
    :param job_type: The type of job
    :param parameters: The parameters used to call create the job (might need to be encrypted)
    :param task_kwargs: the keyword argument that are required to run the next task (other than job_id)
    :param task: the celery task be run after promises are completed. Provide the function without calling it
    :param promises: list of promises that need to complete before continuing with the job.
    :param trace_id: optional string that will be passed along with the published results
    :param status:
    :param results:
    :return: dictionary of the job contents
    """
    from .base import get_allowed_promise_states
    from stratus_api.document import create_object
    assert status in get_allowed_promise_states()

    promise_ids = []
    if isinstance(promises, list):
        promise_ids = [i['id'] for i in promises]
    if not results:
        results = dict()
    job_data = dict(
        id=job_id,
        job_type=job_type,
        parameters=parameters,
        status=status,
        promise_ids=promise_ids,
        results=results,
        trace_id=trace_id,
        task=task.name if task is not None else None,
        task_kwargs=task_kwargs if task_kwargs is not None else dict(),
    )
    job = create_object(collection_name='jobs', unique_keys=['id'], attributes=job_data)
    publish_job_status(job_id=job_id, status=job_data['status'], job_type=job_type, results=job_data['results'],
                       trace_id=job_data['trace_id'])
    return job


def get_job(job_id: str, get_promises: bool = False) -> dict:
    """Get the job values currently stored in Firebase

    :param job_id: internal job id
    :param get_promises: Optional flag to include the promise values in the response
    :return: dictionary of the current job
    """
    from stratus_api.document import get_objects
    jobs = get_objects(collection_name='jobs', eq_id=job_id)
    if jobs:
        job = jobs[0]
        if get_promises:
            promises = get_objects(collection_name='promises', contains_job_ids=job['id'], limit=None)
            job['promises'] = promises
        return job
    else:
        return dict()


def update_job(job_id: str, status: str, next_task=None, task_kwargs: dict = None, results=None,
               promises: list = None):
    """Update a job when completed/failed or when there are additional promises that need to complete.

    :param job_id: the job id
    :param status: plain english description of the current job state (active, pending, completed, failed)
    :param next_task: the celery task be run after promises are completed. Provide the function without calling it
    :param task_kwargs: the keyword argument that are required to run the next task (other than job_id)
    :param results: the results of the job
    :param promises: a list of new promises
    :return: a dictionary of the job's contents
    """
    from .base import get_allowed_promise_states
    from stratus_api.document import get_objects, update_object
    assert status in get_allowed_promise_states()
    jobs = get_objects(collection_name='jobs', eq_id=job_id)
    if not jobs:
        raise ValueError("Job does not Exist")
    job = jobs[0]
    job.update(
        dict(
            status=status,
            results=results if results is not None else dict(),
            task=next_task.name if next_task is not None else None,
            task_kwargs=task_kwargs if task_kwargs is not None else dict(),
            promise_ids=job['promise_ids'] if promises is None else list(
                set(job['promise_ids'] + [i['id'] for i in promises]))
        ))
    update_object(collection_name='jobs', object_id=job_id, attributes=job)
    publish_job_status(job_id=job_id, status=status, job_type=job['job_type'], results=results,
                       trace_id=job['trace_id'])
    return job


def publish_job_status(job_id: str, status: str, job_type: str, results: dict = None, trace_id: str = None):
    """Publishes a message to the message bus based with the current job's status

    :param job_id: the internal id for the job
    :param status: the current job status
    :param job_type: the API path used to create the job
    :param results: the current results (if it results in an error
    :param trace_id: externally provided trace_id used by clients that need traceable id for job messages
    :return: Nothing
    """
    from stratus_api.core.settings import get_settings
    from stratus_api.core.logs import get_logger
    from stratus_api.events import publish_event
    from stratus_api.jobs.base import generate_job_topic_name
    if not results:
        results = None
    get_logger().info(dict(job_id=job_id, job_type=job_type, status=status, results=results))
    if trace_id is None:
        trace_id = job_id
    attributes = dict(
        job_id=job_id,
        job_type=job_type,
        service_name=get_settings(settings_type='app')['service_name'],
        status=status,
        trace_id=trace_id
    )
    publish_event(topic_name=generate_job_topic_name(job_type=job_type), attributes=attributes, event_type='jobs',
                  payload=results, status=status)

    return True


def resume_job(job_id, promise_status, promise_id, last_job_update, last_promise_update):
    from celery import signature
    from .tasks.jobs import job_error_handler_task
    from .base import start_task_signature
    from stratus_api.document import get_objects
    job = get_job(job_id=job_id, get_promises=True)
    finished_promises = [i for i in job['promises'] if i['status'] in ('completed', 'resolved')]
    promise = get_objects(collection_name='promises', eq_id=promise_id)[0]
    task_signature = None
    if last_promise_update == promise.get('updated').timestamp() and last_job_update == job.get('updated').timestamp():
        if job['status'] not in ('completed', 'failed'):
            if promise_status == 'failed':
                if promise.get('failure_task') is not None:
                    task_signature = signature(promise.get('failure_task'),
                                               kwargs=dict(promise_id=promise_id, job_id=job_id,
                                                           **promise.get('failure_task_kwargs')))
                else:
                    update_job(
                        job_id=job_id, status='failed',
                        results=dict(error="Promise: {0} failed".format(promise_id)))
            else:
                if len(finished_promises) == len(job['promises']):
                    update_job(job_id=job_id, status='active')
                    task_signature = signature(job.get('task'),
                                               kwargs=dict(job_id=job_id, **job.get('task_kwargs'))).on_error(
                        job_error_handler_task.s(job_id=job_id))
    if task_signature is not None:
        start_task_signature(sig=task_signature)
    return job, promise
