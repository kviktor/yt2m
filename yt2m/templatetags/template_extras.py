from django import template

register = template.Library()


@register.filter
def readable_duration(value, verbose=False):
    retval = ""
    minutes, seconds = divmod(value, 60)
    if minutes:
        if verbose:
            retval += f" {minutes} minute{'s' if minutes > 1 else ''}"
        else:
            retval += f"{minutes}m"

    if seconds:
        if verbose:
            retval += f" {seconds} second{'s' if seconds > 1 else ''}"
        else:
            retval += f"{seconds}s"

    return retval.strip()
