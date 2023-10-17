# Rhythm
Rhythm allows you to design and control workflows made of Celery tasks. A workflow is a sequence of steps to run one after the other. Rhythm simplifies the process of executing workflows consisting of long-running tasks with reliability.

The following are the features of Rhythm workflows:
- If a workflow consisting of three steps (S1, S2, and S3) encounters a failure while executing S2 (even after retries by Celery), it is possible to resume the workflow later. Resuming the workflow with restart S2 with previous arguments and after its completion S3 will be run.
- A workflow can be paused and resumed later.
- You can keep track of which step is currently running, as well as its progress.

### Installation

```
pip install sca-rhythm
```

see on [pypi](https://pypi.org/project/sca-rhythm/)

### Prerequisites

Celery app should be configured with a mongo database backend.

### Create Tasks with `WorkflowTask` class

```python
import os
import time

from celery import Celery

from sca_rhythm import WorkflowTask

app = Celery("tasks")

@app.task(base=WorkflowTask, bind=True)
def task1(self, batch_id, **kwargs):
    print(f'task - {os.getpid()} 1 starts with {batch_id}')
    # do work
    time.sleep(1)

    # update progress to result backend
    # sets the task's state as "PROGRESS"
    self.update_progress({
        done: 2873,
        total: 100000
    })

    # do some more work
    return batch_id, {'return_obj': 'foo'}
```
#### :warning: Task Constraints :warning:
1. The task signature must contain `**kwargs` for the workflow orchestration to function.
2. The return type must be of list / tuple type and the first element of the return value is sent to the next task as its argument.

### Create Workflows with `Workflow` class

```python
from celery import Celery

from sca_rhythm import Workflow

steps = [
    {
        'name': 'inspect',
        'task': 'tasks.inspect'
    },
    {
        'name': 'archive',
        'task': 'tasks.archive'
    },
    {
        'name': 'stage',
        'task': 'tasks.stage'
    }
]

wf = Workflow(app, steps=steps, name='archive_batch')
wf.start('batch-id-test')
```

### Pause and Resume Workflows

Pausing a workflow stop the current running task and resuming a workflow will restart the stopped task with the same arguments.

```python
wf = Workflow(app, workflow_id='2f87decb-a431-472b-b26e-32c894993881')

wf.pause()

wf.resume()
```

### Build & Publish
```bash
poetry install
poetry publish --build
```