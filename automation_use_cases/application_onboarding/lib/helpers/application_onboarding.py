import logging
from .insightappsec import InsightAppSec


def create_application(api_key, region, settings):
    url = f"https://{region}.api.insight.rapid7.com/ias/v1"
    api = InsightAppSec(url=url, api_key=api_key)

    onboarding_config = settings.get("onboarding_config")
    engine_group = settings.get("engine_group")

    for config in onboarding_config:
        try:
            # Check to see if app already exists
            app_name = config.get("app_name")
            app_results = api.search("APP", f"app.name='{app_name}'")

            # Create application if it doesn't already exist
            if app_results is None or app_results == []:
                app = {"name": app_name}
                app_id = api.create_app(app)
            else:
                logging.info(f"Application {app_name} already exists. Continuing to next configuration")
                continue

            # Get attack template
            attack_template_name = config.get("attack_template")
            attack_template_results = api.search("ATTACK_TEMPLATE", f"attacktemplate.name='{attack_template_name}'")

            if attack_template_results is not None and attack_template_results != []:
                attack_template_id = attack_template_results[0].get("id")
            else:
                logging.info(f"Attack template {attack_template_name} not found. Continuing to next configuration")
                continue

            # Get engine group
            engine_group_name = engine_group.get("name")
            engine_group_results = api.search("ENGINE_GROUP", f"enginegroup.name='{engine_group_name}'")

            if engine_group_results is not None and engine_group_results != []:
                engine_group_id = engine_group_results[0].get("id")
            else:
                logging.info(f"Engine group {engine_group_name} not found. Continuing to next configuration")
                continue

            scan_config = {
                "name": config.get("app_name") + " Scan Config",
                "app": {"id": app_id},
                "attack_template": {"id": attack_template_id},
                "assignment": {"type": "ENGINE_GROUP", "id": engine_group_id,
                               "environment": engine_group.get("environment")}
            }

            # Create scan config
            scan_config_id = api.create_scan_config(scan_config)

            # Check to see if target already exists
            url = config.get("url")
            domain = url.strip("http://").strip("https://")
            target_results = api.search("TARGET", f"target.domain='{domain}'")

            # Create new target if it doesn't exist
            if target_results is None or target_results == []:
                target = {"domain": domain, "enabled": True}
                api.create_target(target)
            else:
                logging.info(f"Target {domain} already exists. Continuing onboarding process")

            # Update scan config options to add URL
            options = {
                "crawl_config": {"scope_constraint_list": [{"url": url + "/*", "exclusion": "INCLUDE"}],
                                 "seed_url_list": [{"value": url}]}
            }
            api.update_scan_config_options(scan_config_id, options)

            # Submit scan
            if settings.get("scan_on_creation") and app_id is not None and scan_config_id is not None:
                scan_submission = {"app": {"id": app_id}, "scan_config": {"id": scan_config_id}}
                scan_id = api.submit_scan(scan_submission)
            else:
                logging.info("Continuing to next configuration without scanning")
                continue

            # Get scan status
            scan = api.get_scan(scan_id)
            scan_status = scan.get("status")
            logging.info(f"Scan status: {scan_status}")
        except Exception as e:
            logging.error(f"Error in application onboarding for configuration: {str(config)}", e)
