import stripe
from .base_agent import BaseAgent
from app.models import Transaction
from decimal import Decimal

class PaymentProcessorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="payment_processor_v3",
            capabilities=["transactions", "payouts", "reconciliation"]
        )
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        self.fee_distribution = {
            'owner': Decimal('0.6'),
            'ai_fund': Decimal('0.2'),
            'reserve': Decimal('0.2')
        }
    
    def process_payment(self, amount, client_id, service_type):
        """Handle complete payment flow"""
        try:
            # Create Stripe charge
            charge = stripe.Charge.create(
                amount=int(amount * 100),  # Convert to cents
                currency='zar',
                source='tok_visa',  # In production: use actual token
                description=f"{service_type} for {client_id}"
            )
            
            # Record transaction
            transaction = Transaction(
                client_id=client_id,
                stripe_id=charge.id,
                amount=amount,
                service_type=service_type,
                status='completed'
            )
            db.session.add(transaction)
            
            # Distribute funds
            self._distribute_funds(amount, transaction.id)
            
            return {"status": "success", "transaction_id": transaction.id}
            
        except stripe.error.StripeError as e:
            self.log_error(f"Payment failed: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _distribute_funds(self, amount, transaction_id):
        """Split payment according to business rules"""
        amount = Decimal(str(amount))
        
        distributions = [
            ('owner', amount * self.fee_distribution['owner']),
            ('ai_fund', amount * self.fee_distribution['ai_fund']),
            ('reserve', amount * self.fee_distribution['reserve'])
        ]
        
        for account_type, amount in distributions:
            # In production: Actual bank transfers would happen here
            self.log_transaction(
                f"Distributed {amount} ZAR to {account_type} account",
                transaction_id
            )
