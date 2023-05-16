from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
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