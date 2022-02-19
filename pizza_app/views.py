from django.http import JsonResponse
from django.shortcuts import render
from pizzapy import Customer, StoreLocator, Order, CreditCard
from rest_framework.views import APIView
from rest_framework.response import Response

from pizzapy.menu import Menu

# Create your views here.

# {
# "firstName": "Laith",
# "lastName": "Harb",
# "email": "harblaith7@gmail.com",
# "phone": "6133625418",
# "address": "6724 Yacht Blv",
# "city": "Cornwall",
# "region": "ON",
# "code": "K6H7N6",
# "items": [{"code": "12HTTSIXCH", "qty": 1}],
# "card_number": "4520880039060015",
# "card_expiry": "0624",
# "cvv": "374",
# "zip_code": "K6H7N6"
# }

# {
# "firstName": "Laith",
# "lastName": "Harb",
# "email": "harblaith7@gmail.com",
# "phone": "6133625418",
# "address": "6724 Yacht Blv",
# "city": "Cornwall",
# "region": "ON",
# "code": "K6H7N6",
# "items": [{"code": "12HTTSIXCH", "qty": 1}],
# }

class PizzaLocations(APIView):
    def post(self, request):
        body = request.data

        location = body["address"] + ", " + body["city"] + ", " + body["region"] + ", " + body["code"]
    
        customer = Customer("", "", "", "", location)
        my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)
        menu = my_local_dominos.get_menu()
        menu.search()
        return Response({
            'location': my_local_dominos.data
        })

class PizzaStoreMenu(APIView):
    def get(self, request, store_id):
        menu = Menu.from_store(store_id, country="ca")
        
        return Response({
            'menu': menu.variants.values()
        })


class PizzaPlaceOrder(APIView):
    def post(self, request):
        body = request.data

        location = body["address"] + ", " + body["city"] + ", " + body["region"] + ", " + body["code"]
    
        customer = Customer(body["firstName"], body["lastName"], body["email"], body["phone"], location)
        my_local_dominos = StoreLocator.find_closest_store_to_customer(customer)

        order = Order.begin_customer_order(customer, my_local_dominos, "ca")

        for item in body["items"]:
            print(item["code"], item["qty"])
            order.add_item(item["code"], item["qty"])

        try:
            card = CreditCard(body['card_number'], body['card_expiry'], body['cvv'], body['zip_code'])
        except Exception as e:
            print({'the nonio error': e})
            return 'no'

        order.place(card)
        my_local_dominos.place_order(order, card)

        return Response({
            'order': order.data
        })



# {
#   "order": {
#       "Address": {
#           "Street": "6724 Yacht Blv",
#           "City": "Cornwall",
#           "Region": "ON",
#           "PostalCode": "K6H7N6",
#           "Type": "House",
#           "StreetNumber": "6724",
#           "StreetName": "YACHT BLVD",
#           "CountyName": null,
#           "CountyNumber": null
#       },
#       "Coupons": [],
#       "CustomerID": "",
#       "Extension": "",
#       "OrderChannel": "OLO",
#       "OrderID": "LxbSZX7E4bWRgVWw8Gcs",
#       "NoCombine": true,
#       "OrderMethod": "Web",
#       "OrderTaker": null,
#       "Payments": [
#           {
#               "Type": "CreditCard",
#               "Expiration": "0624",
#               "Amount": 23.71,
#               "CardType": "VISA",
#               "Number": 4520880039060015,
#               "SecurityCode": 374,
#               "PostalCode": "K6H7N6"
#           }
#       ],
#       "Products": [
#           {
#               "ID": 1,
#               "Code": "12HTTSIXCH",
#               "Qty": 1,
#               "CategoryCode": "Pizza",
#               "SizeCode": "12",
#               "FlavorCode": "HANDTOSSTHIN",
#               "Price": 16.99,
#               "Amount": 16.99,
#               "Status": 0,
#               "LikeProductID": 0,
#               "Name": "12\" Hand Tossed Thin 6 Cheese Pizza",
#               "IsNew": false,
#               "NeedsCustomization": false,
#               "AutoRemove": false,
#               "Fulfilled": false,
#               "SideOptions": [],
#               "Tags": {
#                   "Servings": "8 slices",
#                   "ServingSize": "1/8 pizza",
#                   "DefaultSides": "",
#                   "DefaultToppings": "X=1,C=1,Cp=1,Fe=1,E=1,Pa=1"
#               },
#               "descriptions": [
#                   {
#                       "portionCode": "1/1",
#                       "value": "Pizza Sauce, Cheese, Provolone*, Feta*, Cheddar*, Parmesan Asiago*"
#                   }
#               ]
#           }
#       ],
#       "Market": "CANADA",
#       "Currency": "CAD",
#       "ServiceMethod": "Delivery",
#       "Tags": {},
#       "Version": "1.0",
#       "SourceOrganizationURI": "order.dominos.com",
#       "LanguageCode": "en",
#       "Partners": {},
#       "NewUser": true,
#       "metaData": {},
#       "Amounts": {
#           "Menu": 20.98,
#           "Discount": 0,
#           "Surcharge": 3.99,
#           "Adjustment": 0,
#           "Net": 20.98,
#           "Tax": 2.73,
#           "Tax1": 2.73,
#           "Tax2": 0,
#           "Bottle": 0,
#           "Customer": 23.71,
#           "Payment": 23.71
#       },
#       "BusinessDate": "2022-02-08",
#       "EstimatedWaitMinutes": "23-33",
#       "PriceOrderTime": "2022-02-08 20:46:01",
#       "AmountsBreakdown": {
#           "FoodAndBeverage": "16.99",
#           "Adjustment": "0.00",
#           "Surcharge": "0.00",
#           "DeliveryFee": "3.99",
#           "Tax": 2.73,
#           "Tax1": 2.73,
#           "Tax2": 0,
#           "Tax3": 0,
#           "Tax4": 0,
#           "Tax5": 0,
#           "Bottle": 0,
#           "Customer": 23.71,
#           "RoundingAdjustment": 0,
#           "Cash": 0,
#           "Savings": "0.00"
#       },
#       "StoreID": "10520",
#       "Email": "harblaith7@gmail.com",
#       "FirstName": "Laith",
#       "LastName": "Harb",
#       "Phone": "6133625418",
#       "IP": "69.159.77.96",
#       "Status": 1,
#       "StatusItems": [
#           {
#               "Code": "PriceInformationRemoved"
#           }
#       ],
#       "Promotions": {
#           "Redeemable": [],
#           "AvailablePromos": {
#               "EndOfOrder": null
#           }
#       },
#       "AvailablePromos": {
#           "EndOfOrder": null
#       },
#       "PriceOrderMs": 1331,
#       "PricingFlag": "0"
#   }
# }