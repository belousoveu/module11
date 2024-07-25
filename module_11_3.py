from PIL import Image
import pprint as pp


def introspection_info(obj):
    obj_description = {'Name:': obj.__class__.__name__, 'Type:': type(obj), 'attributes': dir(obj),
                       'Class:': obj.__class__.__name__, 'methods': dir(obj.__class__),
                       'module': obj.__class__.__module__, '__doc__': obj.__doc__ if obj.__doc__ else None}
    return obj_description


if __name__ == '__main__':
    im = Image.open('sample.jpg')
    pp.pprint(introspection_info(im))
    im.show()
