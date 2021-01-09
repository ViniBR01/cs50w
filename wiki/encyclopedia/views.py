from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from markdown2 import markdown
import random

class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            all_entries = util.list_entries()
            if search in all_entries:
                return redirect("wiki:entry", search)
            else:
                return redirect("wiki:search", search)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
    })

def search(request, search):
    all_entries = util.list_entries()
    if search in all_entries:
        return redirect("wiki:entry", search)
    related_entries = []
    for entry in all_entries:
        if search in entry:
            related_entries += [entry]
    return render(request, "encyclopedia/search.html", {
        "title": search,
        "entries": related_entries,
        "form": SearchForm(),
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry != None:
        html_entry = markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": html_entry,
            "form": SearchForm(),
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "title": title,
            "form": SearchForm(),
        })

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            #do something with input
    return render(request, "encyclopedia/new.html", {
            "new_entry": NewEntryForm(),
            "form": SearchForm(),
        })

def rand(request):
    all_entries = util.list_entries()
    rand_id = random.randint(0, len(all_entries) - 1)
    return redirect("wiki:entry", all_entries[rand_id])