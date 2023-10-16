__client__ = dict()


def create_bq_client(credentials=None, project=None):
    """Convenience function to create a BQ client or pull the client from cache

    :return: an authenticated storage client
    """
    from google.cloud import bigquery
    global __client__
    project_key = 'default' if project is None else project
    if not __client__.get(project_key):
        __client__[project_key] = bigquery.Client(credentials=credentials, project=project)
    return __client__[project_key]


def delete_table(table_name, project_id=None, dataset_name=None, not_found_ok: bool = False):
    bq_client = create_bq_client()
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    table = dataset_ref.table(table_id=table_name)
    bq_client.delete_table(table=table, not_found_ok=not_found_ok)
    return True


def get_job(bq_job_id, project_id=None):
    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    if project_id is None:
        project_id = app_settings['project_id']
    bq_client = create_bq_client(project=project_id)
    job = bq_client.get_job(job_id=bq_job_id, project=project_id)
    return job


def generate_dataset_ref(dataset_name=None, project_id=None):
    from google.cloud.bigquery import DatasetReference

    from stratus_api.core.settings import get_settings
    app_settings = get_settings(settings_type='app')
    if dataset_name is None:
        dataset_name = app_settings['dataset_name']
    if project_id is None:
        project_id = app_settings['project_id']
    return DatasetReference(project=project_id, dataset_id=dataset_name)


def create_table(table_name, schema, dataset_name=None, project_id=None, expiration=7,
                 partition_field=None, clustering_fields=None, partition_type=None, partition_expiration_ms=None):
    from google.cloud import bigquery
    from datetime import datetime, timedelta
    bq_client = create_bq_client()
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)

    table_ref = bigquery.TableReference(dataset_ref=dataset_ref,
                                        table_id=table_name)
    table = bigquery.Table(
        table_ref=table_ref,
        schema=[bigquery.SchemaField(i['name'], i['type'], i.get('mode', 'NULLABLE')) for i in schema]
    )
    if expiration is not None:
        dt = datetime.utcnow() + timedelta(days=expiration)
        table.expires = dt
    if partition_type or partition_field:
        if partition_type is None:
            partition_type = 'DAY'
        table.time_partitioning = bigquery.TimePartitioning(field=partition_field, type_=partition_type,
                                                            expiration_ms=partition_expiration_ms)
    if clustering_fields:
        table.clustering_fields = clustering_fields
    bq_client.create_table(table=table, exists_ok=True)
    return table_name


def load_csv_to_bq_table(bucket: str, table_name: str, external_job_id: str, schema: list, file_patterns: list,
                         project_id=None, dataset_name=None, headers=True, max_bad_records=None, jagged_edges=True,
                         expiration=7, client_project=None, delimiter=','):
    """Create a BQ load job to load data from a bucket into a specific table
    :param bucket: External bucket name where the data files exist
    :param file_patterns: list of file path pattern including * wildcard
    :param table_name: table name to load data into
    :param external_job_id: externally generated job id
    :param schema: data file schema
    :param headers: boolean that headers exist
    :param dataset_name: GCP dataset name to load data into
    :param project_id: GCP project id
    :param expiration: table Expiration in days
    :return: external id after bq job has been created
    """
    from google.cloud import bigquery
    from google.cloud.exceptions import NotFound
    assert file_patterns
    try:
        get_table(table_name, project_id=project_id, dataset_name=dataset_name)
    except NotFound:
        create_table(table_name=table_name, schema=schema, project_id=project_id, dataset_name=dataset_name,
                     expiration=expiration)
    bq_client = create_bq_client(project=client_project)
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.field_delimiter = delimiter
    job_config.schema = [
        bigquery.SchemaField(i['name'], i['type']) for i in schema
    ]

    job_config.allow_jagged_rows = jagged_edges
    if headers:
        job_config.skip_leading_rows = 1
    else:
        job_config.skip_leading_rows = 0
    if max_bad_records:
        job_config.max_bad_records = max_bad_records
    job_config.source_format = bigquery.SourceFormat.CSV
    bq_client.load_table_from_uri(
        source_uris=['gs://' + bucket + '/' + i for i in file_patterns],
        destination=dataset_ref.table(table_name),
        job_config=job_config,
        job_id=external_job_id,
        project=project_id
    )
    return external_job_id


