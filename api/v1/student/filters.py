from rest_framework.filters import BaseFilterBackend
from datetime import datetime
from coreapi import Field


class DateRangeFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            Field(
                name="from_date",
                location="query",
                required=False,
                type="string",
            ),
            Field(
                name="to_date",
                location="query",
                required=False,
                type="string",
            ),
        ]

    def filter_queryset(self, request, queryset, view):
        from_date_str = request.query_params.get("from_date", None)
        to_date_str = request.query_params.get("to_date", None)

        from_date = (
            datetime.strptime(from_date_str, "%Y/%m/%d") if from_date_str else None
        )
        to_date = datetime.strptime(to_date_str, "%Y/%m/%d") if to_date_str else None

        if from_date and to_date:
            queryset = queryset.filter(date__range=(from_date, to_date))

        return queryset
