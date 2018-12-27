import os
import json
from rest_framework import serializers

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

json_data = open(os.path.join(BASE_DIR, 'static/json/currency_code.json'))   
data = json.load(json_data)
CURRENCY_CHOICES = sorted([item['AlphabeticCode'] for item in data])

class CurrencySerializer(serializers.Serializer):
    currency_code = serializers.ChoiceField(choices=CURRENCY_CHOICES)
    currency_value = serializers.DecimalField(max_digits=20, decimal_places=5)
    target_code = serializers.ChoiceField(choices=CURRENCY_CHOICES)