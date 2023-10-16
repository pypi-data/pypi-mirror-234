### Installation
```bash
$ pip install django-command-queue
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_command_queue']
```

optional
name|default|description
-|-|-
`COMMAND_WORKER_SLEEP`|`0.1`|`command_queue_worker` sleep interval
`COMMAND_WORKER_RESTART`|`None`|`command_queue_worker` restart interval

#### `migrate`
```bash
$ python manage.py migrate
```

#### Models/tables
model|db_table|fields/columns
-|-|-
`Queue`|`django_command_queue`|`id`,`name`
### Features
+   customizable with `command_queue_sleep.py`

### Examples
queue worker/Docker `entrypoint`
```bash
python manage.py command_queue_worker
```

`command_queue_sleep.py` - worker sleep customization
```
import time
from django.core.management.base import BaseCommand
from django_command_queue.models import Queue

class Command(BaseCommand):
    def handle(self,*args,**options):
        time.sleep(0.42)
        if todo:
            Queue(name='command_name1').save()
            Queue(name='command_name2').save()
```

queue processing without worker/endless loop
```bash
python manage.py command_queue
```

