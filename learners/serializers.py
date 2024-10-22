from rest_framework import serializers
from .models import LearnerRegister, Grade

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'grade_name']

class LearnerProfileSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)
    grade_id = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all(), source='grade', write_only=True)

    class Meta:
        model = LearnerRegister
        fields = ['learner_id', 'name', 'grade', 'grade_id', 'date_of_birth', 'gender', 'name_of_parent', 'parent_contact']
        read_only_fields = ['learner_id']

