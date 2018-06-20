from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    text = models.CharField(max_length=200)
    data_added = models.DateTimeField(auto_now_add=True) #自动设置为当前时间
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self): #默认使用此属性显示Topic类的信息
        return self.text

class Entry(models.Model):
    #主题的具体知识
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,)
    text = models.CharField(max_length=2000)
    data_added = models.DateTimeField(auto_now_add=True)

    class Meta:#设置Meta属性
        verbose_name_plural = 'entries' #人类可读的复数名称, verbose 冗长的 plural 复数

    def __str__(self):
        "返回字符串表示"
        return self.text[0:50]+'...'
