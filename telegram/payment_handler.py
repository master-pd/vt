# -*- coding: utf-8 -*-
"""
PAYMENT HANDLER - MANAGE PAYMENTS AND SUBSCRIPTIONS
AUTHOR: MASTER (RANA)
TEAM: MAR PD
"""

import hashlib
import time
from datetime import datetime
from typing import Dict, Optional
from database.database import Database
from utils.logger import bot_logger

class PaymentHandler:
    def __init__(self):
        self.db = Database()
        self.payments = {}  # payment_id -> payment_data
        
        # Payment plans
        self.plans = {
            'free': {
                'name': 'Free Plan',
                'price': 0,
                'daily_tests': 10,
                'daily_views': 100000,
                'max_views_per_test': 10000,
                'features': ['Basic Testing', '10 Tests/Day']
            },
            'basic': {
                'name': 'Basic Plan',
                'price': 9.99,
                'daily_tests': 50,
                'daily_views': 500000,
                'max_views_per_test': 50000,
                'features': ['50 Tests/Day', 'Priority Queue', 'Basic Support']
            },
            'pro': {
                'name': 'Professional Plan',
                'price': 29.99,
                'daily_tests': 200,
                'daily_views': 2000000,
                'max_views_per_test': 100000,
                'features': ['Unlimited Tests', 'Priority Processing', '24/7 Support', 'Advanced Analytics']
            },
            'enterprise': {
                'name': 'Enterprise Plan',
                'price': 99.99,
                'daily_tests': 1000,
                'daily_views': 10000000,
                'max_views_per_test': 500000,
                'features': ['Custom Limits', 'Dedicated Support', 'API Access', 'Custom Features']
            }
        }
    
    def create_payment(self, user_id: int, plan: str, amount: float, currency: str = 'USD') -> Optional[str]:
        """Create a new payment"""
        if plan not in self.plans:
            bot_logger.error(f"Invalid plan: {plan}")
            return None
        
        plan_data = self.plans[plan]
        
        # Generate payment ID
        payment_data = f"{user_id}{plan}{time.time()}{amount}"
        payment_id = hashlib.md5(payment_data.encode()).hexdigest()[:16]
        
        payment = {
            'payment_id': payment_id,
            'user_id': user_id,
            'plan': plan,
            'amount': amount,
            'currency': currency,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'expires_at': None,
            'payment_method': None,
            'transaction_id': None,
            'notes': ''
        }
        
        self.payments[payment_id] = payment
        bot_logger.info(f"Payment created: {payment_id} for user {user_id}, plan {plan}")
        
        return payment_id
    
    def process_payment(self, payment_id: str, payment_method: str, transaction_id: str = None) -> bool:
        """Process a payment"""
        if payment_id not in self.payments:
            bot_logger.error(f"Payment not found: {payment_id}")
            return False
        
        payment = self.payments[payment_id]
        
        # Update payment status
        payment['status'] = 'completed'
        payment['payment_method'] = payment_method
        payment['transaction_id'] = transaction_id
        payment['completed_at'] = datetime.now().isoformat()
        
        # Calculate expiration (30 days from now)
        expire_date = datetime.now().timestamp() + (30 * 24 * 3600)
        payment['expires_at'] = datetime.fromtimestamp(expire_date).isoformat()
        
        # Update user plan in database
        # This would update user's subscription
        
        bot_logger.info(f"Payment processed: {payment_id}, method: {payment_method}")
        return True
    
    def get_payment(self, payment_id: str) -> Optional[Dict]:
        """Get payment details"""
        return self.payments.get(payment_id)
    
    def get_user_payments(self, user_id: int) -> List[Dict]:
        """Get all payments for a user"""
        user_payments = []
        
        for payment in self.payments.values():
            if payment['user_id'] == user_id:
                user_payments.append(payment)
        
        return sorted(user_payments, key=lambda x: x['created_at'], reverse=True)
    
    def get_plan_details(self, plan: str) -> Optional[Dict]:
        """Get plan details"""
        return self.plans.get(plan)
    
    def get_all_plans(self) -> Dict:
        """Get all available plans"""
        return self.plans
    
    def generate_payment_link(self, payment_id: str, gateway: str = 'stripe') -> Optional[str]:
        """Generate payment link for a gateway"""
        if payment_id not in self.payments:
            return None
        
        payment = self.payments[payment_id]
        
        # Generate payment link based on gateway
        if gateway == 'stripe':
            # Generate Stripe payment link
            amount = int(payment['amount'] * 100)  # Convert to cents
            return f"https://buy.stripe.com/test_XXX/{payment_id}"
        
        elif gateway == 'paypal':
            # Generate PayPal payment link
            return f"https://www.paypal.com/paypalme/XXX/{payment_id}"
        
        elif gateway == 'crypto':
            # Generate crypto payment address
            return f"BTC Address: 1ABC... for {payment['amount']} {payment['currency']}"
        
        return None
    
    def check_subscription(self, user_id: int) -> Dict:
        """Check user's subscription status"""
        # Get user's active payment
        user_payments = self.get_user_payments(user_id)
        active_payment = None
        
        for payment in user_payments:
            if payment['status'] == 'completed':
                # Check if not expired
                if payment['expires_at']:
                    expire_date = datetime.fromisoformat(payment['expires_at'])
                    if datetime.now() < expire_date:
                        active_payment = payment
                        break
        
        if active_payment:
            plan = active_payment['plan']
            plan_data = self.plans.get(plan, self.plans['free'])
            
            return {
                'has_subscription': True,
                'plan': plan,
                'plan_name': plan_data['name'],
                'expires_at': active_payment['expires_at'],
                'payment_id': active_payment['payment_id'],
                'limits': {
                    'daily_tests': plan_data['daily_tests'],
                    'daily_views': plan_data['daily_views'],
                    'max_views_per_test': plan_data['max_views_per_test']
                },
                'features': plan_data['features']
            }
        else:
            # Free plan
            plan_data = self.plans['free']
            
            return {
                'has_subscription': False,
                'plan': 'free',
                'plan_name': plan_data['name'],
                'expires_at': None,
                'payment_id': None,
                'limits': {
                    'daily_tests': plan_data['daily_tests'],
                    'daily_views': plan_data['daily_views'],
                    'max_views_per_test': plan_data['max_views_per_test']
                },
                'features': plan_data['features']
            }
    
    def cancel_subscription(self, user_id: int) -> bool:
        """Cancel user's subscription"""
        # Find active subscription
        subscription = self.check_subscription(user_id)
        
        if not subscription['has_subscription']:
            return False
        
        # Mark as cancelled
        payment_id = subscription['payment_id']
        if payment_id in self.payments:
            self.payments[payment_id]['status'] = 'cancelled'
            self.payments[payment_id]['cancelled_at'] = datetime.now().isoformat()
            
            bot_logger.info(f"Subscription cancelled for user {user_id}")
            return True
        
        return False
    
    def get_revenue_statistics(self, period: str = 'monthly') -> Dict:
        """Get revenue statistics"""
        # Calculate revenue from completed payments
        total_revenue = 0
        payment_count = 0
        
        for payment in self.payments.values():
            if payment['status'] == 'completed':
                total_revenue += payment['amount']
                payment_count += 1
        
        # Plan distribution
        plan_distribution = {}
        for payment in self.payments.values():
            if payment['status'] == 'completed':
                plan = payment['plan']
                plan_distribution[plan] = plan_distribution.get(plan, 0) + 1
        
        return {
            'total_revenue': total_revenue,
            'total_payments': payment_count,
            'avg_payment_value': total_revenue / payment_count if payment_count > 0 else 0,
            'plan_distribution': plan_distribution,
            'currency': 'USD',
            'period': period
        }