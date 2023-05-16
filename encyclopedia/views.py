import random

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


# Form for search field in search bar
class SearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Search Encyclopedia", "class": "search"}))


# Form for new page entry
class NewEntryForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Title", "class": "row"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Markdown Content", "rows": "5", "class": "row"}))


# From for editing page entry
class EditEntryForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"rows": "5", "class": "row"}))


# List all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "search": SearchForm(auto_id=False),
        "entries": util.list_entries()
    })


# Show entry page if exists, else error page
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
    

# Show entry page if match, else show search results containing search
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
    
    # Show emtpy results
    return render(request, "encyclopedia/search.html", {
        "results": []
    })


# Create new page entry
def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title:str = form.cleaned_data["title"]
            content:str = form.cleaned_data["content"]
            entries = util.list_entries()

            # Show error alert if title already exists
            if title.lower() in [entry.lower() for entry in entries]:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": True
                })

            # Save and redirect to new entry page
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    # Show new page entry form
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm(auto_id=False)
    })


# Edit page entry
def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]

            # Save edited page entry and redirect to entry
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

    # Get content of page and show edit page form including existing content
    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditEntryForm(initial={"content": entry})
    })


# Random entry page
def random_page(request):
    return HttpResponseRedirect(reverse("entry", kwargs={"title": random.choice(util.list_entries())}))