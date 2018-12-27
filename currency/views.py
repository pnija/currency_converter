import requests
import collections
from rest_framework.views import APIView
from django.http import JsonResponse
from lxml import html
from currency.serializers import CurrencySerializer
from currency_converter.settings import EXCHANGE_RATE_URL

class CurrencyConvert(APIView):
    """
    API for converting currencies.
    """
    def get(self, request):
        currency_code = request.GET.get('currency_code')
        currency_value = request.GET.get('currency_value','0.0')
        target_code = request.GET.get('target_code')
        data = {'currency_code':currency_code,
                'currency_value':currency_value,
                'target_code':target_code}
        serializer = CurrencySerializer(data=data)
        if serializer.is_valid():
            present_rates = self.get_exchange_rates() # Retrieving latest exchange rates
            #-------------Converting currency based on exchange rates--------------------------#
            data['currency_value'] = float(data['currency_value'])
            data['default_target_code'] = 'USD' # Default target in case of invalid target code
            currency_value = None
            if present_rates.get(data['currency_code'] + '/' + data['target_code']):
                currency_value = present_rates[data['currency_code'] + '/' + data['target_code']] * data['currency_value']
            elif present_rates.get(data['target_code'] + '/' + data['currency_code']):
                currency_value = data['currency_value'] / present_rates[data['target_code'] + '/' + data['currency_code']] 
            else:
                if(present_rates.get(data['currency_code'] + '/USD')):
                    currency_value = present_rates[data['currency_code'] + '/USD'] * data['currency_value']
                elif(present_rates.get('USD/' + data['currency_code'])):
                    currency_value = data['currency_value'] / present_rates['USD/' + data['currency_code']]
                
                if not currency_value:
                    currency_value = 'Invalid currency code!'
                elif present_rates.get('USD/' + data['target_code']):
                    currency_value = currency_value * present_rates['USD/' + data['target_code']]
                elif present_rates.get(data['target_code'] + '/USD'):
                    currency_value = currency_value / present_rates[data['target_code'] + '/USD']
                else:
                    data[data['default_target_code']] = round(currency_value, 4)
            #--------------------------------------End----------------------------------------------#
            data = collections.OrderedDict(data)
            try:
                if not data.get(data['default_target_code']):
                    data[data['target_code']] = round(currency_value, 4)
            except TypeError:
                data[data['target_code']] = currency_value
            return JsonResponse(data, status=201)
        return JsonResponse(serializer.errors, status=400)

    def get_exchange_rates(self):
        '''
        Retrieving latest exchange rate for currency conversion
        '''
        url = EXCHANGE_RATE_URL
        response = requests.get(url)
        doc = html.fromstring(response.text)
        currency_list = doc.xpath('.//div[@id="cont1"]//tr//table/tr')
        present_rates = dict()
        for each_currency in currency_list:
            currency_pair = each_currency.find('./td[1]').text_content().strip()
            current_spot = float(each_currency.find('./td[2]').text_content().strip())
            present_rates.update({currency_pair:current_spot})
        return present_rates
