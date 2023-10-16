def generate_bq_log_input(job_type, promise_id, subscription, results: dict = None, errors: dict = None):
    from stratus_api.core.settings import get_settings
    from stratus_api.events.pubsub import generate_pubsub_push_message
    app_settings = get_settings()
    if not errors:
        errors = dict()
    data = {
        "protoPayload": {
            "methodName": "jobservice.jobcompleted",
            "resourceName": "projects/{0}/jobs/{1}".format(app_settings['project_id'], promise_id),
            "serviceData": {
                "@type": "type.googleapis.com/google.cloud.bigquery.logging.v1.AuditData",
                "jobCompletedEvent": {
                    "eventName": "{0}_job_completed".format(job_type),
                    "job": {
                        "jobName": {
                            "projectId": app_settings['project_id'],
                            "jobId": promise_id,
                            "location": "US"
                        },
                        "jobStatus": {
                            "state": "DONE",
                            "error": errors
                        },
                        'jobStatistics': results
                    }
                }
            }
        }
    }
    return generate_pubsub_push_message(subscription=subscription, attributes=dict(), message=data)
