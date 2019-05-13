from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module


# 表单集，便于视图函数一次处理多个表单
# 此处通过inlineformset_factory工厂函数，创建特殊类型的表单集
# Course和Module是一对多的关系，工厂函数接收的参数中，第一个是“一”的那一方，
# 第二个参数是多的那一方
# 创建表单的时候，必须通过instance参数，传入一个course对向，实现一对多关系
# 并且实现了查找一条course下所有的module，并构建表单集的功能
ModuleFormSet = inlineformset_factory(Course, Module, fields=['title', 'description'], extra=2, can_delete=True)

# Django针对不同的formset提供了3种方法: formset_factory, modelformset_factory和inlineformset_factory


