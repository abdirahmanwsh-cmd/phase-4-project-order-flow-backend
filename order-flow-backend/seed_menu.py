from app import create_app, db
from app.models.menu_item import MenuItem

def seed_menu():
    menu_items = [
        {"name": "Cheese Pizza", "description": "Classic cheese pizza with tomato sauce and mozzarella.", "price": 1200},
        {"name": "Pepperoni Pizza", "description": "Pepperoni slices on cheese pizza.", "price": 1500},
        {"name": "Chicken Burger", "description": "Grilled chicken burger with lettuce and mayo.", "price": 850},
        {"name": "Cheeseburger", "description": "Beef burger with cheese.", "price": 800},
        {"name": "French Fries", "description": "Crispy golden fries.", "price": 350},
        {"name": "Caesar Salad", "description": "Fresh lettuce with Caesar dressing.", "price": 700},
        {"name": "Soda (500ml)", "description": "Cold fizzy drink.", "price": 200},
        {"name": "Ice Cream (1 scoop)", "description": "Vanilla ice cream.", "price": 250},

        # Kenyan food
        {"name": "Ugali", "description": "Maize flour stiff porridge.", "price": 300},
        {"name": "Nyama Choma", "description": "Grilled meat with kachumbari.", "price": 1400},
        {"name": "Sukuma Wiki", "description": "Stir-fried greens.", "price": 350},
        {"name": "Mchuzi wa Samaki", "description": "Fish stew in coconut sauce.", "price": 900},
        {"name": "Chapati", "description": "Soft flatbread.", "price": 250},
        {"name": "Githeri", "description": "Beans and maize stew.", "price": 450},
        {"name": "Mandazi", "description": "Sweet fried dough.", "price": 120},
        {"name": "Kuku Paka", "description": "Chicken coconut curry.", "price": 1100},
    ]

    for item in menu_items:
        if not MenuItem.query.filter_by(name=item["name"]).first():
            db.session.add(MenuItem(**item))

    db.session.commit()
    print("✅ Menu seeding complete")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_menu()
