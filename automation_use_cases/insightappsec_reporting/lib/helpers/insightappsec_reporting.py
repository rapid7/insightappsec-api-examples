import os
import json
import logging
from .insightappsec import InsightAppSec


def generate_reports(api_key, region, report_config, report_format):
    url = f"https://{region}.api.insight.rapid7.com/ias/v1"
    api = InsightAppSec(url=url, api_key=api_key)

    # For each config defined in settings
    for config in report_config:
        try:
            # Get app
            app_name = config.get("app")
            logging.info(f"Application name: {app_name}")
            app = api.search("APP", f"app.name='{app_name}'", "")

            if app is not None and app != []:
                app_id = app[0].get("id")
                logging.info(f"Application ID: {app_id}")
            else:
                logging.info(f"App {app_name} not found. Moving to next configuration")
                continue

            # Get scan config
            scan_config_name = config.get("scan_config")
            logging.info(f"Scan config: {scan_config_name}")
            scan_config = api.search("SCAN_CONFIG", f"scanconfig.name='{scan_config_name}'", "")

            if scan_config is not None and scan_config != []:
                scan_config_id = scan_config[0].get("id")
                logging.info(f"Scan config ID: {scan_config_id}")
            else:
                logging.info(f"Scan config {scan_config_name} not found. Moving to next configuration")
                continue

            # Get scans with app ID and scan config ID
            scans = api.search("SCAN", f"scan.app.id='{app_id}'&&"
                                       f"scan.scan_config.id='{scan_config_id}'", "?sort=scan.submit_time,DESC")

            # Get the most recent scan
            if scans is not None and scans != []:
                scan = scans[0]
                scan_id = scan.get("id")
                logging.info(f"Latest scan ID: {scan_id}")
            else:
                logging.info(f"No scans found for app {app_name} and scan config {scan_config}. "
                             f"Moving to next configuration")
                continue

            # Get vulns, severities, and modules from the most recent scan
            vulns = api.search("VULNERABILITY", f"vulnerability.scans.id='{scan_id}'", "")
            logging.info(f"Vulnerability count: {len(vulns)}")
            severities = get_severities(vulns)
            modules = get_modules(vulns, api)

            # Write reports
            scan_date = scan.get("completion_time").split(".")[0].replace(":", "")
            json_args = {"indent": 4, "sort_keys": True} if report_format.get("pretty_print") is True else {}

            write_report(json.dumps(modules, **json_args), f"Modules-{app_name}-{scan_config_name}-{scan_date}")
            write_report(json.dumps(severities, **json_args), f"Severities-{app_name}-{scan_config_name}-{scan_date}")
            write_report(json.dumps(vulns, **json_args), f"Vulnerabilities-{app_name}-{scan_config_name}-{scan_date}")
        except Exception as e:
            logging.error(f"Error generating reports for configuration: {str(config)}", e)


def get_modules(vulns, api):
    modules = {}
    try:
        for vuln in vulns:
            # Only need the first variance because all have the same module ID
            variance = vuln.get("variances")[0]
            if variance is None:
                continue
            module = api.get_module(variance.get("module").get("id"))
            module_name = module.get("name")
            if module_name in modules:
                modules[module_name] += 1
            else:
                modules[module_name] = 1
        return modules
    except Exception as e:
        logging.error("Error retrieving modules", e)
        return None


def get_severities(vulns):
    severities = {}
    try:
        for vuln in vulns:
            severity = vuln.get("severity")
            if severity in severities:
                severities[severity] += 1
            else:
                severities[severity] = 1
        return severities
    except Exception as e:
        logging.error("Error retrieving severities", e)
        return None


def write_report(report_content, report_name):
    try:
        with open(os.path.realpath(f"../reports//{report_name}.json"), "w") as file:
            file.write(report_content)
        logging.info(f"Report created: {report_name}")
    except Exception as e:
        logging.error(f"Error writing report: {report_name}", e)



