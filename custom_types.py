import click
import click_web


class DateParamType(click.ParamType):
    name = 'date'

    def convert(self, value, param, ctx):
        return value


class DateInput(click_web.resources.input_fields.BaseInput):
    param_type_cls = DateParamType

    @property
    def type_attrs(self):
        type_attrs = {}
        type_attrs['type'] = 'date'
        type_attrs['click_type'] = 'date'
        return type_attrs


click_web.resources.input_fields.INPUT_TYPES.append(DateInput)

DATE_TYPE = DateParamType()
