import mock
import pytest

from wfinterop.testbed import poll_services
from wfinterop.testbed import get_checker_id
from wfinterop.testbed import check_workflow
from wfinterop.testbed import check_all


def test_poll_services(mock_queue_config, 
                       mock_trs,
                       mock_wes,
                       monkeypatch):
    monkeypatch.setattr('wfinterop.testbed.queue_config', 
                        lambda: mock_queue_config)
    monkeypatch.setattr('wfinterop.testbed.TRS', 
                        lambda trs_id: mock_trs) 
    monkeypatch.setattr('wfinterop.testbed.WES', 
                        lambda wes_id: mock_wes)  

    test_service_status = poll_services()
    assert test_service_status == {'toolregistries': {'mock_trs': True},
                                   'workflowservices': {'local': True}}


def test_get_checker_id(mock_trs,  monkeypatch):
    mock_checker_url = '/%23workflow%2Fmock_wf%2F_cwl_checker'
    mock_trs.get_workflow.return_value = {'checker_url': mock_checker_url}
    mock_checker_id = 'mock_wf/_cwl_checker'

    test_checker_id = get_checker_id(mock_trs, 'mock_wf')

    assert test_checker_id == mock_checker_id


def test_check_workflow(mock_queue_config, 
                        mock_trs, 
                        monkeypatch):
    monkeypatch.setattr('wfinterop.testbed.queue_config', 
                        lambda: mock_queue_config)
    monkeypatch.setattr('wfinterop.testbed.TRS', 
                        lambda trs_id: mock_trs)                        
    monkeypatch.setattr('wfinterop.testbed.get_checker_id', 
                        lambda x,y: 'mock_wf_checker')
    monkeypatch.setattr('wfinterop.testbed.add_queue', 
                        lambda **kwargs: None)
    monkeypatch.setattr('wfinterop.testbed.create_submission', 
                        lambda **kwargs: None)
    mock_trs.get_workflow_tests.return_value = [{'content': '', 'url': ''}]

    mock_submission_log = {
        'mock_wf': {
            'mock_sub': {
                'queue_id': 'mock_queue',
                'job': '',
                'wes_id': '',
                'run_id': 'mock_run',
                'status': 'QUEUED',
                'start_time': ''
            }
        }
    }
    monkeypatch.setattr('wfinterop.testbed.run_queue', 
                        lambda x: mock_submission_log)

    test_submission_log = check_workflow(queue_id='mock_queue_1', 
                                         wes_id='local')

    assert test_submission_log == mock_submission_log


def test_check_all(mock_queue_config, monkeypatch):
    monkeypatch.setattr('wfinterop.testbed.queue_config', 
                        lambda: mock_queue_config)

    mock_submission_logs = {
        'mock_wes_1': {
            'mock_wf': {
                'mock_sub': {
                    'queue_id': 'mock_queue',
                    'job': '',
                    'wes_id': 'mock_wes_1',
                    'run_id': 'mock_run',
                    'status': 'QUEUED',
                    'start_time': ''
                }
            }
        },
        'mock_wes_2': {
            'mock_wf': {
                'mock_sub': {
                    'queue_id': 'mock_queue',
                    'job': '',
                    'wes_id': 'mock_wes_2',
                    'run_id': 'mock_run',
                    'status': 'QUEUED',
                    'start_time': ''
                }
            }
        }
    }
    monkeypatch.setattr('wfinterop.testbed.check_workflow', 
                        lambda x,y: mock_submission_logs[y])

    mock_workflow_wes_map = {
        'mock_wf': ['mock_wes_1', 'mock_wes_2']
    }
    test_submission_logs = check_all(mock_workflow_wes_map)
    assert all([log in mock_submission_logs.values() 
                for log in test_submission_logs])