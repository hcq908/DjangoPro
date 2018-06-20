from django import forms

from .models import Topic, Entry

#从model中的数据结构创建表单
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text'] #调用model中的哪些字段
        labels = {'text':''} #不要为text生成表单

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        widgets = {'text':forms.Textarea(attrs={'cols':80})} #设置输入区域宽度为80列


