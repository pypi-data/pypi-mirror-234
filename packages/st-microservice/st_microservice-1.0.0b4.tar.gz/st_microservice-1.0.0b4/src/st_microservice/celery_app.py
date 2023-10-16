import celery
from redis import from_url

from .general_utils import get_required_env


BROKER_URI = get_required_env('BROKER_URI')
redis = from_url(BROKER_URI, decode_responses=True)


def get_send_message_function(task_self: celery.Task):
    if task_self.request.called_directly:
        return print

    channel = f'task-messages-{task_self.request.id}'

    def send_message(message: str):
        redis.publish(channel, message)

    return send_message


app = celery.Celery('tasks', broker=BROKER_URI, backend=BROKER_URI)
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.event_serializer = 'pickle'
app.conf.accept_content = ['application/x-python-serialize']
app.conf.enable_utc = False
