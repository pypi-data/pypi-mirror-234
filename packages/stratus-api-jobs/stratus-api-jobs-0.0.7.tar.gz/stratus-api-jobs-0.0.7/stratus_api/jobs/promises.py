from datetime import datetime
from google.cloud import firestore

CHANGES = dict(
    active={'completed', 'failed', 'resolved'},
    completed=set(),
    failed={'resolved', 'completed'},
    pending={'active', 'completed', 'failed', 'resolved'},
    resolved=set(),
)


def get_allowed_promise_state_changes(status):
    global CHANGES
    return CHANGES[status]


def generate_promise_id(service_name: str, external_id: str) -> str:
    """Takes a service name and external id and returns the internal promise id

    :param service_name: Name of the service
    :param external_id: External promise id
    :return: internal promise id
    """
    return "{0}-{1}".format(service_name, external_id)


def parse_promise_id(promise_id: str) -> tuple:
    """Convenience function to parse a promise id back to its external Id and service name

    :param promise_id: internal promise_id
    :return: service name, external id
    """
    service_name = promise_id.split('-')[0]
    external_id = '-'.join(promise_id.split('-')[1:])
    return service_name, external_id


def create_promise(service_name: str, promise_type: str, external_id: str, status: str = "pending",
                   parameters: dict = None, failure_task=None, failure_task_kwargs: dict = None, job_id=None,
                   job_ids=None) -> dict:
    """Store an externally created promise. Promises will automatically be updated once they complete.

    :param job_id: the internal job id that created this promise.
    :param service_name: The service name (will be included in the promise response)
    :param promise_type: API path used to generate the promise
    :param external_id: external promise id
    :param parameters: the parameters used to generate the promise
    :param status: plain english description of the current job state (active, pending, completed, failed)
    :param failure_task: celery task that will be executed if the promise fails
    :param failure_task_kwargs: additional parameters to inject into the failure task
    :return: dictionary of the promise values

    """
    from .base import get_allowed_promise_states
    from stratus_api.document import create_object
    assert status in get_allowed_promise_states()
    promise_id = generate_promise_id(service_name=service_name, external_id=external_id)
    job_ids = [job_id] if job_ids is None else job_ids
    promise_data = dict(
        id=promise_id,
        service=service_name,
        promise_type=promise_type,
        parameters=dict() if parameters is None else parameters,
        failure_task=failure_task.name if failure_task is not None else None,
        failure_task_kwargs=dict() if failure_task_kwargs is None else failure_task_kwargs,
        external_id=external_id,
        status=status,
        job_ids=job_ids
    )
    promise = create_object(collection_name='promises', attributes=promise_data, unique_keys=['id'])
    return promise


@firestore.transactional
def update_promise_transaction(transaction, promise_id, results=None, status=None, job_ids=None):
    from stratus_api.document import create_db_client
    from stratus_api.document.utilities import generate_collection_firestore_name

    db = create_db_client()
    promise_ref = db.collection(generate_collection_firestore_name(collection_name='promises')).document(promise_id)
    promise = promise_ref.get(transaction=transaction).to_dict()
    jobs = None
    updated = False
    if promise:

        if job_ids and isinstance(job_ids, list):
            promise['job_ids'].extend(job_ids)
        if status in get_allowed_promise_state_changes(status=promise['status']):
            job_ref = db.collection(generate_collection_firestore_name('jobs')).where('promise_ids', 'array_contains',
                                                                                      promise_id)
            jobs = [i.to_dict() for i in job_ref.stream(transaction=transaction)]
            updated = True
            promise.update(dict(results=results, status=status, updated=datetime.utcnow()))
        transaction.update(promise_ref, promise)
    return updated, promise, jobs


def update_promise(external_id: str, service_name: str, results: dict, status: str) -> tuple:
    """Update a promise and kick off the associated job

    :param external_id: external promise id from the service
    :param service_name: external service name
    :param results: json results returned in the promise (None is okay)
    :param status: plain english description of the current job state (active, pending, completed, failed)
    :return: dictionary of the promises attributes.
    """
    from stratus_api.document import create_db_client, get_objects
    from .tasks.jobs import resume_job_task
    from .base import start_task_signature, get_allowed_promise_states
    db = create_db_client()
    assert status in [*get_allowed_promise_states(), 'resolved']
    transaction = db.transaction()
    promise_id = generate_promise_id(service_name=service_name, external_id=external_id)
    updated, promise, jobs = update_promise_transaction(transaction=transaction, status=status, results=results,
                                                        promise_id=promise_id)
    if updated:
        promise = get_objects(collection_name='promises', eq_id=promise_id)[0]
        for job in jobs:
            sig = resume_job_task.s(job_id=job['id'], promise_status=status, promise_id=promise_id,
                                    last_job_update=job['updated'].timestamp(),
                                    last_promise_update=promise['updated'].timestamp())
            start_task_signature(sig=sig)
    return updated, promise


def add_jobs_to_promise(service_name, external_id, job_ids):
    from stratus_api.document import create_db_client
    db = create_db_client()
    transaction = db.transaction()
    promise_id = generate_promise_id(service_name=service_name, external_id=external_id)
    updated, promise, jobs = update_promise_transaction(transaction=transaction, promise_id=promise_id, job_ids=job_ids)
    return promise
