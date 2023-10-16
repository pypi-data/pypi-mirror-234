import copy
import logging
import time
import traceback
from functools import wraps

from catchpoint import constants
from catchpoint.application.global_application_info_provider import GlobalApplicationInfoProvider
from catchpoint.compat import TimeoutError
from catchpoint.config import config_names
from catchpoint.config.config_provider import ConfigProvider
from catchpoint.context.execution_context_manager import ExecutionContextManager
from catchpoint.context.global_execution_context_provider import GlobalExecutionContextProvider
from catchpoint.context.plugin_context import PluginContext
from catchpoint.integrations import handler_wrappers
from catchpoint.timeout import Timeout
from catchpoint.wrappers import wrapper_utils
from catchpoint.wrappers.aws_lambda import LambdaApplicationInfoProvider
from catchpoint.wrappers.aws_lambda import lambda_executor
from catchpoint.wrappers.base_wrapper import BaseWrapper

logger = logging.getLogger(__name__)


class LambdaWrapper(BaseWrapper):

    def __init__(self, api_key=None, disable_trace=False, disable_metric=True, disable_log=True, opts=None):
        super(LambdaWrapper, self).__init__(api_key, disable_trace, disable_metric, disable_log, opts)
        self.application_info_provider = GlobalApplicationInfoProvider(LambdaApplicationInfoProvider())
        self.plugin_context = PluginContext(application_info=self.application_info_provider.get_application_info(),
                                            request_count=0,
                                            executor=lambda_executor,
                                            api_key=self.api_key)

        ExecutionContextManager.set_provider(GlobalExecutionContextProvider())
        self.plugins = wrapper_utils.initialize_plugins(self.plugin_context, disable_trace, disable_metric, disable_log,
                                                        self.config)

        self.timeout_margin = ConfigProvider.get(config_names.CATCHPOINT_LAMBDA_TIMEOUT_MARGIN,
                                                 constants.DEFAULT_LAMBDA_TIMEOUT_MARGIN)

        if not ConfigProvider.get(config_names.CATCHPOINT_TRACE_INSTRUMENT_DISABLE):
            # Pass catchpoint instance to integration for wrapping handler wrappers
            handler_wrappers.patch_modules(self)


    def __call__(self, original_func):
        if hasattr(original_func, "_catchpoint_wrapped") or ConfigProvider.get(config_names.CATCHPOINT_DISABLE, False):
            return original_func

        @wraps(original_func)
        def wrapper(event, context):
            application_name = self.plugin_context.application_info.get('applicationName')
            self.application_info_provider.update({
                'applicationId': LambdaApplicationInfoProvider.get_application_id(context,
                                                                                  application_name=application_name)
            })

            # Execution context initialization
            execution_context = wrapper_utils.create_execution_context()
            try:
                execution_context.platform_data['originalEvent'] = copy.deepcopy(event)
            except:
                execution_context.platform_data['originalEvent'] = event
            execution_context.platform_data['originalContext'] = context
            ExecutionContextManager.set(execution_context)

            # Before running user's handler
            try:
                if ConfigProvider.get(config_names.CATCHPOINT_LAMBDA_WARMUP_WARMUPAWARE,
                                      False) and self.check_and_handle_warmup_request(event):
                    return None

                self.plugin_context.request_count += 1
                self.execute_hook('before:invocation', execution_context)

                timeout_duration = self.get_timeout_duration(context)
            except Exception as e:
                logger.error("Error during the before part of Catchpoint: {}".format(e))
                return original_func(event, context)

            # Invoke user handler
            try:
                response = None
                with Timeout(timeout_duration, self.timeout_handler, execution_context):
                    response = original_func(event, context)
                    execution_context.response = response
            except Exception as e:
                try:
                    execution_context.error = {
                        'type': type(e).__name__,
                        'message': str(e),
                        'traceback': traceback.format_exc()
                    }
                    self.prepare_and_send_reports(execution_context)
                except Exception as e_in:
                    logger.error("Error during the after part of Catchpoint: {}".format(e_in))
                    pass
                raise e
            finally:
                pass

            # After having run the user's handler
            try:
                self.prepare_and_send_reports(execution_context)
            except Exception as e:
                logger.error("Error during the after part of Catchpoint: {}".format(e))

            ExecutionContextManager.clear()
            return response

        setattr(wrapper, '_catchpoint_wrapped', True)
        return wrapper

    call = __call__


    def check_and_handle_warmup_request(self, event):

        # Check whether it is empty request which is used as default warmup request
        if not event:
            print("Received warmup request as empty message. " +
                  "Handling with 90 milliseconds delay ...")
            time.sleep(0.1)
            return True
        else:
            if isinstance(event, str):
                # Check whether it is warmup request
                if event.startswith('#warmup'):
                    delayTime = 90
                    args = event[len('#warmup'):].strip().split()
                    # Warmup messages are in '#warmup wait=<waitTime>' format
                    # Iterate over all warmup arguments
                    for arg in args:
                        argParts = arg.split('=')
                        # Check whether argument is in key=value format
                        if len(argParts) == 2:
                            argName = argParts[0]
                            argValue = argParts[1]
                            # Check whether argument is "wait" argument
                            # which specifies extra wait time before returning from request
                            if argName == 'wait':
                                waitTime = int(argValue)
                                delayTime += waitTime
                    print("Received warmup request as warmup message. " +
                          "Handling with " + str(delayTime) + " milliseconds delay ...")
                    time.sleep(delayTime / 1000)
                    return True
            return False

    def get_timeout_duration(self, context):
        timeout_duration = 0
        if hasattr(context, 'get_remaining_time_in_millis'):
            timeout_duration = context.get_remaining_time_in_millis() - self.timeout_margin
            if timeout_duration <= 0:
                timeout_duration = context.get_remaining_time_in_millis() - \
                                   constants.DEFAULT_LAMBDA_TIMEOUT_MARGIN
                logger.warning('Given timeout margin is bigger than lambda timeout duration and '
                               'since the difference is negative, it is set to default value (' +
                               str(constants.DEFAULT_LAMBDA_TIMEOUT_MARGIN) + ')')

        return timeout_duration / 1000.0

    def timeout_handler(self, execution_context):
        execution_context.timeout = True
        execution_context.error = TimeoutError('Task timed out')
        self.prepare_and_send_reports(execution_context)
