from celery import shared_task


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def resume_job_task(self, job_id, promise_status, promise_id, last_job_update, last_promise_update):
    """Resumes the job if all promises have completed

    :return:
    """
    from stratus_api.jobs.jobs import resume_job
    job, promise = resume_job(job_id=job_id, promise_status=promise_status, promise_id=promise_id,
                              last_job_update=last_job_update, last_promise_update=last_promise_update)
    return job, promise


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def close_job_task(self, job_id, status, results):
    from stratus_api.jobs.jobs import update_job
    return update_job(job_id=job_id, status=status, results=results)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def job_error_handler_task(self, exc, task_id, *args, **kwargs):
    from stratus_api.jobs.jobs import update_job
    return update_job(job_id=args[1]['job_id'], status='failed',
                      results=dict(error=exc.args[0], traceback=str(args[-1])))
