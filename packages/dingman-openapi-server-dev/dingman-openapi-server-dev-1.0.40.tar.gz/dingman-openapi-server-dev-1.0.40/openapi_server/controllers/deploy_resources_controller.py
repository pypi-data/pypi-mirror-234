import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.deploy_platform_resource import DeployPlatformResource  # noqa: E501
from openapi_server.models.deploy_resources import DeployResources  # noqa: E501
from openapi_server.models.dingman_error import DingmanError  # noqa: E501
from openapi_server.models.dingman_response import DingmanResponse  # noqa: E501
from openapi_server import util


def get_deploy_platform_resource_by_pop(app_service_name, pop_name):  # noqa: E501
    """Get DeployPlatformResources under an app service for the specific pop

    This operation returns the DeployPlatformResources data under the specified app-service for the specified pop # noqa: E501

    :param app_service_name: 
    :type app_service_name: str
    :param pop_name: 
    :type pop_name: str

    :rtype: Union[DeployPlatformResource, Tuple[DeployPlatformResource, int], Tuple[DeployPlatformResource, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_deploy_platform_resources(app_service_name):  # noqa: E501
    """Get DeployPlatformResources under an app service for all pops

    This operation returns the DeployPlatformResources data under the specified app-service for all pops # noqa: E501

    :param app_service_name: 
    :type app_service_name: str

    :rtype: Union[List[DeployPlatformResource], Tuple[List[DeployPlatformResource], int], Tuple[List[DeployPlatformResource], int, Dict[str, str]]
    """
    return 'do some magic!'


def get_deploy_resource_overlays(app_service_name):  # noqa: E501
    """Get DeployResourceOverlays for an app service

    This operation returns the DeployResourceOverlays data under the specified app-service # noqa: E501

    :param app_service_name: 
    :type app_service_name: str

    :rtype: Union[Dict[str, DeployResources], Tuple[Dict[str, DeployResources], int], Tuple[Dict[str, DeployResources], int, Dict[str, str]]
    """
    return 'do some magic!'


def get_deploy_resources(app_service_name):  # noqa: E501
    """Get DeployResources under an app service

    This operation returns the DeployResources data under the specified app-service # noqa: E501

    :param app_service_name: 
    :type app_service_name: str

    :rtype: Union[DeployResources, Tuple[DeployResources, int], Tuple[DeployResources, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_deploy_resources_by_pop(app_service_name, pop_name):  # noqa: E501
    """Get DeployResources under an app service for the specified pop

    This operation returns the DeployResources data under the specified app-service for the specified pop # noqa: E501

    :param app_service_name: 
    :type app_service_name: str
    :param pop_name: 
    :type pop_name: str

    :rtype: Union[DeployResources, Tuple[DeployResources, int], Tuple[DeployResources, int, Dict[str, str]]
    """
    return 'do some magic!'


def patch_deploy_resource_overlays(app_service_name, request_body):  # noqa: E501
    """Patch DeployResourceOverlays under an app service

    This operation patches the DeployResourceOverlays data under the specified app-service # noqa: E501

    :param app_service_name: 
    :type app_service_name: str
    :param request_body: A DeployResourceOverlays json body
    :type request_body: dict | bytes

    :rtype: Union[DingmanResponse, Tuple[DingmanResponse, int], Tuple[DingmanResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        request_body = {k: DeployResources.from_dict(v) for k, v in six.iteritems(connexion.request.get_json())}  # noqa: E501
    return 'do some magic!'


def patch_deploy_resources(app_service_name, deploy_resources):  # noqa: E501
    """Patch DeployResources under an app service

    This operation patches the DeployResources data under the specified app-service # noqa: E501

    :param app_service_name: 
    :type app_service_name: str
    :param deploy_resources: A DeployResources json body
    :type deploy_resources: dict | bytes

    :rtype: Union[DingmanResponse, Tuple[DingmanResponse, int], Tuple[DingmanResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        deploy_resources = DeployResources.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def put_deploy_resource_overlays(app_service_name, request_body):  # noqa: E501
    """Put DeployResourceOverlays for an app service

    This operation overwrites the DeployResourceOverlays data under the specified app-service # noqa: E501

    :param app_service_name: 
    :type app_service_name: str
    :param request_body: A DeployResourceOverlays json body
    :type request_body: dict | bytes

    :rtype: Union[DingmanResponse, Tuple[DingmanResponse, int], Tuple[DingmanResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        request_body = {k: DeployResources.from_dict(v) for k, v in six.iteritems(connexion.request.get_json())}  # noqa: E501
    return 'do some magic!'


def put_deploy_resources(app_service_name, deploy_resources):  # noqa: E501
    """Put DeployResources for an app-service

    This operation overwrites the DeployResources data under the specified app-service # noqa: E501

    :param app_service_name: 
    :type app_service_name: str
    :param deploy_resources: A DeployResources json body
    :type deploy_resources: dict | bytes

    :rtype: Union[DingmanResponse, Tuple[DingmanResponse, int], Tuple[DingmanResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        deploy_resources = DeployResources.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