def export_bq_table_to_csv(external_job_id: str, file_pattern: str, table_name: str, project_id=None, dataset_name=None,
                           compressed=True, delimiter=',', bucket_name=None, include_headers=True, client_project=None):
    """Export a table from the service data set to the local service bucket based on a desired file pattern.
    Must include * wildcard

    :param external_job_id: External job id
    :param file_pattern: exported file path pattern including * wildcard
    :param table_name: table name to export
    :param compressed: Boolean to compress the data. True will compress using gz and file pattern must include .gz
    :param dataset_name: GCP dataset name to load data into
    :param project_id: GCP project id
    :param bucket_name: GCS Bucket name to export data to
    :param delimiter: internal file delimiter. Defaults to comma
    :return: external bq job id
    """
    from google.cloud import bigquery
    from stratus_api.core.settings import get_settings
    bq_client = create_bq_client(project=client_project)
    assert not compressed or file_pattern.endswith('.gz')
    assert '*' in file_pattern
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    job_config = bigquery.ExtractJobConfig()
    if bucket_name is None:
        bucket_name = get_settings(settings_type='app')['bucket_name']
    if compressed:
        job_config.compression = bigquery.job.Compression.GZIP
    job_config.field_delimiter = delimiter
    job_config.destination_format = bigquery.DestinationFormat.CSV
    job_config.print_header = include_headers

    bq_client.extract_table(
        source=dataset_ref.table(table_name),
        destination_uris='gs://' + bucket_name + '/' + file_pattern,
        job_config=job_config,
        job_id=external_job_id
    )
    return external_job_id


def execute_async_query(external_job_id: str, table_name: str, query: str, expiration=None, parameters: list = None,
                        write_behavior: str = 'TRUNCATE', schema: list = None, dataset_name=None, project_id=None,
                        client_project=None, labels: dict = None):
    """Execute a BQ query and create a new table

    :param external_job_id: externally generated bq job id. Must be unique.
    :param table_name: table name for the new table
    :param query: query to execute
    :param parameters: list of query parameters
    :param write_behavior: BQ write behavior replace = TRUNCATE, append = APPEND
    :return:
    """
    from google.cloud import bigquery
    from google.cloud.exceptions import NotFound
    from google.cloud.bigquery.job import QueryPriority
    from stratus_api.core.settings import get_settings
    app_settings = get_settings()
    write_behavior = write_behavior.upper()
    assert write_behavior in ('TRUNCATE', 'APPEND')
    bq_client = create_bq_client(project=client_project)
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    job_config = bigquery.QueryJobConfig()
    if parameters:
        job_config.query_parameters = parameters
    query_labels = {
        'service_name': app_settings['service_name'],
    }
    if labels:
        labels.update(query_labels)
    else:
        labels = query_labels
    job_config.labels = labels
    job_config.default_dataset = dataset_ref
    job_config.destination = dataset_ref.table(table_name)
    job_config.write_disposition = "WRITE_{0}".format(write_behavior)
    job_config.priority = QueryPriority.BATCH
    if app_settings['environment'] == 'test':
        job_config.priority = QueryPriority.INTERACTIVE

    if (write_behavior == 'TRUNCATE' or schema) and expiration is not None:
        if not schema:
            schema = [dict(name='id', type='STRING')]
        try:
            get_table(table_name)
        except NotFound:
            create_table(table_name=table_name, schema=schema, dataset_name=dataset_name, project_id=project_id,
                         expiration=expiration)

    bq_client.query(
        query=query,
        job_config=job_config,
        job_id=external_job_id
    )
    return external_job_id


