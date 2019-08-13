import os
import requests

from parsl import python_app

# In both _http_stage_in and _ftp_stage_in the handling of
# file.local_path is rearranged: file.local_path is an optional
# string, so even though we are setting it, it is still optional
# and so cannot be used as a parameter to open.

def _http_stage_in(working_dir, outputs=[], staging_inhibit_output=True):
    file = outputs[0]
    if working_dir:
        os.makedirs(working_dir, exist_ok=True)
        local_path = os.path.join(working_dir, file.filename)
    else:
        local_path = file.filename

    file.local_path = local_path

    resp = requests.get(file.url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def _http_stage_in_app(dm, executor):
    return python_app(executors=[executor], data_flow_kernel=dm.dfk)(_http_stage_in)