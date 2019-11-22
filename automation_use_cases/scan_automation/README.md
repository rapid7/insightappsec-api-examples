# Scan Automation

## Getting Started
The Scan Automation solution is designed to automate the triggering and reporting of scans in InsightAppSec. Given a list of pairs of application names and scan config names, this script can automatically trigger and track the status of multiple InsightAppSec scans in parallel.

The steps for the scan automation process are executed as follows:

1. Grab application and scan config information from configuration file
2. Lookup and store IDs for application and scan config
3. Trigger the scans using the application and scan config IDs
4. Track status of the scans
5. Report on scan findings

### Configuration

To begin the process of scan automation, there must be at least one target application and scan config pair defined in the
`config/settings.yml` file. The `scan_info` section houses a list of `app_name` and `scan_config_name` pairs as well as a `status_check_interval` which will apply to all scans. The `app_name` field will hold
the name of the InsightAppSec application to scan. The `config` field will hold the name of the InsightAppSec
scan config to use for the scan. You should be sure that this scan config name belongs to the app that you specified. Below is an example of a valid `scan_info` configuration. The `status_check_interval` field represents the number of seconds between each status check while tracking the scan's progress. If left unspecified, this field defaults to 60 seconds.

```
scan_info:
  - app_name: Application 1
    scan_config_name: Config Name 1
  - app_name: Application 2
    scan_config_name: Config Name 2
  status_check_interval: 300
```

Connection settings must also be defined to connect to InsightAppSec and perform the required operations. Under 
`connection` in `config/settings.yml`, there are fields for both `region` and `api_key` to facilitate this 
connection.

```
connection:
  region: us
  api_key: 
```

Rapid7 recommends the encryption and secure storage of sensitive values such as the API key to adhere to best 
security practices. If an API key is not entered in `settings.yml`, then the script will prompt the user to 
enter one upon executing it.

## Usage

### Running the Script

The main script can be executed by navigating to the project's `bin` directory and entering the CLI command 
`python main.py`. This will launch the script and begin creating, triggering, and reporting on scans based off of the
settings defined in `settings.yml`. 

### Output

The script is designed to include logging as its logic is executed, written to a log file located in the `log` 
directory. These logs contain information about each operation being performed in the scan automation process, 
such as scan creation, scan status updates, and scan results.

```
2019-11-22 11:40:52.753562 - INFO - Region: us
2019-11-22 11:40:52.753562 - INFO - Launched new scan: 0000000-0000-0000-0000-000000000000
2019-11-22 11:40:52.753562 - INFO - Launched new scan: 0000000-0000-0000-0000-000000000001
2019-11-22 11:40:52.753562 - INFO - CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000000, First Application, Default): RUNNING
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000001, Second Application, Default): QUEUED
2019-11-22 11:40:52.753562 - INFO - CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000000, First Application, Default): COMPLETE
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000001, Second Application, Default): RUNNING
2019-11-22 11:40:52.753562 - INFO - CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000001, Second Application, Default): RUNNING
2019-11-22 11:40:52.753562 - INFO - CHECKING STATUS OF REMAINING SCANS... (Scan ID, App Name, Scan Config Name): STATUS
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000001, Second Application, Default): COMPLETE
2019-11-22 11:40:52.753562 - INFO - REPORTING VULNERABILITY COUNTS OF SCANS... (Scan ID, App Name, Scan Config Name): NUM VULNS
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000000, First Application, Default): 75
2019-11-22 11:40:52.753562 - INFO - (0000000-0000-0000-0000-000000000001, Second Application, Default): 0
```