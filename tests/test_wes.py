import mock
import pytest
import inspect

from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient, ResourceDecorator
from bravado.testing.response_mocks import BravadoResponseMock
from wes_client.util import WESClient

from synorchestrator.wes.client import _get_wes_opts
from synorchestrator.wes.client import _init_http_client
from synorchestrator.wes.client import WESAdapter
from synorchestrator.wes.client import load_wes_client
from synorchestrator.wes.wrapper import WES


@pytest.fixture()
def mock_wes_config():
    mock_wes_config = {
        'mock_wes': {
            'auth': 'auth_token',
            'auth_type': 'token',
            'host': '0.0.0.0:8080',
            'proto': 'https'
        }
    }
    yield mock_wes_config


def test__get_wes_opts(mock_wes_config, monkeypatch):
    monkeypatch.setattr('synorchestrator.wes.client.wes_config', 
                        lambda: mock_wes_config)
    test_wes_opts = _get_wes_opts('mock_wes')

    assert test_wes_opts == mock_wes_config['mock_wes']


def test__init_http_client(mock_wes_config):
    mock_opts = mock_wes_config['mock_wes']
    test_http_client = _init_http_client(opts=mock_opts)

    assert isinstance(test_http_client, RequestsClient)
    assert test_http_client.authenticator.host == mock_opts['host']
    assert test_http_client.authenticator.api_key == mock_opts['auth']


def test_load_wes_client_from_spec(mock_wes_config, monkeypatch):
    monkeypatch.setattr('synorchestrator.wes.client._get_wes_opts', 
                        lambda x: mock_wes_config['mock_wes'])

    mock_http_client = RequestsClient()
    test_wes_client = load_wes_client(service_id='mock_wes',
                                      http_client=mock_http_client)

    assert isinstance(test_wes_client, ResourceDecorator)


@pytest.fixture()
def mock_wes_client(request):
    mock_wes_client = mock.Mock(name='mock WESClient')
    with mock.patch('wes_client.util.WESClient', 
                    autospec=True, spec_set=True):
        yield mock_wes_client


class TestWESAdapter:
    """
    Tests methods for the :class:`WESAdapter` class, which translate
    methods from the workflow-service :class:`WESClient` class to match
    the interface defined in the GA4GH WES API spec. The tests below 
    check whether the adapter methods are calling adaptee class methods
    with the correct signature.
    """
    def test_init(self, mock_wes_config):   
        mock_wes_client = WESClient(mock_wes_config['mock_wes'])

        test_wes_adapter = WESAdapter(wes_client=mock_wes_client)
        
        assert isinstance(test_wes_adapter, WESAdapter)
        assert hasattr(test_wes_adapter, '_wes_client')
        assert isinstance(test_wes_adapter._wes_client, WESClient)
    
    def test_GetServiceInfo(self, mock_wes_client):
        mock_response = {}
        mock_wes_client.get_service_info.return_value = mock_response

        wes_adapter = WESAdapter(wes_client=mock_wes_client)
        test_args = {arg: '' for arg in 
                     inspect.getargspec(WESClient.get_service_info)[0][1:]}
        test_response = wes_adapter.GetServiceInfo()

        mock_wes_client.get_service_info.assert_called_once_with(**test_args)
        assert test_response == mock_response

    def test_ListRuns(self, mock_wes_client):
        mock_response = {}
        mock_wes_client.list_runs.return_value = mock_response

        wes_adapter = WESAdapter(wes_client=mock_wes_client)
        test_args = {arg: '' for arg in 
                     inspect.getargspec(WESClient.list_runs)[0][1:]}
        test_response = wes_adapter.ListRuns()

        mock_wes_client.list_runs.assert_called_once_with(**test_args)
        assert test_response == mock_response

    def test_RunWorkflow(self, mock_wes_client):
        mock_request = {'workflow_url': '',
                        'workflow_params': '',
                        'attachment': ''}
        mock_response = {}
        mock_wes_client.run.return_value = mock_response

        wes_adapter = WESAdapter(wes_client=mock_wes_client)
        test_args = {arg: '' for arg in 
                     inspect.getargspec(WESClient.run)[0][1:]}
        test_response = wes_adapter.RunWorkflow(mock_request)

        mock_wes_client.run.assert_called_once_with(**test_args)
        assert test_response == mock_response

    def test_CancelRun(self, mock_wes_client):
        mock_response = {}
        mock_wes_client.cancel.return_value = mock_response

        wes_adapter = WESAdapter(wes_client=mock_wes_client)
        test_args = {arg: '' for arg in 
                     inspect.getargspec(WESClient.cancel)[0][1:]}
        test_response = wes_adapter.CancelRun(run_id='')

        mock_wes_client.cancel.assert_called_once_with(**test_args)
        assert test_response == mock_response

    def test_GetRunStatus(self, mock_wes_client):
        mock_response = {}
        mock_wes_client.get_run_status.return_value = mock_response

        wes_adapter = WESAdapter(wes_client=mock_wes_client)
        test_args = {arg: '' for arg in 
                     inspect.getargspec(WESClient.get_run_status)[0][1:]}
        test_response = wes_adapter.GetRunStatus(run_id='')

        mock_wes_client.get_run_status.assert_called_once_with(**test_args)
        assert test_response == mock_response

    def test_GetRunLog(self, mock_wes_client):
        mock_response = {}
        mock_wes_client.get_run_log.return_value = mock_response

        wes_adapter = WESAdapter(wes_client=mock_wes_client)
        test_args = {arg: '' for arg in 
                     inspect.getargspec(WESClient.get_run_log)[0][1:]}
        test_response = wes_adapter.GetRunLog(run_id='')

        mock_wes_client.get_run_log.assert_called_once_with(**test_args)
        assert test_response == mock_response


