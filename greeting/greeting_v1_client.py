"""Generated client library for greeting version v1."""
# NOTE: This file is autogenerated and should not be edited by hand.
from apitools.base.py import base_api
from . import greeting_v1_messages as messages


class GreetingV1(base_api.BaseApiClient):
  """Generated client library for service greeting version v1."""

  MESSAGES_MODULE = messages
  BASE_URL = u'https://dash-test-1.appspot.com/_ah/api/greeting/v1/'

  _PACKAGE = u'greeting'
  _SCOPES = [u'https://www.googleapis.com/auth/userinfo.email']
  _VERSION = u'v1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'GreetingV1'
  _URL_VERSION = u'v1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None):
    """Create a new greeting handle."""
    url = url or self.BASE_URL
    super(GreetingV1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers)
    self.api = self.ApiService(self)

  class ApiService(base_api.BaseApiService):
    """Service class for the api resource."""

    _NAME = 'api'

    def __init__(self, client):
      super(GreetingV1.ApiService, self).__init__(client)
      self._upload_configs = {
          }

    def Authcheck(self, request, global_params=None):
      """Authcheck method for the api service.

      Args:
        request: (GreetingAuthcheckRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (MainResult) The response message.
      """
      config = self.GetMethodConfig('Authcheck')
      return self._RunMethod(
          config, request, global_params=global_params)

    Authcheck.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'greeting.authcheck',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'greetings/authcheck',
        request_field='',
        request_type_name=u'GreetingAuthcheckRequest',
        response_type_name=u'MainResult',
        supports_download=False,
    )

    def Create(self, request, global_params=None):
      """Create method for the api service.

      Args:
        request: (Greeting) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Greeting) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'greeting.create',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'greetings/create',
        request_field='<request>',
        request_type_name=u'Greeting',
        response_type_name=u'Greeting',
        supports_download=False,
    )

    def Delete(self, request, global_params=None):
      """Delete method for the api service.

      Args:
        request: (Greeting) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Greeting) The response message.
      """
      config = self.GetMethodConfig('Delete')
      return self._RunMethod(
          config, request, global_params=global_params)

    Delete.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'greeting.delete',
        ordered_params=[u'id'],
        path_params=[u'id'],
        query_params=[],
        relative_path=u'greetings/{id}',
        request_field='<request>',
        request_type_name=u'Greeting',
        response_type_name=u'Greeting',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      """Get method for the api service.

      Args:
        request: (GreetingGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Greeting) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'greeting.get',
        ordered_params=[u'id'],
        path_params=[u'id'],
        query_params=[],
        relative_path=u'greetings/{id}',
        request_field='',
        request_type_name=u'GreetingGetRequest',
        response_type_name=u'Greeting',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      """List method for the api service.

      Args:
        request: (GreetingListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (GreetingCollection) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'greeting.list',
        ordered_params=[],
        path_params=[],
        query_params=[u'limit', u'order', u'pageToken'],
        relative_path=u'greetings/list',
        request_field='',
        request_type_name=u'GreetingListRequest',
        response_type_name=u'GreetingCollection',
        supports_download=False,
    )

    def Setup2(self, request, global_params=None):
      """Setup2 method for the api service.

      Args:
        request: (GreetingSetup2Request) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (MainResult) The response message.
      """
      config = self.GetMethodConfig('Setup2')
      return self._RunMethod(
          config, request, global_params=global_params)

    Setup2.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'greeting.setup2',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'greetings/setup2',
        request_field='',
        request_type_name=u'GreetingSetup2Request',
        response_type_name=u'MainResult',
        supports_download=False,
    )