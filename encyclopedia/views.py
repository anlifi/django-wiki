from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia"}))


class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Title", "class": "row"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Markdown Content", "rows": "5", "class": "row"}))


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
            
            return render(request, "encyclopedia/search.html", {
                "results": [s for s in entries if q.lower() in s.lower()]
            })
    
    return render(request, "encyclopedia/search.html", {
        "results": []
    })


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title:str = form.cleaned_data["title"]
            content:str = form.cleaned_data["content"]
            entries = util.list_entries()
            if title.lower() in [entry.lower() for entry in entries]:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": True
                })

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })