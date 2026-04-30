'''
ayment Gateway - Low Level Design Problem

## Problem Statement

Design and implement a **Payment Gateway** system that processes payments from multiple payment methods (Credit Card, Debit Card, PayPal), handles transaction lifecycle (initiation, processing, success, failure), and manages payment history. The system should support payment processing, refunds, and transaction status tracking.

---

## Functional Requirements

### 1. Core Entities

- **Payment**: Represents a payment request/intent
  - Payment ID, Amount, Currency, Status, Payment Method, User ID, Timestamp
  - One Payment can have multiple Transactions (retry attempts)
  - Status reflects overall payment outcome (based on latest transaction
- **Payment Method**: Abstract base for different payment types
  - CreditCard, DebitCard, {PayPal}
- **Transaction**: Represents a single payment attempt/transaction record
  - Transaction ID, Payment ID (foreign key), Amount, Status, Gateway Response, Timestamp, Retry Attempt Number
  - Multiple Transactions per Payment (for retries)
  - Each transaction represents one attempt to process the payment
- **Refund**: Represents a refund transaction
  - Refund ID, Payment ID, Amount, Status, Reason, Timestamp

### 2. Core Operations

- **Process Payment**: Process a payment request
  - Validate payment details
  - Route to appropriate payment method handler
  - Create Payment record (status = PENDING)
  - Create initial Transaction record (attempt_number = 1)
  - Process transaction through payment gateway
  - If failed and retryable: Automatically retry (up to max attempts)
  - Create Transaction record for each retry attempt
  - Update Payment status based on transaction results
  - Return payment status (SUCCESS, FAILED, PENDING)
- **Refund Payment**: Process a refund for a successful payment
  - Validate refund eligibility
  - Process refund through original payment method
  - Create refund record
  - Update payment status
- **Get Payment Status**: Query payment status by payment ID
- **Get Transaction History**: Retrieve payment history for a user

### 3. Retry Logic
- **Automatic Retry**: Automatically retry failed payments
  - Maximum retry attempts: 3 (configurable)
  - Retry delay: Exponential backoff (1s, 2s, 4s) or fixed delay
  - Retry conditions: Only retry on transient failures (network errors, timeouts)
  - Don't retry on permanent failures (invalid card, insufficient funds)

- **Retry Strategy**:
  - Retry on: Network errors, timeouts, gateway unavailable
  - Don't retry on: Invalid credentials, expired card, insufficient funds, invalid payment details
  
- **Transaction Tracking**:
  - Each retry creates a new Transaction record
  - Transaction has attempt_number (1, 2, 3, ...)
  - Payment status updates based on latest transaction result
  - Payment status = SUCCESS if any transaction succeeds
  - Payment status = FAILED if all transactions fail

### 4. Payment Methods

- **Credit Card**: 
  - Card Number, CVV, Expiry Date, Cardholder Name
  - Validation: Check card number format, expiry date
- **Debit Card**:
  - Card Number, CVV, Expiry Date, Cardholder Name
  - Validation: Same as credit card
- **PayPal**:
  - PayPal Email (e.g., "user@paypal.com")
  - Validation: Check PayPal Email format and validate with PayPal API

### 5. Transaction Status

**Payment Status:**
- **PENDING**: Payment initiated but not yet processed
- **SUCCESS**: Payment processed successfully (at least one transaction succeeded)
- **FAILED**: Payment processing failed (all transactions failed)
- **REFUNDED**: Payment was refunded
- **CANCELLED**: Payment was cancelled

**Transaction Status:**
- **PENDING**: Transaction initiated
- **SUCCESS**: Transaction processed successfully
- **FAILED**: Transaction processing failed
- **RETRYABLE**: Transaction failed but is retryable (network error, timeout)
- **NON_RETRYABLE**: Transaction failed permanently (invalid card, insufficient funds)

### 5. Constraints & Rules

- **Payment Amount**: Must be positive (> 0)
- **Refund Amount**: Cannot exceed original payment amount
- **Refund Eligibility**: Can only refund successful payments
- **Idempotency**: Same payment request should not be processed twice
- **Validation**: Payment method details must be validated before processing
- **Retry Limits**: Maximum 3 retry attempts per payment
- **Retry Delay**: Exponential backoff (1s, 2s, 4s) between retries
- **Retry Conditions**: Only retry transient failures, not permanent failures


### Card Validation

Simple validation rules:
- Card number: 13-19 digits
- CVV: 3-4 digits
- Expiry date: Format MM/YY, not in past
- PayPal Email: Valid email format`

## Additional Edge Cases (Retry Logic)

10. **Retry Limit Reached**: All retry attempts exhausted
11. **Mixed Retry Results**: Some transactions retryable, some not
12. **Success After Retry**: Payment succeeds on retry attempt
13. **Retry Delay**: Proper delay between retry attempts
14. **Non-Retryable Failure**: Immediate failure without retry

**Retryable (should retry):**
- Network errors
- Timeout errors
- Gateway unavailable
- Temporary service unavailability

**Non-Retryable (don't retry):**
- Invalid card number
- Expired card
- Insufficient funds
- Invalid CVV
- Invalid payment details
- Authentication failures

'''
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import uuid
import re
import time
from threading import Lock
import random


