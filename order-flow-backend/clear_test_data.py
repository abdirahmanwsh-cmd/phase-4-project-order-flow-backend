#!/usr/bin/env python3
"""Script to clear test data from the database"""

from app import create_app, db
from app.models.order import Order
from app.models.order_item import OrderItem

def clear_test_orders():
    app = create_app()
    with app.app_context():
        try:
            # Delete all order items first (due to foreign key constraints)
            OrderItem.query.delete()
            # Then delete all orders
            Order.query.delete()
            db.session.commit()
            print("✅ All test orders and order items have been cleared")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error clearing data: {str(e)}")

if __name__ == '__main__':
    clear_test_orders()
