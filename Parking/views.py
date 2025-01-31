from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PerkingSerializer
from .models import ParkingModels
from profiles.permission import IsOwner
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from category.models import CategoryModel
import uuid
from sslcommerz_lib import SSLCOMMERZ
import uuid
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import os
import environ




env=environ.Env()
environ.Env.read_env()
B_URL= "https://backend-parking-p4dd.onrender.com/parking/"
F_URL="http://localhost:5173/"
S_ID=env('STORE_ID')
S_PASS=env('STORE_PASS')




def generate_id():
    return str(uuid.uuid4())




class CreateParkings(APIView):
    permission_classes=[IsAuthenticated]
    # serializer_class=PerkingSerializer

    def post(self, request):
        serializer = PerkingSerializer(data=request.data)        
        if serializer.is_valid():
                       
            name = serializer.validated_data['car_name']
            categ = serializer.validated_data['category']
            if categ:              
                    isctg=CategoryModel.objects.get(id=categ.id)
                                      
                             
                    parking=ParkingModels.objects.create(

                    user=request.user.userprofile,
                    ticket=generate_id(),
                    car_name=name,
                    category=categ,
                    start_park=now()  
                    )
                    isctg.available_slots-=1
                    isctg.save()
                    res = PerkingSerializer(parking)
                    return Response(
                        {
                        "message": "Parking created successfully!",
                        "data": res.data,
                        'status':201,
                        }
                    )
            return Response(serializer.errors)


class CheakTotal(APIView):
     permission_classes=[IsAuthenticated]

     def put(self,request,id):
          
          isparking=ParkingModels.objects.get(id=id)
          

          if isparking:      
                      
               ticket=request.data.get('ticket')
            #    print(ticket)
            #    print(isparking.ticket)

               if isparking.ticket!=ticket:
                    return Response({
                    'message':"Wrong Ticket Please Cheak"
                                })
               
               start_park=isparking.start_park
               timeNow=now() 
            
               total_time=timeNow-start_park
                
               
               total__hours = total_time.total_seconds() / 3600
               round(total__hours)

               catewise=CategoryModel.objects.get(id=isparking.category.id)
               priceper_h=catewise.price_p_h

               if total__hours <=1:
                    total__hours=1


               total_price=total__hours*priceper_h
               
               return Response({
                    'total_price':round(total_price),
                    'trans_ticket':generate_id(),
                    'parking_id':isparking.id,
                    'message':"Your Total Bill"
               }) 

                    
          else:
               return Response({
                    'message':"ID Wrong Please Cheak"
               })          
               
               
                
class BackCar(APIView):
      permission_classes=[IsAuthenticated]

      def put(self,request,id):
          
          trans_id=request.data.get('trans_ticket')
          t_price=request.data.get('total_price')
          if not trans_id or not t_price:
            return Response({
                "message": "transaction ticket and total price are required."
            })
          
          isparking=ParkingModels.objects.get(id=id)
        
          if isparking:
               catewise=CategoryModel.objects.get(id=isparking.category.id)
               catewise.available_slots+=1            
               isparking.is_complete=True
               isparking.total_price=t_price
               isparking.end_park=now()
               catewise.save()
               isparking.save()
               return Response({
                        'messages':"Thanks For Parking",
                        'status':"Sucess"
                    })



class AllParkings(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        data = ParkingModels.objects.all().order_by('-start_park')
        
        if self.request.user.userprofile.account_type =='User':
             res= data.filter(user=self.request.user.userprofile)
             serializer=PerkingSerializer(res,many=True)
             for item in serializer.data:
                item.pop("ticket", None)
             
            
         
             return Response(
                {
                    'data':serializer.data,
                    'messages':'Your All Parkings'
                }
             )
        else:
            serializer=PerkingSerializer(data,many=True)
           
            for item in serializer.data:
                item.pop("ticket", None)
          
        
            
            return Response(
                {
                    'data':serializer.data,
                    'messages':' All Parkings'
                }
                )
        


class PaymentView(APIView):

    def post(self,request):

        res=request.data
        trans_id=generate_id()
    

        settings = { 'store_id': S_ID, 'store_pass': S_PASS, 'issandbox': True }
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = res['totalammount']
        post_body['currency'] = "BDT"
        post_body['tran_id'] = trans_id
        post_body['success_url']=f"{B_URL}payment/success/{trans_id}/"
        post_body['fail_url'] =f"{B_URL}payment/failed/" 
        post_body['cancel_url'] =f"{B_URL}payment/failed/"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "test"
        post_body['cus_email'] = request.user.email
        post_body['cus_phone'] =request.user.userprofile.mobile_no,
        post_body['cus_add1'] = "Dhaka"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"


        response = sslcz.createSession(post_body) 
        
        return Response({
            "message":"payment sucess",
            "data":response,
            'transId':trans_id
                     }) 






@csrf_exempt
async def paymentSucess(request, trans_id: str):
    return redirect(f'{F_URL}payment/sucess/{trans_id}')
    


@csrf_exempt
async def paymentfailed(request):
    return redirect(f'{F_URL}payment/failed')
    


          
            
     

   


    

