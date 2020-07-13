from time import sleep

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from redis import Redis
from rq import Queue

from .forms import InputForm
from .models import Result

redis_instance = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
default_queue = Queue(connection=redis_instance)
fast_queue = Queue('fast', connection=redis_instance)


# Create your views here.
def tetration(request):

    if request.method == 'POST':
        filled_form = InputForm(request.POST)
        if filled_form.is_valid():
            input_val = filled_form.cleaned_data['incoming_val']
            if already_processing(f'process_{input_val}'):
                # Currently being processed return result from database
                job = default_queue.enqueue(retrieve_result, input_val)
            else:
                # Add new value to database
                job = default_queue.enqueue(process_request, input_val, job_id=f'process_{input_val}')
        else:
            try:
                # Try returning existing result from database if pk exists
                job = fast_queue.enqueue(retrieve_result, request.POST["incoming_val"])
            except ObjectDoesNotExist:
                pass  # error handled in below try block

        try:
            while job.get_status() in ['queued', 'started']:
                sleep(0.1)
            calculated_val, note = job.result
            error = ''
        except TypeError:
            calculated_val = 'n/a'
            note = ''
            error = f'An Error has occurred unable to process given input or find in database (input received: {request.POST["incoming_val"]})'

        new_form = InputForm()
        return render(request, 'tetration/home.html', {
            'input_form': new_form,
            'input_value': request.POST["incoming_val"],
            'calculated_val': calculated_val,
            'note': note,
            'error': error
        })
    else:
        new_form = InputForm()
        return render(request, 'tetration/home.html', {'input_form': new_form})


def second_tetration(input_value):
    # Return calculation
    return input_value ** input_value


def process_request(input_value):
    # Process new request and insert into database
    cal_val = second_tetration(input_value)
    Result(incoming_val=input_value, calculated_val=str(cal_val)).save()
    return cal_val, 'Database has been updated with new value'


def retrieve_result(input_value):
    # Retrieve results from the database using primary key
    cal_val = Result.objects.get(pk=input_value).calculated_val
    return cal_val, 'Value retrieved from database'


def already_processing(job_id):
    # Check if current value is being/been processed or queued to be
    return job_id in [
        *default_queue.scheduled_job_registry.get_job_ids(),
        *default_queue.started_job_registry.get_job_ids(),
        *default_queue.finished_job_registry.get_job_ids()
    ]


