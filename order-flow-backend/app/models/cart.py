from app import db

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    def to_dict(self):
        item_data = {
            'id': self.id,
            'user_id': self.user_id,
            'menu_item_id': self.menu_item_id,
            'quantity': self.quantity
        }
        if self.menu_item:
            item_data['menu_item'] = self.menu_item.to_dict()
            item_data['subtotal'] = self.menu_item.price * self.quantity
        return item_data