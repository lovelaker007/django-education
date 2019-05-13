from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


# 和User，Subject都建立多对一的关系
class Course(models.Model):
    owner = models.ForeignKey(User, related_name='course_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


# 和Course建立多对一的关系
class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # 自定义的字段，实现了在相同的course下的序号
    # 作用的通俗解释：
        # course是课程，module是内容，一个course包括多个module
        # 在Module整张表的范围内，对每个module编号没有意义
        # 应该按照course分类，对属于同一course的module再编号，
        # 之后便可以方便的查询，一门course下，按序号排列的module
    order = OrderField(for_fields=['course'], blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


# ContentType
# django内部维护了一张cotenttype表，表中的记录就是整个项目，各个app下定义的数据模型(model)
# 通过contenttype表，可以方便的查看到整个项目下，定义的所有模型(model)
# 下表的content_type字段，就是指向contenttype表的外键，通过该外键可以确切找到一个模型了
# object_id字段是正数字段，表示主键值
# 通过确定的模型和主键值，可以确定模型中的一条记录，这条记录就被下表的item字段关联
# 总之，通过在表中的content_type, onject_id, item三个字段，实现了向任意模型的任意一条数据关联的功能
class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                 limit_choices_to={'model__in': ('text', 'file', 'image', 'video')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


# 类似与接口的方式，实现模型继承
class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # 指定abstract说明该类类似于接口
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()
