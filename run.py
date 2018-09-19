from wfinterop import config
from wfinterop import orchestrator
from wfinterop import testbed


config.add_queue(queue_id='demo_queue',
                 wf_type='CWL',
                 wf_id='github.com/dockstore-testing/md5sum-checker',
                 version_id='develop',
                 trs_id='dockstore')

config.add_workflowservice(service='local-wes',
                           host='localhost:8080',
                           auth={'Authorization': 'Bearer the-token'},
                           proto='http')


config.add_wes_opt(queue_ids='demo_queue', wes_id='local-wes')

orchestrator.run_job(queue_id='demo_queue',
                     wes_id='local-wes',
                     wf_jsonyaml='file://tests/testdata/md5sum.cwl.json')

orchestrator.monitor_queue(queue_id='demo_queue')