class PaymentGateway:
    def __init__(self):
        self.payments = {}
        self.transactions = {}
        self.refund = {}
        self.payments_by_user = {}
        self.lock = Lock()

    def process_payment(self, amount, currency, payment_method, user_id, **kwargs):
        """
        Process payment request with automatic retry logic

        Args:
            amount: Payment amount
            currency: Currency code
            payment_method: "CREDIT_CARD" or "PAYPAL"
            user_id: User identifier
            **kwargs: Payment method specific details
                - For CREDIT_CARD: card_number, cvv, expiry_date, cardholder_name
                - For PayPal: email
        """
        with self.lock:
            # Step 1: Validate payment details
            if payment_method == "CREDIT_CARD":
                CreditCardPaymentMethod.validate(
                    kwargs["card_number"],
                    kwargs["cvv"],
                    kwargs["expiry_date"],
                    kwargs["cardholder_name"]
                )
                # Create PaymentMethod object (with masked data)
                payment_method_obj = CreditCardPaymentMethod(
                    kwargs["card_number"],
                    kwargs["expiry_date"],
                    kwargs["cardholder_name"]
                )
                # Process function for credit card

                def process_func():
                    return payment_method_obj.process(
                        amount,
                        kwargs["card_number"],
                        kwargs["cvv"]
                    )

            elif payment_method == "PAYPAL":
                PayPalPaymentMethod.validate(kwargs["email"])
                # Create PaymentMethod object
                payment_method_obj = PayPalPaymentMethod(kwargs["email"])
                # Process function for PayPal

                def process_func():
                    return payment_method_obj.process(amount, kwargs["email"])

            else:
                raise InvalidPaymentMethodException()

            # Step 2: Create Payment object
            payment = Payment(amount, currency, payment_method, user_id)

            # Step 3: Process payment with retry logic
            max_retries = Transaction.MAX_RETRY_ATTEMPTS
            final_result = None

            for attempt_number in range(1, max_retries + 1):
                # Process payment attempt
                result = process_func()

                # Create Transaction object for this attempt
                transaction_status = TransactionStatus.SUCCESS if result[
                    "status"] == "SUCCESS" else TransactionStatus.FAILED
                transaction = Transaction(
                    payment_id=payment.payment_id,
                    status=transaction_status,
                    gateway_response=result,
                    retry_attempt_number=attempt_number
                )

                # Link transaction to payment
                payment.transactions.append(transaction)
                self.transactions[transaction.transaction_id] = transaction

                # If successful, stop retrying
                if result["status"] == "SUCCESS":
                    final_result = result
                    payment.status = PaymentStatus.SUCCESS
                    break

                # If failed and not retryable, stop retrying
                if not result.get("is_retryable", False):
                    final_result = result
                    payment.status = PaymentStatus.FAILED
                    break

                # If failed but retryable and not last attempt, wait and retry
                if attempt_number < max_retries:
                    # Exponential backoff: 1s, 2s, 4s
                    delay = 2 ** (attempt_number - 1)
                    time.sleep(delay)
                    final_result = result
                else:
                    # Last attempt failed
                    final_result = result
                    payment.status = PaymentStatus.FAILED

            # Step 4: Store Payment object
            self.payments[payment.payment_id] = payment

            # Step 5: Index by user
            if user_id not in self.payments_by_user:
                self.payments_by_user[user_id] = []
            self.payments_by_user[user_id].append(payment.payment_id)

            return payment


class PaymentMethod(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def process(self):
        pass

    def _simulate_payment_processing(self, amount):
        """Simulate payment processing with 90% success rate"""
        if random.random() < 0.9:  # 90% success
            return {"status": "SUCCESS", "transaction_id": generate_id()}
        else:  # 10% failure
            failure_reasons = [
                "Insufficient funds",
                "Card expired",
                "Network error",
                "Invalid credentials"
            ]
            return {
                "status": "FAILED",
                "error": random.choice(failure_reasons)
            }


class CreditCardPaymentMethod(PaymentMethod):
    def __init__(self, card_number, expiry_date, cardholder_name):
        try:
            self.card_last_four_numbers = card_number[-4:]
        except IndexError:
            raise InvalidPaymentDetailsException()
        self.expiry_date = expiry_date
        self.cardholder_name = cardholder_name

    @staticmethod
    def validate(card_number, cvv, expiry_date, cardholder_name):
        if len(card_number) < 13 or len(card_number) > 19:
            raise InvalidPaymentDetailsException()
        if len(cvv) != 3 and len(cvv) != 4:
            raise InvalidPaymentDetailsException()
        m, y = expiry_date.split('/')
        if int(m) < 1 or int(m) > 12:
            raise InvalidPaymentDetailsException()
        if int(y) < datetime.now().year % 100:
            raise InvalidPaymentDetailsException()
        if cardholder_name is None:
            raise InvalidPaymentDetailsException()
        return True

    def process(self, amount, card_number, cvv):
        """
        Process credit card payment

        Args:
            amount: Payment amount
            card_number: Full card number (used for processing, not stored)
            cvv: CVV (used for processing, not stored)

        Returns:
            dict: {
                "status": "SUCCESS" or "FAILED",
                "transaction_id": str (if success),
                "error": str (if failed),
                "is_retryable": bool (if failed)
            }
        """
        # Simulate payment gateway call
        result = self._simulate_payment_processing(amount, card_number, cvv)
        return result

    def _simulate_payment_processing(self, amount, card_number, cvv):
        """Simulate credit card gateway processing"""
        if random.random() < 0.9:  # 90% success
            return {
                "status": "SUCCESS",
                "transaction_id": str(uuid.uuid4()),
                "gateway_response": "Payment processed successfully"
            }
        else:  # 10% failure
            failure_reasons = [
                {"error": "Network error", "is_retryable": True},
                {"error": "Timeout", "is_retryable": True},
                {"error": "Gateway unavailable", "is_retryable": True},
                {"error": "Insufficient funds", "is_retryable": False},
                {"error": "Card expired", "is_retryable": False},
                {"error": "Invalid CVV", "is_retryable": False}
            ]
            error = random.choice(failure_reasons)
            return {
                "status": "FAILED",
                "error": error["error"],
                "is_retryable": error["is_retryable"],
                "transaction_id": None
            }


class DebitCardPaymentMethod(PaymentMethod):
    pass


class PayPalPaymentMethod(PaymentMethod):
    def __init__(self, email):
        self.email = email

    @staticmethod
    def validate(email):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise InvalidPaymentDetailsException()
        return True

    def process(self, amount, email):
        """
        Process PayPal payment

        Args:
            amount: Payment amount
            email: PayPal email (used for processing)

        Returns:
            dict: {
                "status": "SUCCESS" or "FAILED",
                "transaction_id": str (if success),
                "error": str (if failed),
                "is_retryable": bool (if failed)
            }
        """
        # Simulate PayPal gateway call
        result = self._simulate_payment_processing(amount, email)
        return result

    def _simulate_payment_processing(self, amount, email):
        """Simulate PayPal gateway processing"""
        if random.random() < 0.9:  # 90% success
            return {
                "status": "SUCCESS",
                "transaction_id": str(uuid.uuid4()),
                "gateway_response": "PayPal payment processed successfully"
            }
        else:  # 10% failure
            failure_reasons = [
                {"error": "Network error", "is_retryable": True},
                {"error": "PayPal service unavailable", "is_retryable": True},
                {"error": "Timeout", "is_retryable": True},
                {"error": "Insufficient PayPal balance", "is_retryable": False},
                {"error": "Invalid PayPal account", "is_retryable": False},
                {"error": "Account suspended", "is_retryable": False}
            ]
            error = random.choice(failure_reasons)
            return {
                "status": "FAILED",
                "error": error["error"],
                "is_retryable": error["is_retryable"],
                "transaction_id": None
            }


class Payment:
    def __init__(self, amount, currency, payment_method, user_id):
        self.payment_id = str(uuid.uuid4())
        self.amount = amount
        self.currency = currency
        self.payment_method = payment_method
        self.user_id = user_id
        self.status = PaymentStatus.PENDING
        self.transactions = []
        self.refund = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class Transaction:
    '''- Transaction ID, Payment ID (foreign key), Amount, Status, Gateway Response, Timestamp, Retry Attempt Number
    - Multiple Transactions per Payment (for retries)
    - Each transaction represents one attempt to process the payment'''
    MAX_RETRY_ATTEMPTS = 3

    def __init__(self, payment_id, status, gateway_response, retry_attempt_number):
        self.transaction_id = str(uuid.uuid4())
        self.payment_id = payment_id
        self.status = status
        self.gateway_response = gateway_response
        self.retry_attempt_number = retry_attempt_number
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class PaymentStatus(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'
    CANCELLED = 'CANCELLED'


class TransactionStatus(Enum):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class Refund:
    '''- **Refund**: Represents a refund transaction
    - Refund ID, Payment ID, Amount, Status, Timestamp'''

    def __init__(self, payment_id, amount, status):
        self.refund_id = str(uuid.uuid4())
        self.payment_id = payment_id
        self.amount = amount
        self.status = status
        self.created_at = datetime.now()


class InvalidPaymentDetailsException(Exception):
    def __init__(self):
        super().__init__('Invalid payment details')


class InvalidPaymentMethodException(Exception):
    def __init__(self):
        super().__init__('Invalid payment method')


# Test Case 1: Successful credit card payment
gateway = PaymentGateway()
payment = gateway.process_payment(
    amount=1000.00,
    currency="USD",
    payment_method="CREDIT_CARD",
    card_number="4111111111111111",  # Valid test card
    cvv="123",
    expiry_date="12/25",
    cardholder_name="John Doe",
    user_id="user1"
)
assert payment.status == "SUCCESS"
assert payment.amount == 1000.00

# Test Case 2: Invalid card number
try:
    gateway.process_payment(
        amount=100.00,
        payment_method="CREDIT_CARD",
        card_number="1234",  # Invalid
        cvv="123",
        expiry_date="12/25",
        cardholder_name="John Doe",
        user_id="user1"
    )
    assert False, "Should raise InvalidPaymentDetailsException"
except InvalidPaymentDetailsException:
    pass

# Test Case 3: Refund successful payment
refund = gateway.refund_payment(
    payment_id=payment.payment_id,
    amount=1000.00,
    reason="Customer request"
)
assert refund.status == "SUCCESS"
assert refund.amount == 1000.00

# Test Case 4: Refund failed payment (should fail)
failed_payment = gateway.process_payment(...)  # Assume this fails
try:
    gateway.refund_payment(failed_payment.payment_id, 100.00, "reason")
    assert False, "Should raise RefundNotAllowedException"
except RefundNotAllowedException:
    pass

# Test Case 5: Refund amount exceeds payment
try:
    gateway.refund_payment(payment.payment_id, 2000.00, "reason")
    assert False, "Should raise InvalidRefundAmountException"
except InvalidRefundAmountException:
    pass
