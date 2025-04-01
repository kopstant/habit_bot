from rest_framework.pagination import PageNumberPagination


class CustomPaginator(
    PageNumberPagination
):  # Пользовательский класс для пагинации(DRF).
    page_size = (
        5  # Определяет количество отображаемых элементов на странице по умолчанию
    )
    page_size_query_param = (
        "page_size"  # Для изменения количества отображаемых элементов
    )
    max_page_size = 100  # Максимальное количество элементов. В случае если пользователь запросит большое количество
