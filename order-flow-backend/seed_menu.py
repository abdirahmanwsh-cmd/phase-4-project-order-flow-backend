from app import create_app, db
from app.models.menu_item import MenuItem

def seed_menu():
    menu_items = [
        {"name": "Cheese Pizza", "description": "Classic cheese pizza with tomato sauce and mozzarella.", "price": 1200,
         "image_url": "https://images.unsplash.com/photo-1548365328-8b849e6f3b9a"},
        {"name": "Pepperoni Pizza", "description": "Pepperoni slices on cheese pizza.", "price": 1500,
         "image_url": "https://images.unsplash.com/photo-1601924582975-7c19b7a7a0c7"},
        {"name": "Chicken Burger", "description": "Grilled chicken burger with lettuce and mayo.", "price": 850,
         "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349"},
        {"name": "Cheeseburger", "description": "Beef burger with cheese.", "price": 800,
         "image_url": "https://images.unsplash.com/photo-1550547660-d9450f859349"},
        {"name": "French Fries", "description": "Crispy golden fries.", "price": 350,
         "image_url": "https://images.unsplash.com/photo-1576107232684-1279f390859f"},
        {"name": "Caesar Salad", "description": "Fresh lettuce with Caesar dressing.", "price": 700,
         "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38"},
        {"name": "Soda (500ml)", "description": "Cold fizzy drink.", "price": 200,
         "image_url": "https://images.unsplash.com/photo-1585238342020-4a6b0b0d5a3f"},
        {"name": "Ice Cream (1 scoop)", "description": "Vanilla ice cream.", "price": 250,
         "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"},

         # Kenyan food
        {"name": "Ugali", "description": "Maize flour stiff porridge.", "price": 300,
         "image_url": "https://images.unsplash.com/photo-1633945274417-51c8a4e5d2e4"},
        {"name": "Nyama Choma", "description": "Grilled meat with kachumbari.", "price": 1400,
         "image_url": "https://images.unsplash.com/photo-1626776876729-bab6cfd97d7e"},
        {"name": "Sukuma Wiki", "description": "Stir-fried greens.", "price": 350,
         "image_url": "https://images.unsplash.com/photo-1564758866810-1b9f0a41e2d0"},
        {"name": "Mchuzi wa Samaki", "description": "Fish stew in coconut sauce.", "price": 900,
         "image_url": "https://images.unsplash.com/photo-1601050691351-1d6d6b3d2b58"},
        {"name": "Chapati", "description": "Soft flatbread.", "price": 250,
         "image_url": "https://images.unsplash.com/photo-1625944525101-6d72f0f2b1e6"},
        {"name": "Githeri", "description": "Beans and maize stew.", "price": 450,
         "image_url": "https://images.unsplash.com/photo-1604908176997-3b7e3c07e02a"},
        {"name": "Mandazi", "description": "Sweet fried dough.", "price": 120,
         "image_url": "https://images.unsplash.com/photo-1511920170033-f8396924c348"},
        {"name": "Kuku Paka", "description": "Chicken coconut curry.", "price": 1100,
         "image_url": "https://images.unsplash.com/photo-1604908176997-3b7e3c07e02a"},
        {"name": "Chilli Sachet", "description": "Spicy chili sachet for extra flavor.", "price": 10,
         "image_url": "https://images.unsplash.com/photo-1582281298055-e25b84a30b0b"}
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

