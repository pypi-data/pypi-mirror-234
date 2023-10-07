from catchpoint.config import config_names

CONFIG_METADATA = {
    config_names.CATCHPOINT_APIKEY: {
        'type': 'string',
    },
    config_names.CATCHPOINT_DEBUG_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_METRIC_DISABLE: {
        'type': 'boolean',
        'defaultValue': True,
    },
    config_names.CATCHPOINT_LOG_DISABLE: {
        'type': 'boolean',
        'defaultValue': True,
    },
    config_names.CATCHPOINT_APPLICATION_ID: {
        'type': 'string',
    },
    config_names.CATCHPOINT_APPLICATION_INSTANCE_ID: {
        'type': 'string',
    },
    config_names.CATCHPOINT_APPLICATION_NAME: {
        'type': 'string',
    },
    config_names.CATCHPOINT_APPLICATION_STAGE: {
        'type': 'string',
    },
    config_names.CATCHPOINT_APPLICATION_DOMAIN_NAME: {
        'type': 'string',
        'defaultValue': 'API',
    },
    config_names.CATCHPOINT_APPLICATION_CLASS_NAME: {
        'type': 'string',
        'defaultValue': 'AWS-Lambda',
    },
    config_names.CATCHPOINT_APPLICATION_VERSION: {
        'type': 'string',
    },
    config_names.CATCHPOINT_APPLICATION_TAG_PREFIX: {
        'type': 'any',
    },
    config_names.CATCHPOINT_REPORT_REST_BASEURL: {
        'type': 'string',
        'defaultValue': 'https://collector.tracing.catchpoint.com/v1',
    },
    config_names.CATCHPOINT_REPORT_CLOUDWATCH_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_REPORT_REST_LOCAL: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_REPORT_REST_COMPOSITE_BATCH_SIZE: {
        'type': 'int',
        'defaultValue': 100,
    },
    config_names.CATCHPOINT_REPORT_CLOUDWATCH_COMPOSITE_BATCH_SIZE: {
        'type': 'int',
        'defaultValue': 10,
    },
    config_names.CATCHPOINT_REPORT_REST_COMPOSITE_ENABLE: {
        'type': 'boolean',
        'defaultValue': True,
    },
    config_names.CATCHPOINT_REPORT_CLOUDWATCH_COMPOSITE_ENABLE: {
        'type': 'boolean',
        'defaultValue': True,
    },
    config_names.CATCHPOINT_LAMBDA_HANDLER: {
        'type': 'string',
    },
    config_names.CATCHPOINT_LAMBDA_WARMUP_WARMUPAWARE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LAMBDA_TIMEOUT_MARGIN: {
        'type': 'int',
    },
    config_names.CATCHPOINT_LAMBDA_ERROR_STACKTRACE_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_REQUEST_SKIP: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_RESPONSE_SKIP: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LAMBDA_TRACE_KINESIS_REQUEST_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LAMBDA_TRACE_FIREHOSE_REQUEST_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LAMBDA_TRACE_CLOUDWATCHLOG_REQUEST_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LAMBDA_AWS_STEPFUNCTIONS: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LAMBDA_AWS_APPSYNC: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INSTRUMENT_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INSTRUMENT_TRACEABLECONFIG: {
        'type': 'string',
    },
    config_names.CATCHPOINT_TRACE_SPAN_LISTENERCONFIG: {
        'type': 'string',
    },
    config_names.CATCHPOINT_SAMPLER_TIMEAWARE_TIMEFREQ: {
        'type': 'int',
        'defaultValue': 300000,
    },
    config_names.CATCHPOINT_SAMPLER_COUNTAWARE_COUNTFREQ: {
        'type': 'int',
        'defaultValue': 100
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_SNS_MESSAGE_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_SNS_TRACEINJECTION_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_SQS_MESSAGE_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_SQS_TRACEINJECTION_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_LAMBDA_PAYLOAD_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_LAMBDA_TRACEINJECTION_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_DYNAMODB_STATEMENT_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_DYNAMODB_TRACEINJECTION_ENABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_ATHENA_STATEMENT_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_HTTP_BODY_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_HTTP_URL_DEPTH: {
        'type': 'int',
        'defaultValue': 1,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_HTTP_TRACEINJECTION_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_HTTP_ERROR_STATUS_CODE_MIN: {
        'type': 'int',
        'defaultValue': 400,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_REDIS_COMMAND_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_RDB_STATEMENT_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_ELASTICSEARCH_BODY_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_ELASTICSEARCH_PATH_DEPTH: {
        'type': 'int',
        'defaultValue': 1,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_MONGODB_COMMAND_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_EVENTBRIDGE_DETAIL_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_SES_MAIL_MASK: {
        'type': 'boolean',
        'defaultValue': True,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_AWS_SES_MAIL_DESTINATION_MASK: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_CHALICE_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_DJANGO_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_DJANGO_ORM_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_FLASK_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_FASTAPI_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LOG_CONSOLE_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    },
    config_names.CATCHPOINT_LOG_LOGLEVEL: {
        'type': 'string',
        'defaultValue': 'TRACE',
    },
    config_names.CATCHPOINT_TRACE_INTEGRATIONS_TORNADO_DISABLE: {
        'type': 'boolean',
        'defaultValue': False,
    }
}
