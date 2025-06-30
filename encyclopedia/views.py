from django.shortcuts import redirect, render

from . import util

def index(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()

    if query:
        for entry in entries:
            if entry.lower() == query.lower():
                return redirect("entry_page", title=entry)
            
        entries = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "query": query
    })

def entry_page(request, title):
    entry = util.get_entry(title)

    if entry is None:
        return render(request, "encyclopedia/404.html", status=404)
    
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        entry = util.get_entry(title)

        if entry is None:
            util.save_entry(title=title, content=content)
            return redirect('index')
        else:
            return render(request, "encyclopedia/new.html", {
                "message": "Encyclopedia entry already exists"
            })

    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title=title, content=content)
        return redirect('entry_page', title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": entry
    })
