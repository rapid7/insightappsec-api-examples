# Application Onboarding

## Getting Started

The Application Onboarding solution is designed to automate the creation and configuration of applications in 
InsightAppSec. The solution's configuration is intended to be minimal in the fields required for each application, 
thus allowing organizations to do bulk creation of applications as needed.

The steps for the application onboarding process are executed as follows:

1. Create new application
2. Create new scan configuration
3. Create new target (if needed) to whitelist scanning
4. Submit scan for newly created application (optional)

Each of these operations is performed in accordance with the settings specified in the solution's configuration.

### Configuration

To begin the process of application onboarding, there must be at least one configuration defined in the 
`config/settings.yml` file. The `onboarding_config` section houses this list of configurations. Each one is comprised 
of an application name, an attack template name, and a URL. All three of these fields are required to successfully 
create and configure a new application in InsightAppSec for scanning purposes.

```
onboarding_config:
  - app_name: App Name 1
    attack_template: All Modules
    url: https://website.com
  - app_name: App Name 2
    attack_template: SQL Injection
    url: https://otherwebsite.com
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

There is also a configuration field known as `engine_group`.

```
engine_group:
  name: Working Engines
  environment: ON_PREMISE
```

These engine group settings will be applied to each application created from this solution when performing scans in 
InsightAppSec. The `name` must be a valid engine group name, while the environment can either be `ON_PREMISE` or 
`CLOUD`.

Finally, there is the global `scan_immediately` option. This can be set to `true` or `false` and will determine whether 
a scan is immediately launched for each application after its creation and configuration. Note that setting this to 
`true` may result in the queueing of scans due to engine availability.

```
scan_immediately: false
```

## Usage

### Running the Script

The main script can be executed by navigating to the project's `bin` directory and entering the CLI command 
`python main.py`. This will launch the script and begin creating and configuring new applications based on the 
settings defined in `settings.yml`.

### Output

When the script has completed in its execution, the newly created applications should be available for use in 
InsightAppSec. Each application should contain its own scan configuration with options defined in accordance with the 
contents of this solution's configuration file. Any pending or ongoing scans and their results should also be visible 
under the Scans section in the UI.

The script is also designed to include logging as its logic is executed, written to a log file located in the `log` 
directory. These logs contain information about each operation being performed in the application onboarding process, 
such as application creation, scan configuration updates, and the launch of a new scan.

```
2019-11-12 14:26:12.405613 - INFO - Created new application: 00000000-0000-0000-0000-000000000000
2019-11-12 14:26:24.732567 - INFO - Created new scan config: 00000000-0000-0000-0000-000000000001
2019-11-12 14:27:56.326718 - INFO - Created new target: 00000000-0000-0000-0000-000000000002
2019-11-12 14:27:58.895227 - INFO - Updated scan config options: 00000000-0000-0000-0000-000000000001
2019-11-12 14:28:35.567345 - INFO - Launched new scan: 00000000-0000-0000-0000-000000000003
2019-11-12 14:29:42.208254 - INFO - Scan status: PENDING
```