def execute_query(query: str, parameters: list = None, dry_run=False, client_project=None, labels: dict = None):
    """Execute a BQ query and create a new table

    :param table_name: table name for the new table
    :param query: query to execute
    :param parameters: list of query parameters
    :param write_behavior: BQ write behavior replace = TRUNCATE, append = APPEND
    :return:
    """
    from google.cloud import bigquery
    from google.cloud.bigquery.job import QueryPriority
    from stratus_api.core.settings import get_settings
    app_settings = get_settings()
    bq_client = create_bq_client(project=client_project)
    job_config = bigquery.QueryJobConfig()
    if parameters:
        job_config.query_parameters = parameters
    query_labels = {
        'service_name': app_settings['service_name'],
    }
    if labels:
        labels.update(query_labels)
    else:
        labels = query_labels
    job_config.labels = labels
    job_config.priority = QueryPriority.INTERACTIVE
    job_config.dry_run = dry_run
    query_job = bq_client.query(
        query=query,
        job_config=job_config,
    )
    if dry_run:
        return True
    else:
        return query_job.result()


def create_bq_dataset(dataset_name=None, project_id=None, expiration=False, expiration_hours: int = None):
    """Convenience function to create a dataset based on the service name.

    :param dataset_name:
    :param project_id:
    :param expiration:
    :param expiration_hours:
    :return:
    """
    from google.cloud import bigquery
    from google.cloud.exceptions import Conflict
    from stratus_api.core.settings import get_settings
    from stratus_api.core.logs import get_logger
    bq_client = create_bq_client()
    app_settings = get_settings(settings_type='app')
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    dataset = bigquery.Dataset(dataset_ref)
    if expiration:
        if expiration_hours is None:
            expiration_hours = app_settings.get('table_expiration_hours', 7 * 24)
        dataset.default_table_expiration_ms = int(expiration_hours) * 60 * 60 * 1000
    try:
        bq_client.create_dataset(dataset=dataset)
    except Conflict as exc:
        get_logger().info(exc)
    return dataset_ref


def get_dataset(dataset_name, project_id=None):
    """

    :param dataset_name:
    :param project_id:
    :return:
    """
    bq_client = create_bq_client()
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    dataset = bq_client.get_dataset(dataset_ref=dataset_ref)
    return dataset


def get_table(table_name, dataset_name=None, project_id=None):
    """

    :param table_name:
    :param dataset_name:
    :param project_id:
    :return:
    """
    bq_client = create_bq_client()
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    table_ref = dataset_ref.table(table_name)
    table = bq_client.get_table(table=table_ref)
    return table


def delete_dataset(dataset_name, project_id=None):
    bq_client = create_bq_client()
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    bq_client.delete_dataset(dataset=dataset_ref, delete_contents=True)
    return True


def stream_records_to_bigquery(rows, table_name, project_id=None, dataset_name=None, row_ids: list = None):
    from stratus_api.core.common import generate_hash_id
    bq_client = create_bq_client()
    table = get_table(table_name=table_name, project_id=project_id, dataset_name=dataset_name)
    if row_ids is None:
        row_ids = [generate_hash_id(row) for row in rows]
    return bq_client.insert_rows(rows=rows, table=table, row_ids=row_ids)


def get_table_names_by_pattern(pattern, dataset_name=None, project_id=None):
    for table in get_tables_by_pattern(pattern=pattern, dataset_name=dataset_name, project_id=project_id):
        yield table.table_id


def get_tables_by_pattern(pattern, dataset_name=None, project_id=None):
    import re
    bq_client = create_bq_client()
    matcher = re.compile(pattern=pattern)
    dataset_ref = generate_dataset_ref(dataset_name=dataset_name, project_id=project_id)
    for table in bq_client.list_tables(dataset=dataset_ref):
        if matcher.match(table.table_id):
            yield table


def get_dataset_names_by_pattern(pattern, project_id=None):
    for dataset in get_datasets_by_pattern(pattern=pattern, project_id=project_id):
        yield dataset.dataset_id


def get_datasets_by_pattern(pattern, project_id=None):
    import re
    from stratus_api.core.settings import get_settings
    bq_client = create_bq_client()
    if project_id is None:
        project_id = get_settings()['project_id']
    matcher = re.compile(pattern=pattern)
    for dataset in bq_client.list_datasets(project=project_id):
        if matcher.match(dataset.dataset_id):
            yield dataset
