from django.shortcuts import render
from django import forms
from . import util
from markdown2 import markdown

class SearchForm(forms.Form):
    search = forms.CharField(label="Search")

def index(request):
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