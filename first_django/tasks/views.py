from django.shortcuts import render

tasks = ["task1", "task2", "task3"]

# Create your views here.
def index(request):
    return render(request, "tasks/index.html", {
        "tasks": tasks
    })