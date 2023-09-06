from django.shortcuts import render
from .models import TodoModel
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import date, timedelta
import datetime
from django.db.models import Q
from .forms import TodoModelForm
from django.views.generic import FormView, CreateView, UpdateView, DeleteView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your views here.


def index(request):
    # x=TodoModel.objects.all().first()
    # print(x.date)

    # current_datetime_utc = datetime.datetime.now()
    # print(current_datetime_utc)

    return render(request, 'index.html')


def TodoList(request):
    selected_filter = request.GET.get("filter", "all")
    items_per_page = int(request.GET.get('page_size', 4))
    page_number = int(request.GET.get('page', 1))
    searching = request.GET.get('search', '')

    if searching:
        todo_list = TodoModel.objects.filter(
            Q(name__icontains=searching) | Q(description__icontains=searching))
    else:
        todo_list = TodoModel.objects.all().order_by('name')

    # filter
    if selected_filter == "today":
        todo_list = todo_list.filter(date__date=date.today())
    elif selected_filter == "this_week":
        # today = date.today()
        # start = today - timedelta(days=today.weekday())
        # end = start_of_week + timedelta(days=6)
        current_date = datetime.datetime.now()
        current_week_number = int(current_date.strftime("%U"))
        todo_list = todo_list.filter(date__week=current_week_number)

    elif selected_filter == "this_month":
        todo_list = todo_list.filter(date__month=date.today().month)

    # pagination
    paginator = Paginator(todo_list, items_per_page)
    page = paginator.get_page(page_number)
    total_items = paginator.count

    if page_number:
        starting_item_number = min(
            (page.number - 1) * items_per_page + 1, total_items)
        ending_item_number = min(
            starting_item_number + items_per_page - 1, total_items)
    else:
        starting_item_number = 1
        ending_item_number = items_per_page
    # print(page)

    data = {
        'todo': [{'id': item.id,
                  'title': item.name,
                  'date': item.date.strftime("%d/%m/%Y %I:%M%p"),
                  'repeat': item.repeat,
                  'description': item.description} for item in page],  # Customize this according to your TodoModel
        'count': total_items,
        'showing_start': starting_item_number,
        'showing_end': ending_item_number,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'previous_page_number': page.previous_page_number() if page.has_previous() else None,
        'next_page_number': page.next_page_number() if page.has_next() else None,
    }
    # print(data['todo'])
    return JsonResponse(data)


def search_autocompletion(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        tasks_qs = TodoModel.objects.filter(Q(name__icontains=search))
        titles = [task.name for task in tasks_qs]
        print(titles)
        return JsonResponse(titles, safe=False)


class TaskCreateView(CreateView):
    model = TodoModel
    template_name = "createTask.html"
    form_class = TodoModelForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        # Get the cleaned date from the form
        date = form.cleaned_data['date']
        print(date.year, date.month, date.day)
        print(date)

        # # Get the current UTC time
        current_datetime_utc = timezone.now()
        print(current_datetime_utc)

        # # Convert the current UTC time to the desired time zone (e.g., "Asia/Kolkata")
        # current_datetime = current_datetime_utc.astimezone(timezone.get_current_timezone())

        # # Combine the date from the form with the current time
        # combined_datetime = timezone.datetime(
        #     date.year, date.month, date.day, current_datetime.hour, current_datetime.minute, current_datetime.second,
        #     tzinfo=timezone.get_current_timezone()
        # )

        # # Assign the combined datetime to the date field in the form
        # form.cleaned_data['date'] = combined_datetime

        # Save the associated model with the updated date
        self.object = form.save()

        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = TodoModel
    form_class = TodoModelForm
    template_name = "createTask.html"
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context


def deleteTask(request, pk):
    task = TodoModel.objects.get(id=pk)
    task.delete()
    return JsonResponse("Deleted successfully", safe=False)




@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        recipient = request.POST.get('email', None)

        if recipient:
            try:
                validate_email(recipient)
                TaskList = TodoModel.objects.filter(
                    Q(date__date=date.today()) | Q(repeat='daily'))
                if TaskList:
                    tasks_to_send = "\n".join([task.name for task in TaskList])

                    subject = "Due Tasks"
                    message = f'Tasks for today:\n{tasks_to_send}'
                    to_mail = settings.EMAIL_HOST_USER
                    recipient_address = [recipient]
                    try:
                        # Send the email
                        send_mail(subject, message, to_mail, recipient_address)
                        print("Email sent successfully")
                        return JsonResponse({'status': 'success', 'message': f'Email sent to {recipient}'})
                    except Exception as e:
                        print(e)
                return JsonResponse("No due tasks were found for today", safe=False)
            except ValidationError as e:
                print(e)
                return JsonResponse({'status': 'error', 'message': "Invalid email address!"})
        else:
            return JsonResponse({'status': 'error', 'message': 'Recipient Email not provided'})