def test_load_wes_client_from_lib(mock_wes_config, monkeypatch):
    monkeypatch.setattr('synorchestrator.wes.client._get_wes_opts', 
                        lambda x: mock_wes_config['mock_wes'])
    
    mock_http_client = RequestsClient()
    test_wes_client = load_wes_client(service_id='mock_wes',
                                      client_library='workflow-service',
                                      http_client=mock_http_client)

    spec_methods = ['GetServiceInfo', 
                    'ListRuns', 
                    'RunWorkflow', 
                    'CancelRun',
                    'GetRunStatus', 
                    'GetRunLog']
    assert isinstance(test_wes_client, WESAdapter)
    assert all([hasattr(test_wes_client, method) for method in spec_methods])


@pytest.fixture(params=[None, 'workflow-service'])
def mock_api_client(request):
    if request.param is None:
        mock_api_client = mock.Mock(name='mock SwaggerClient')
        with mock.patch.object(SwaggerClient, 'from_spec', 
                            return_value=mock_api_client):
            yield mock_api_client
    else:
        mock_api_client = mock.Mock(name='mock WESAdapter')
        with mock.patch('synorchestrator.wes.client.WESAdapter', 
                        autospec=True):
            yield mock_api_client


class TestWES:
    """
    Tests methods for the :class:`WES` class, which serve as the main
    Python interface for the GA4GH WES API. The tests below are primarily
    checking whether each method is making calls to the correct path
    and correctly handling responses.
    """
    def test_init(self, mock_api_client):
        wes_instance = WES(wes_id='mock_wes', 
                           api_client=mock_api_client)

        assert hasattr(wes_instance, 'api_client')
        assert hasattr(wes_instance.api_client, 'GetServiceInfo')  

    def test_get_service_info_bravado(self, mock_api_client):
        mock_service_info = {'workflow_type_versions': ['CWL', 'WDL']}

        mock_response = BravadoResponseMock(result=mock_service_info)
        mock_api_client.GetServiceInfo.return_value.response = mock_response
        wes_instance = WES(wes_id='mock_wes', 
                           api_client=mock_api_client)
        test_service_info = wes_instance.get_service_info()

        assert isinstance(test_service_info, dict) 
        assert test_service_info == mock_service_info

    def test_get_service_info_direct(self, mock_api_client):
        mock_service_info = {'workflow_type_versions': ['CWL', 'WDL']}

        mock_api_client.GetServiceInfo.return_value = mock_service_info

        wes_instance = WES(wes_id='mock_wes', 
                           api_client=mock_api_client)
        test_service_info = wes_instance.get_service_info()

        assert isinstance(test_service_info, dict) 
        assert test_service_info == mock_service_info

    def test_list_runs(self, mock_api_client):
        mock_runs = ['foo', 'bar']

        mock_response = BravadoResponseMock(result=mock_runs)
        mock_api_client.ListRuns.return_value.response = mock_response

        wes_instance = WES(wes_id='mock_wes', 
                           api_client=mock_api_client)
        test_runs = wes_instance.list_runs()

        assert isinstance(test_runs, list) 
        assert test_runs == mock_runs

    def test_run_workflow(self, mock_api_client):
        mock_run_id = {'run_id': 'foo'}

        mock_response = BravadoResponseMock(result=mock_run_id)
        mock_api_client.RunWorkflow.return_value.response = mock_response

        wes_instance = WES(wes_id='mock_wes', 
                           api_client=mock_api_client)
        test_run_id = wes_instance.run_workflow(request={})

        assert isinstance(test_run_id, dict) 
        assert test_run_id == mock_run_id

    def test_get_run(self, mock_api_client):
        mock_run_log = {'run_id': 'foo',
                        'request': {},
                        'state': '',
                        'run_log': {},
                        'task_logs': [],
                        'outputs': {}}

        mock_response = BravadoResponseMock(result=mock_run_log)
        mock_api_client.GetRunLog.return_value.response = mock_response

        wes_instance = WES(wes_id='mock_wes', 
                           api_client=mock_api_client)
        test_run_log = wes_instance.get_run(id='foo')

        assert isinstance(test_run_log, dict) 
        assert test_run_log == mock_run_log

    def test_get_run_status(self, mock_api_client):
        mock_run_status = {'run_id': 'foo',
                           'state': ''}

        mock_response = BravadoResponseMock(result=mock_run_status)
        mock_api_client.GetRunStatus.return_value.response = mock_response

        wes_instance = WES(wes_id='mock_wes', 
                           api_client=mock_api_client)
        test_run_status = wes_instance.get_run_status(id='foo')

        assert isinstance(test_run_status, dict) 
        assert test_run_status == mock_run_status
