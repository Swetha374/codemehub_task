from rest_framework import serializers
from user.models import Student, Attendance


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "name", "roll_number")


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("id", "student", "date", "status", "leave_type")


class MarkAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ("id", "date", "status", "leave_type")

    def validate(self, data):
        status = data.get("status")
        leave_type = data.get("leave_type")
        print(status)

        if status == "leave" and leave_type is None:
            raise serializers.ValidationError(
                "Leave type should not be specified when status is 'leave'"
            )

        return data


class AttendanceReportSerializer(serializers.Serializer):
    student__id = serializers.IntegerField()
    student__name = serializers.CharField()
    total_days = serializers.SerializerMethodField()
    total_leaves = serializers.IntegerField()
    total_present = serializers.IntegerField()
    attendance_percentage = serializers.SerializerMethodField()

    def get_total_days(self, obj):
        total_leaves = obj.get("total_leaves", 0)
        total_present = obj.get("total_present", 0)
        return total_leaves + total_present


    def get_attendance_percentage(self, obj):
        total_days =  self.get_total_days(obj)
        print(total_days)
        total_present = obj.get("total_present", 0)
        if total_days == 0:
            return 0
        total=(total_present / total_days) * 100
        return total