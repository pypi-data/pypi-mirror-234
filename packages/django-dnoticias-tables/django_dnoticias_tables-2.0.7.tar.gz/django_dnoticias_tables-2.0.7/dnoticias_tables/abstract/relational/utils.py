from django.db.models import Manager

def get_model_attr(instance, field, default=[]):
    try:
        value = getattr(instance, field, None)
    except Exception as e:
        logger.exception(e)
        value = None
    is_manager = isinstance(value, Manager)
    if is_manager:
        value = value.all()
    return value