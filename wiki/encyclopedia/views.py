from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from markdown2 import markdown
import random

class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            all_entries = util.list_entries()
            if search in all_entries:
                return redirect("wiki:entry", search)
            else:
                #Find all entries that are related
                related_entries = []
                for entry in all_entries:
                    if search in entry:
                        related_entries += [entry]
                #Fix-me: redirect to a search results page instead
                return render(request, "encyclopedia/search.html", {
                    "title": search,
                    "entries": related_entries,
                    "form": SearchForm(),
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
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

def rand(request):
    all_entries = util.list_entries()
    rand_id = random.randint(0, len(all_entries) - 1)
    return redirect("wiki:entry", all_entries[rand_id])

def new(request):
    return render(request, "encyclopedia/new.html", {
            "form": SearchForm(),
        })