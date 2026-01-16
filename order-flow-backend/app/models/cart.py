from app import db
from datetime import datetime  #-added

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    menu_item_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # ADDED: snapshot fields for price & name stability
    menu_item_name = db.Column(db.String(100), nullable=False)
    menu_item_price = db.Column(db.Float, nullable=False)
    
    # ADDED: timestamps for consistency
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'menu_item_id': self.menu_item_id,
            'name': self.menu_item_name,      #-added
            'price': self.menu_item_price,    #-added
            'quantity': self.quantity,
            'subtotal': round(self.menu_item_price * self.quantity, 2)  #-added
        }