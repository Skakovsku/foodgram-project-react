from rest_framework import exceptions


class NotFoundCastom(exceptions.NotFound):
    default_detail = "Страница не найдена."
