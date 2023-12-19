from rest_framework import serializers
from datetime import datetime  # Import datetime from datetime module

def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")

def check_expiry_year(value):
    today = datetime.now()  # Use datetime.now() instead of datetime.datetime.now()
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year.")

def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")

def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid payment_method.")

class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(
        max_length=150,
        required=True,
    )
    expiry_month = serializers.CharField(
        max_length=2,  # Assuming expiry month should be a 2-digit number
        required=True,
        validators=[check_expiry_month],
    )
    expiry_year = serializers.CharField(
        max_length=4,  # Assuming expiry year should be a 4-digit number
        required=True,
        validators=[check_expiry_year],
    )
    cvc = serializers.CharField(
        max_length=4,  # Adjust the max_length based on your requirements
        required=True,
        validators=[check_cvc],
    )
