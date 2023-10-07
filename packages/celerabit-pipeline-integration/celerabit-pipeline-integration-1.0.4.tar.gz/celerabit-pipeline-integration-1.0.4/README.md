
# CELERABIT PIPELINE INTEGRATION TOOLS

This package helps to integrate CI/CD processes with [celerabit platform](https://www.celerabit.com)

**REQUIEREMENTS**

None.
  
**USAGE**

```
python3 -m celerabitpipelineintegration <operation> [ags] [<flags>]
```

## Operation `authenticate`
Generates an [authentication token](https://app.celerabit.com).  This token will be input for secure operations.

### **Examples**

- Generate authentication token

    ```sh
    python3 -m celerabitpipelineintegration authenticate login "myemail@mydomain.com" password "secretpassword"
    ```
    You must replace `myemail@mydomain.com` and `secretpassword` for your valid credentials in celerabit platform.
    The Output of this operation is an alphanumeric token like this:
    ```
    eyJhbGciOiJIUzI1NiIsInR5cCI6Ikicm9sZXMiOm51bGx9LCJpYXQiOjE2NzIyNTQyMDAsImV4cCI6MTY3MjI2MTQwMH0cWBm8Iua2sUFkHbr89epcfN9EtwBDKtqoLMUtdXJSk
    ```

## Operation `run`
This operation runs a performance testing scenario and waitwait for it to finish.

### **Examples**

- Runs a scenario and waits for the execution to finish. If the scenario has not finished in 120 seconds (2 minutes), it will throw an exception.

    ```sh
    python3 -m celerabitpipelineintegration run token "nR5cCI6Ikicm9sZXMiOm51bGYXQiOjE2NzIyNDAsImV4cCI6MTY3MjI2MTQwMH0" client "My client Name" application "My application Name" scenario "My scenario code" timeout 120
    ```
    You must replace `nR5cCI6Ikicm9sZXMiOm51bGx9LCJpYXQiOjE2NzIyNTQyMDAsImV4cCI6MTY3MjI2MTQwMH0` for a valid authentication token, `My client Name` for your client name in celerabit platform, `My application Name` for the name of the application in celerabit platform aich the scneario belongs to, and `My scenario code` for the code of the existing scenario that you want to run.  
    
    >If **silent mode** is needed to avoid verbose info messages, you can add the flag `-q` at the end of the execution command line.

    The output of the command is a json object that specifies the new job id:
    ```
    {
        "jobId": 1158298, 
        "status": "SUCCESS", 
        "dateCreated": "2023-01-01T17:01:01.851Z", 
        "duration": 178.913196, 
        "kpiLatency": 3000, 
        "kpiErrors": 5, 
        "kpiThroughput": 100, 
        "kpiDeviation": 3000, 
        "metricLatency": 27.74, 
        "metricErrors": 0.35, 
        "metricThroughput": 1659057.06, 
        "metricDeviation": 52.36, 
        "complianceLatency": 199.08, 
        "complianceErrors": 192.94, 
        "complianceThroughput": 200, 
        "complianceDeviation": 198.25
    }
    ```

    Ih this response:

    | Attribute | Type | Description |
    | -- | -- | -- |
    | `jobId` | Job Info | Id corresponding the new created job for this scenario run. |
    | `status` | Job Info | Indicates if the job finished in `SUCCESS` or `ERROR` status. |
    | `dateCreated` | Job Info | Date and time the job starts its execution. |
    | `duration` | Job Info | Indicates the seconds the job took to finalize. |
    | `kpiLatency` | KPI | Objective value defined for the scenario average latency. |
    | `kpiErrors` | KPI | Objective value defined for the scenario errors percentage. |
    | `kpiThroughput` | KPI | Objective value defined for the scenario capacity (requests attended per minute). |
    | `kpiDeviation` | KPI | Objective value defined for the standard deviation for scenario average latency. |
    | `metricLatency` | Metric | Measured value for the scenario average latency in this run (For this `jobId`). |
    | `metricErrors` | Metric | Measured value for the scenario errors percentage in this run (For this `jobId`). |
    | `metricThroughput` | Metric | Measured value for the capacity (requests attended per minute) in this run (For this `jobId`). |
    | `metricDeviation` | Metric | Measured value for the standard deviation for scenario average latency in this run (For this `jobId`). |
    | `complianceLatency` | Compliance | Latency compliance (latency metric vs latency KPI). |
    | `complianceErrors` | Compliance | Errors percentage compliance (Errors percentage metric vs Errors percentage KPI). |
    | `complianceThroughput` | Compliance | Capacity compliance (Capacity metric vs Capacity KPI). |
    | `complianceDeviation` | Compliance | Deviation compliance (Deviation metric vs Deviation KPI). |
    

## Operation `eval-job-results`
Receives the json structure resulting from executing a scenario and evaluates its compliance by giving a tolerance level.

### **Examples**

- Receive the json structure resulting of executing an scenario and evaluates its compliance giving a tolerance level.

    ```sh
    python3 -m celerabitpipelineintegration eval-job-results job-result "$EXEC_RESULT" tolerance "latency=0.8,throughput=0.5,errors=0.95,deviation=0.2"
    ```
    >The output of this command is an string with the compliance validation errors.  If there is not, the string will be empty.

    In this example, the `EXEC_RESULT` variable contains the **json** structure returned by using the [run](#Operation-run) operation.  The values sent in the `tolerance` parameter specify the minimum percentage of compliance accepted for the executed scenario.  For the example:
    
    | Performance dimension | Tolerance (Minimun compliance) |
    | -- | -- |
    | `latency` | `0.8` (80%) |
    | `throughput` | `0.5` (50%) |
    | `errors` | `0.95` (95%) |
    | `deviation` | `0.2` (20%) |

    If no tolerance value is specified for a performance dimension (Latency, Throughput, errors, deviation), the default tolerance would be zero. It means that a minimum compliance of 100% will be evaluated.
