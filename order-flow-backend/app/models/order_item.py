from app import db

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Relationship to MenuItem
    menu_item = db.relationship('MenuItem', backref='order_items', foreign_keys=[menu_item_id])
    
    def to_dict(self):
        item_dict = {
            'id': self.id,
            'order_id': self.order_id,
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.price * self.quantity
        }
        
        # Include menu item details if relationship exists
        if self.menu_item:
            item_dict['menu_item'] = {
                'id': self.menu_item.id,
                'name': self.menu_item.name,
                'description': self.menu_item.description,
                'image_url': self.menu_item.image_url
            }
        
        return item_dict