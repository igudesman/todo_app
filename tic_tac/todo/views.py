from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from django.views.decorators.http import require_POST
#v0.3.1 Beta

def index(request):
	todo_list = Todo.objects.order_by('id')
	form = TodoForm()
	percent = progressBar()

	context = {'todo_list': todo_list,
				'form': form,
				'percent': percent}

	return render(request, 'index.html', context)

@require_POST
def addTodo(request):
	form = TodoForm(request.POST)

	if form.is_valid():
		new_todo = Todo(text=request.POST['text'])
		new_todo.save()

	return redirect('index')

def completeTodo(request, todo_id):
	todo = Todo.objects.get(pk=todo_id)
	todo.complete = True
	todo.save()

	return redirect('index')

def deleteCompleted(request):
	Todo.objects.filter(complete__exact=True).delete()

	return redirect('index')

def deleteAll(request):
	Todo.objects.all().delete()

	return redirect('index')

def progressBar():
	completed_tasks= (Todo.objects.filter(complete__exact=True)).count()
	all_tasks = (Todo.objects.all()).count()
	if all_tasks != 0:
		return (completed_tasks/all_tasks)*100
	return 0

