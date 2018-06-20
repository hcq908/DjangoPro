from django.shortcuts import render
# 注意引用同一个文件内的文件，前面要加.号
from .models import Topic, Entry
# Create your views here.
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
# import pdb

def index(request):
    "学习笔记的主页"
    return render(request, 'learningApp/index.html')

@login_required #需要先登录
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('data_added')
    # pdb.set_trace()
    # topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'learningApp/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic, and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-data_added')  #注意排序的条目是在models.py中建立的
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learningApp/topic.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        #POST提交数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learningApp:topics')) #reverse 返回url
    context = {'form':form}
    return render(request, 'learningApp/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learningApp:topic',args=[topic_id]))
    context = {'topic':topic, 'form':form}
    return render(request,'learningApp/new_entry.html',context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry) #instance关键字如何用? 180529 ,
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learningApp:topic', args=[topic.id])) #注意reverse的用法,参数都在括号内
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request, 'learningApp/edit_entry.html',context)