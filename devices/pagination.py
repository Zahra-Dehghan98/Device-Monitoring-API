from rest_framework.pagination import CursorPagination

class StandardCursorPagination(CursorPagination):
    ordering = "-created_at"

class TelemetryCursorPagination(CursorPagination):
    ordering = "-timestamp"