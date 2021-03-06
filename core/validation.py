from django.utils.translation import gettext_lazy as _


class ErrorMessages:

    EMPTY_FIELD = _("Поле не {} не должно быть пустым.")
    PERMISSIONS_DENIED = _("Недостаточно прав.")


class Messages:

    PASSWORD_CHANGED = _("Пароль был успешно изменен.")
