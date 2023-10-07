
import array


class ComplianceEvaluator:

    job_execution_result:any
    tolerance:dict

    def __init__(self, job_execution_result:any, tolerance:dict) -> None:
        self.job_execution_result = job_execution_result
        self.tolerance = tolerance

    def __validate_job__(self) -> list:
        result_list:list = []

        if not "status" in self.job_execution_result:
            result_list.append('job without status')
        elif self.job_execution_result["status"] != "SUCCESS":
            result_list.append('job status is not SUCCESS')

        return result_list            

    def evaluate(self) -> array:
        current_value:float = 0.0
        minimum:float = 0.0
        error_messagges:array = []

        validation_list:list = self.__validate_job__()

        if len(validation_list) == 0:
            current_value = float(self.job_execution_result['complianceLatency'])
            minimum = self.tolerance['latency'] * 100
            if (current_value < minimum):
                error_messagges.append('Latency {} below tolerance {}'.format(current_value, minimum))

            current_value = float(self.job_execution_result['complianceThroughput'])
            minimum = self.tolerance['throughput'] * 100
            if (current_value < minimum):
                error_messagges.append('Throughput {} below tolerance {}'.format(current_value, minimum))

            current_value = float(self.job_execution_result['complianceErrors'])
            minimum = self.tolerance['errors'] * 100
            if (current_value < minimum):
                error_messagges.append('Errors {} below tolerance {}'.format(current_value, minimum))

            current_value = float(self.job_execution_result['complianceDeviation'])
            minimum = self.tolerance['deviation'] * 100
            if (current_value < minimum):
                error_messagges.append('Deviation {} below tolerance {}'.format(current_value, minimum))
        else:
            error_messagges = validation_list

        return error_messagges if len(error_messagges) > 0 else None
