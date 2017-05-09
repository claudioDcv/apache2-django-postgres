from django.utils.text import slugify
from PIL import Image


def code_generate(text):
    return slugify(text).replace('-', '_')


def human_text_generate(text):
    return slugify(text).replace('_', ' ')


def ctm_msg(txt):
    return {
        'create:ok': "{} creado con exito",
        'update:ok': "{} actualizado con exito",
        'delete:ok': "{} eliminado con exito",
        'create:nok': "{} creado con exito",
        'update:nok': "{} actualizado sin exito",
        'delete:nok': "{} eliminado sin exito",
        'size:min': "{} minimo {} caracteres",
        'size:max': "{} maximo {} caracteres",
        }[txt]


def resize_image(image_file, f_width=500, f_height=500):
    try:
        image = Image.open(image_file)
        (width, height) = image.size

        _w = width
        _h = height

        if _w > _h:
            if _w > f_width:
                _h = (_h * f_height)/_w
                _w = f_width
            else:
                pass
        else:
            if _h > f_height:
                _w = (_w * f_width)/_h
                _h = f_height
            else:
                pass

        size = (int(_w), int(_h))
        image = image.resize(size, Image.ANTIALIAS)
        image.save(image_file.path)
    except Exception as e:
        return False
    return True
