from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal

from .models import Customer, Transaction
from .serializers import CustomerSerializer
from .twilio_utils import send_sms_to_number
from .pdf_utils import generate_customer_statement

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .auth_utils import get_or_create_user_from_token

@api_view(["POST"])
def google_auth(request):
    token = request.data.get("token")
    user = get_or_create_user_from_token(token)

    if not user:
        return Response({"error": "Invalid token"}, status=400)

    return Response({"token": token})

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()   # 👈 ADD THIS LINE
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_serializer_context(self):
        return {"request": self.request}

@api_view(['POST'])
def record_transaction(request):
    try:
        customer_id = request.data.get("customer_id")
        txn_type = request.data.get("transaction_type")
        amount = Decimal(request.data.get("amount"))

        customer = Customer.objects.get(id=customer_id, user=request.user)

        last_txn = Transaction.objects.filter(customer=customer).order_by('-created_at').first()
        last_balance = last_txn.balance_after if last_txn else Decimal("0.00")

        if txn_type == "credit":
            new_balance = last_balance + amount
        elif txn_type == "debit":
            new_balance = last_balance - amount
        else:
            return Response({"error": "Invalid transaction type"}, status=400)

        Transaction.objects.create(
            customer=customer,
            amount=amount,
            transaction_type=txn_type,
            balance_after=new_balance,
            proof_image=request.FILES.get("proof_image")
            
        )
        pdf_url = generate_customer_statement(customer)
        absolute_pdf_url = request.build_absolute_uri(pdf_url)


        admin_name = request.user.first_name or request.user.username

        message = (
    f"Hi {customer.name},\n"
    f"{'₹' + str(amount) + ' added to your Khata.' if txn_type == 'credit' else 'Payment received: ₹' + str(amount)}\n\n"
    f"Current balance: ₹{new_balance}\n\n"
    f"Shared by: {admin_name}\n"
    f"Statement:\n{absolute_pdf_url}"
        )



        send_sms_to_number(customer.phone, message)

        return Response({
            "success": True,
            "balance": new_balance,
        })

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)
@api_view(['GET'])
def customer_statement(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id, user=request.user)

        transactions = customer.transactions.order_by('created_at')

        return Response({
            "customer": customer.name,
            "phone": customer.phone,
            "transactions": [
                {
                    "date": t.created_at,
                    "type": t.transaction_type,
                    "amount": t.amount,
                    "balance": t.balance_after,
                    "proof_image": t.proof_image.url if t.proof_image else None
                }
                for t in transactions
            ]
        })

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)
@api_view(['GET', 'POST'])
def send_reminder(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id, user=request.user)

        last_txn = Transaction.objects.filter(
            customer=customer
        ).order_by('-created_at').first()

        if not last_txn or last_txn.balance_after <= 0:
            return Response(
                {"error": "No pending balance to remind"},
                status=400
            )

        balance = last_txn.balance_after

        message = (
            f"Hi {customer.name},\n"
            f"Pending amount: ₹{balance}\n\n"
            f"Please clear your due.\n"
            f"- Your App"
        )

        ok, info = send_sms_to_number(customer.phone, message)

        return Response({
            "success": ok,
            "message": "Reminder sent",
            "sms_info": info
        })

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)
