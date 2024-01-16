from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListAPIView,
)
from user.models import Student, Attendance
from .serializers import (
    StudentSerializer,
    AttendanceSerializer,
    AttendanceReportSerializer,
    MarkAttendanceSerializer,
)
from rest_framework.response import Response
from django.db.models import F, Count
from .filters import DateRangeFilterBackend
from datetime import datetime


class StudentListCreateView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    allowed_methods = ["GET", "PATCH", "DELETE"]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "student deleted Successfully"})


class AttendanceListView(ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends=(DateRangeFilterBackend,)

    def get_queryset(self):
        attendance = Attendance.objects.filter(student__id=self.kwargs.get("student_id"))
        return attendance


class AttendanceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    allowed_methods = ["GET", "PATCH", "DELETE"]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "attendance deleted Successfully"})


class MarkAttendanceView(CreateAPIView):
    serializer_class = MarkAttendanceSerializer

    def perform_create(self, serializer):
        print("Request Data:", self.request.data)
        student_id = self.kwargs.get("student_id")
        date = self.request.data.get("date")
        status = self.request.data.get("status")
        leave_type = self.request.data.get("leave_type", None)
        data = {
            "student_id": student_id,
            "date": date,
            "status": status,
            "leave_type": leave_type,
        }

        serializer.is_valid(raise_exception=True)

        attendance_object, created = Attendance.objects.update_or_create(
            student_id=student_id,
            date=date,
            defaults={"status": status, "leave_type": leave_type},
        )
        if not created:
            return Response({"message": "Attendance updated successfully"})

        serializer.instance = attendance_object
        return Response({"message": "Attendance marked successfully"})


class AttendanceReportView(ListAPIView):
    serializer_class = AttendanceReportSerializer
    filter_backends=(DateRangeFilterBackend,)

    def get_queryset(self):
        from_date_str = self.request.query_params.get("from_date", None)
        to_date_str = self.request.query_params.get("to_date", None)

        try:
            from_date = datetime.strptime(from_date_str, "%Y/%m/%d") if from_date_str else None
            to_date = datetime.strptime(to_date_str, "%Y/%m/%d") if to_date_str else None
        except ValueError:
            return Attendance.objects.none()
        queryset = Attendance.objects.values("student__id", "student__name").annotate(
            total_leaves=Count("id", filter=F("status") == "leave"),
            total_present=Count("id", filter=F("status") == "present"),
        )
        if from_date and to_date:
            queryset = queryset.filter(date__range=(from_date, to_date))

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
