from rest_framework import serializers

class DashboardDataSerializer(serializers.Serializer):
    totalRevenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    totalExpenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    netIncome = serializers.DecimalField(max_digits=10, decimal_places=2)
    pendingPayments = serializers.DecimalField(max_digits=10, decimal_places=2)
    months = serializers.ListField(child=serializers.CharField())
    monthlyRevenue = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    monthlyExpenses = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    incomeCategories = serializers.ListField(child=serializers.CharField())
    incomeCategoryValues = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    expenseCategories = serializers.ListField(child=serializers.CharField())
    expenseCategoryValues = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
    cashFlow = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2))
