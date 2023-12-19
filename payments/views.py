from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CardInformationSerializer
import stripe

class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response = {}

        if serializer.is_valid():
            data_dict = serializer.validated_data
            stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
            response = self.stripe_card_payment(data_dict=data_dict)
        else:
            response = {'errors': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST}

        return Response(response)





    def stripe_card_payment(self, data_dict):
        print(data_dict, "___________data_dict____________")
        try:
            card_details = {
                "type": "card",
                "card": {
                    "number": data_dict['card_number'],  # Access values using keys, not values
                    "exp_month": data_dict['expiry_month'],  # Access values using keys, not values
                    "exp_year": data_dict['expiry_year'],  # Access values using keys, not values
                    "cvc": data_dict['cvc'],  # Access values using keys, not values
                },
            }
            # You can also get the amount from the database by creating a model
            payment_intent = stripe.PaymentIntent.create(
                amount=10000,
                currency='inr',
            )
            payment_intent_modified = stripe.PaymentIntent.modify(
                payment_intent['id'],
                payment_method=card_details['card']['number'],
            )

            try:
                payment_confirm = stripe.PaymentIntent.confirm(
                    payment_intent['id']
                )
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
            except stripe.error.CardError as e:
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
                payment_confirm = {
                    "stripe_payment_error": "Failed",
                    "code": e.code,
                    "message": e.user_message,
                    'status': "Failed"
                }

            if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
        except stripe.error.CardError as e:
            response = {
                'error': e.user_message,
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }

        return response
