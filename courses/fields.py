from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# 模型中的序号字段
# 常用的id字段，就是在整个模型的范围内，对数据行统一编号
# 但如果要实现对模型的数据行，先按照某字段分类(例如课程内容字段按课程分类)，
# 再在分类的基础上编号
class OrderField(models.PositiveIntegerField):

    # for_fields字段指定分类的基准字段 
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # 如果本条数据行没有编号
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # 下面一行关键代码
                    # 找出和本条数据行用于分类的字段的取值相同的数据行，通俗说就是和本数据行同类的数据行
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # 取最后一个数据对象的序号
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)
