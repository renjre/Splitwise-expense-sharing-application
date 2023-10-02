from rest_framework import status
from rest_framework.response import Response
from .models import User
from rest_framework import viewsets
from .serializers import *
from rest_framework.views import APIView
from django.db.models import Sum


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ExpenseList(APIView):
    def get(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetailView(APIView):
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def put(self, request, pk):
        expense = self.get_object(pk)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = self.get_object(pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
############################################################################################################

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserRoomViewSet(viewsets.ModelViewSet):
    queryset = UserRoom.objects.all()
    serializer_class = UserRoomSerializer



############################################################################################################


class ExpenseSplitList(APIView):
    def get(self, request):
        expense_splits = ExpenseSplit.objects.all()
        serializer = ExpenseSplitSerializer(expense_splits, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSplitSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            exist_ExpenseSplit = ExpenseSplit.objects.filter(expense=data['expense'], user=data['user'])
            if not exist_ExpenseSplit:
                if data['expense'].expense_type == "PERCENT":
                    total = data['expense'].amount
                    if total > 0:
                        ExpenseSplit.objects.create(
                            expense = data['expense'],
                            user = data['user'],
                            amount = (total/100)*data['amount']
                        )
                else:
                    serializer.save()
            else:
                expense_split = exist_ExpenseSplit.first()
                if data['expense'].expense_type == "PERCENT":
                    total = data['expense'].amount
                    if total > 0:
                        expense_split.amount = (total/100)*data['amount']
                        expense_split.save()
                else:
                    expense_split.amount = data['amount']
                    expense_split.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################################################################################################

def fu(x, zx):
    if x.amount < zx.amount:
        if Owes.objects.filter(id=zx.id) and Owes.objects.filter(id=x.id):
            zx.amount = zx.amount - x.amount
            zx.save()
            x.delete()
    elif x.amount > zx.amount:
        if Owes.objects.filter(id=zx.id) and Owes.objects.filter(id=x.id):
            x.amount = x.amount - zx.amount
            x.save()
            zx.delete()
    
class AllUsersOwesView(APIView):
    def get(self, request):
        owes = Owes.objects.all()
        ls = []
        if owes:
            for x in owes:
                sd = list(map(lambda zx: fu(x, zx) if zx.user == x.owes_to and x.user == zx.owes_to else "no", owes))
        else:
            pass
        
        qs =  Owes.objects.all()
        rel = []
        if qs:
            for x in qs:
               rel.append(x.__str__()) 
        return Response({"result": rel})
    