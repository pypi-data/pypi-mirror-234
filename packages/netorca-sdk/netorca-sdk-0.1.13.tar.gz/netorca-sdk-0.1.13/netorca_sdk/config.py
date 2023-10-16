import logging

AUTH_ENDPOINT = "/api-token-auth/"
TEAM_ENDPOINT = "/account/teams/"
API_VERSION = "/v1"
URL_PREFIX = "/orcabase"
VALIDATE_CONSUMER_SUBMISSION_ENDPOINT = "/orcabase/consumer/submissions/validate/"
SUBMIT_CONSUMER_SUBMISSION_ENDPOINT = "/orcabase/consumer/submissions/submit/"
VALIDATE_SERVICEOWNER_SUBMISSION_ENDPOINT = "/orcabase/serviceowner/services/validate/"
SUBMIT_SERVICEOWNER_SUBMISSION_ENDPOINT = "/orcabase/serviceowner/services/"
SUBMIT_SERVICEOWNER_SUBMISSION_DOCS_ENDPOINT = "/orcabase/serviceowner/services/$id/docs/"
SERVICEOWNER_SERVICE_ITEMS_ENDPOINT = "/orcabase/serviceowner/service_items/"
CONSUMER_SERVICE_ITEMS_ENDPOINT = "/orcabase/consumer/service_items/"
CHANGE_INSTANCES_ENDPOINT = "/orcabase/serviceowner/change_instances/"
DEPLOYED_ITEMS_ENDPOINT = "/orcabase/serviceowner/deployed_items/"
SERVICE_CONFIG_ENDPOINT = "/orcabase/serviceowner/service_configs/"
SERVICEOWNER_DEPENDENT_SERVICE_ITEMS_ENDPOINT = "/orcabase/serviceowner/service_items/dependent/"
CONSUMER_DEPENDENT_SERVICE_ITEMS_ENDPOINT = "/orcabase/consumer/service_items/dependent/"

RETRY_TIMES = 1  # number of times request will be retried

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOG_LEVEL = logging.INFO

logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
logger = logging.getLogger("netorca_sdk")
