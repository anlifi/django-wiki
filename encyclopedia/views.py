from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TimeInput(attrs={'placeholder': 'Search Encyclopedia'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "search": SearchForm(),
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdowner.convert(entry)
        })
    

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            q:str = form.cleaned_data["q"]
            entries = util.list_entries()
            if q in entries:
                return HttpResponseRedirect(reverse("entry", kwargs={"title": q}))
            else:
                return render(request, "encyclopedia/search.html", {
                    "results": [s for s in entries if q.lower() in s.lower()]
                })
    
    return render(request, "encyclopedia/search.html", {
        "results": []
    })