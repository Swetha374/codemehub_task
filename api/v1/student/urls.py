from django.urls import path
from api.v1.student.views import (
  StudentListCreateView,
  StudentDetailView,
  AttendanceListView,
  AttendanceDetailView,
  MarkAttendanceView,
  AttendanceReportView
)


urlpatterns = [
    path("list-create/", StudentListCreateView.as_view()),
    path("<int:pk>/", StudentDetailView.as_view()),
    path("<int:student_id>//attendances/", AttendanceListView.as_view()),
    path("attendance/<int:pk>", AttendanceDetailView.as_view()),
    path("<int:student_id>/mark-attendance/", MarkAttendanceView.as_view()),
    path("attendance-report/", AttendanceReportView.as_view()),





   
]
