from rest_framework import serializers

from learners.models import Grade, LearnerRegister
from learners.models import Parent
from .models import ParentLearnerRelationship

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'address']

class ParentLearnerRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentLearnerRelationship
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'grade_name']

class LearnerRegisterSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)  # Nested serializer for grade details

    class Meta:
        model = LearnerRegister
        fields = ['id', 'name', 'grade']  # Include 'parent' if needed