from django.db.models import (
    CharField,
    PositiveIntegerField,
    TextField,
)
from django.db.models.base import (
    Model,
)


class TitleFieldMixin(Model):
    """
    Добавляет поле текстовое поле title обязательное для заполнения
    """

    title = TextField(verbose_name='расшифровка значения')

    class Meta:
        abstract = True


class IntegerValueMixin(Model):
    """
    Добавляет положительное целочисленное поле value обязательное для заполнения
    """

    value = PositiveIntegerField(verbose_name='значение ')

    class Meta:
        abstract = True


class CharValueMixin(Model):
    """
    Добавляет символьное поле value обязательное для заполнения
    """

    value = CharField(verbose_name='значение ', max_length=256)

    class Meta:
        abstract = True
