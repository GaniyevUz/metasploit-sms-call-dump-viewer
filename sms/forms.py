from django.core.validators import FileExtensionValidator
from django.forms import Form, FileField

file_ext_validator = FileExtensionValidator(['txt'])


class FileForm(Form):
    file = FileField(validators=(file_ext_validator,))
