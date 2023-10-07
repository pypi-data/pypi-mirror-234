import array
import json
from celerabitpipelineintegration.model_credentials import Credentials
from celerabitpipelineintegration.util_compliance_evaluator import ComplianceEvaluator
from celerabitpipelineintegration.util_configuration import Configuration
from celerabitpipelineintegration.model_execution_params import ExecutionParams, parse_from_args
from celerabitpipelineintegration.uc_authenticator import Authenticator
from celerabitpipelineintegration.uc_scenario_runner import ScenarioRunner

class ModuleMain:

    __execution_params__:ExecutionParams = None

    def __is_debug_enabled__(self) -> bool:
        return  self.__execution_params__.exists_swtich('--DEBUG') or \
                self.__execution_params__.exists_swtich('-DEBUG') or \
                self.__execution_params__.exists_swtich('DEBUG')

    def __is_quiet__(self) -> bool:
        return  self.__execution_params__.exists_swtich('-q') or \
                self.__execution_params__.exists_swtich('--q')

    def __configure_logger__(self):
        if self.__execution_params__:
            if (self.__is_debug_enabled__()):
                Configuration.instance().set_config_value('LOGGER', 'level', 'DEBUG')
            if (self.__is_quiet__()):
                Configuration.instance().set_config_value('LOGGER', 'quiet', True)

    def __get_credentials__(self) -> Credentials:
        login:str = self.__execution_params__.get_arg('login')
        password:str = self.__execution_params__.get_arg('password')
        if not login:
            raise Exception('Login not received')
        if not password:
            raise Exception('Password not received')
        return Credentials(login, password)

    def __do_authenticate__(self):
        credentials:Credentials = self.__get_credentials__()
        authenticator:Authenticator = Authenticator()
        token:str = authenticator.authenticate(credentials)
        print(token)

    def __job_info_to_string__(self, job_info:dict) -> str:
        if not job_info:
            return None
        json_string:str = json.dumps(job_info)
        return json_string

    def __do_run__(self):
        token:str = self.__execution_params__.get_arg('token')
        client:str = self.__execution_params__.get_arg('client')
        application:str = self.__execution_params__.get_arg('application')
        scenario:str = self.__execution_params__.get_arg('scenario')
        run_timeout_seconds:int = self.__execution_params__.get_arg('timeout')

        if not token:
            raise Exception('Token not received')
        
        if not client:
            raise Exception('Client not received')

        if not application:
            raise Exception('Application not received')

        if not scenario:
            raise Exception('Scenario not received')

        if not run_timeout_seconds:
            run_timeout_seconds = Configuration.instance().get_config_value('INVOKER', 'default-run-timeout-seconds')

        scenario_runner:ScenarioRunner = ScenarioRunner( \
                                                client_name = client, \
                                                application_name = application, \
                                                scenario_code = scenario, \
                                                token = token,
                                                run_timeout_seconds = run_timeout_seconds
                                            )

        job_info:dict = scenario_runner.run_sync()
        print(self.__job_info_to_string__(job_info))


    def __get_job_execution_result_json__(self, job_execution_result_str:str) -> any:
        job_execution_result:any = None
        try:
            job_execution_result = json.loads(job_execution_result_str)
        except:
            raise Exception('job-result is not a json object')

        if not 'complianceLatency' in job_execution_result:
            raise Exception('complianceLatency is not in job-result')

        if not 'complianceThroughput' in job_execution_result:
            raise Exception('complianceThroughput is not in job-result')

        if not 'complianceErrors' in job_execution_result:
            raise Exception('complianceErrors is not in job-result')

        if not 'complianceDeviation' in job_execution_result:
            raise Exception('complianceDeviation is not in job-result')

        return job_execution_result

    def __get_tolerance__(self, tolerance_str:str = None) -> dict:
        tolerance:dict = {'latency': 0.0, 'throughput': 0.0, 'errors': 0.0, 'deviation': 0.0}

        if tolerance_str:
            tokens:array = tolerance_str.split(',')
            splited_token:array = None
            float_value:float = 0.0
            for token in tokens:
                splited_token = token.strip().split('=')
                if len(splited_token) != 2:
                    raise Exception('Invalid tolerance: {}'.format(token))

                try:
                    float_value = float(splited_token[1])
                except:
                    raise Exception('Invalid value for {}'.format(token))

                if 'latency' == splited_token[0].strip().lower():
                    tolerance['latency'] = float_value
                elif 'throughput' == splited_token[0].strip().lower():
                    tolerance['throughput'] = float_value
                elif 'errors' == splited_token[0].strip().lower():
                    tolerance['errors'] = float_value
                elif 'deviation' == splited_token[0].strip().lower():
                    tolerance['deviation'] = float_value
                else:
                    raise Exception('Invalid performance dimension: {}'.format(splited_token[0]))

        return tolerance

    def __do_eval_job_results__(self):
        job_execution_result_str:str = self.__execution_params__.get_arg('job-result')
        tolerance_str:str = self.__execution_params__.get_arg('tolerance')

        if not job_execution_result_str:
            raise Exception('job-result not received')
        
        job_execution_result:any = self.__get_job_execution_result_json__(job_execution_result_str)

        tolerance:dict = self.__get_tolerance__(tolerance_str)

        evaluator:ComplianceEvaluator = ComplianceEvaluator(job_execution_result, tolerance)
        errors:array = evaluator.evaluate()
        if errors and len(errors) > 0:
            error_message:str = ''
            for error in errors:
                error_message += error + "\n"
            print(error_message)

    def run(self, args:array):
        self.__execution_params__ = parse_from_args(args)
        self.__configure_logger__()

        if self.__execution_params__.operation == 'authenticate':
            self.__do_authenticate__()
        elif self.__execution_params__.operation == 'run':
            self.__do_run__()
        elif self.__execution_params__.operation == 'eval-job-results':
            self.__do_eval_job_results__()
