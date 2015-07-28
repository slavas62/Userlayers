from transliterate import translit
from django.utils.text import slugify

def translit_and_slugify(name):
    return slugify(translit(name, 'ru', reversed=True))

def get_app_label_for_user(user):
    return 'ul_%s' % user.pk

def get_db_table_name(user, name):
    return '%s_%s' % (get_app_label_for_user(user), translit_and_slugify(name))
