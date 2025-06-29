from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/404.html", status=404)
    
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title
    })
