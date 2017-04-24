from django.utils import translation


def change_language(request, lang):
    translation.activate(lang)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang
    request.session.modified = True
