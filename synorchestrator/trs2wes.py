from synorchestrator.config import config_path
from synorchestrator.config import queue_config
from synorchestrator.config import set_yaml
from synorchestrator.trs.wrapper import TRS


def fetch_queue_workflow(queue_id):
    wf_config = queue_config()[queue_id]
    trs_instance = TRS(wf_config['trs_id'])
    wf_descriptor = trs_instance.get_workflow_descriptor(
        id=wf_config['workflow_id'],    
        version_id=wf_config['version_id'], 
        type=wf_config['workflow_type']
    )
    wf_files = trs_instance.get_workflow_files(
        id=wf_config['workflow_id'],
        version_id=wf_config['version_id'],
        type=wf_config['workflow_type']
    )
    wf_config['workflow_url'] = wf_descriptor['url']
    attachment_paths = [wf_file['path'] for wf_file in wf_files
                       if wf_file['file_type'] == 'SECONDARY_DESCRIPTOR']
    wf_attachments = []
    for attachment in attachment_paths:
        attachment_file = trs_instance.get_workflow_descriptor_relative(
            id=wf_config['workflow_id'],
            version_id=wf_config['version_id'],
            type=wf_config['workflow_type'],
            relative_path=attachment
        )
        wf_attachments.append(attachment_file['url'])
    wf_config['workflow_attachments'] = wf_attachments
    set_yaml('queues', queue_id, wf_config)
    return wf_config

    