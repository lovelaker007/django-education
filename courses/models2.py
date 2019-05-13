from django.db import models


class BaseContent1(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# Text1继承自一个抽象基类，在数据库中并不会创建BaseCentent1表
# 会创建Text1表，表中存在title，created，body三个字段
class Text1(BaseContent1):
    body = models.TextField()


class BaseContent2(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


# 数据库会创建BaseContent2和Text2两张表
# Text2中只有body字段和到BaseContent2的一对一的外键字段
class Text2(BaseContent2):
    body = models.TextField()


from django.utils import timezone
class BaseContent3(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


# 代理模型
# 两个模型共同操作数据库中的同一张表，但是代理模型定义的方法，不能通过被代理模型访问
class OrderedContent(BaseContent):
    class Meta:
        proxy = True
        ordering = ['created']

    def created_delta(self):
        return timezone.now() - self.created
