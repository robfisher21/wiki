from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from markdown2 import Markdown
from random import randrange


# Index view: returning a directory of wiki entrries.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Entry page: returning wiki title and content.
def title (request, title):
    markdowner = Markdown()
    if  util.get_entry(title) is None:
       return render(request, "encyclopedia/error.html", {
        })
    else:
        content = util.get_entry(title)
        contentmd = markdowner.convert(content)
        return render(request, "encyclopedia/title.html", {
        "contentmd": contentmd,
        "content": content,
        "title" : title  
       })
# Search: returning wiki entries matching search terms 
def search (request):
    query = request.GET.get('q',"")
    entries = (util.list_entries())
    results = []
    if  util.get_entry(query) is not None:
       return HttpResponseRedirect (reverse ('title', args=[query]))
  
    else:
        for entry in entries:
            lowe = entry.lower()
            lowq = query.lower()
            if lowe.find(lowq) !=-1:
                results.append(entry)
        return render (request, "encyclopedia/search.html", {
            "query" : query,
            "results": results
    })                 

# Add: Enabling new wiki entries to be created

##Class: defines the Form template describing the wiki entry.
class NewEntryForm (forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':5}), label="Body")

##Add: Saves the form entry  
def add(request):
    if request.method =="POST" :
        form = NewEntryForm(request.POST)
        markdowner = Markdown()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request,"add.html", {
            "add": "true",
            "title": title    
            })
                
        else:
            return render(request,"add.html", {
                "form":form          
            })

    return render(request, "add.html", {
            "form": NewEntryForm()
        })

#Edit: enables existing wiki entries to be updated.
def edit(request):
    title= request.POST.get("title")
    if request.method =="POST" and request.POST.get("edit") is None:
        form = NewEntryForm(request.POST)
        

        return render(request,"edit.html", {
                "form":form,
                "title":title         
            })

    elif request.method =="POST" and request.POST.get("edit") =="true":
            form = NewEntryForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
            return HttpResponseRedirect (reverse ('title', args=[title])) 
            
    return render(request, "edit.html", {
            "form": NewEntryForm()
        })

#Random - Returns a wiki entry at random.
def random (request):
    entries = util.list_entries()
    count = len(entries)
    random = randrange(0,count)
    title = entries[random]

    return HttpResponseRedirect (reverse ('title', args=[title])) 
       
 