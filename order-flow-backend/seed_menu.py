from app import create_app, db
from app.models.menu_item import MenuItem

def seed_menu():
    menu_items = [
        # Pizza
        {"name": "Cheese Pizza", "description": "Classic cheese pizza with tomato sauce and mozzarella.", "price": 1200,
         "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop"},
        {"name": "Pepperoni Pizza", "description": "Pepperoni slices on cheese pizza.", "price": 1500,
         "image_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=300&fit=crop"},
        
        # Burgers
        {"name": "Chicken Burger", "description": "Grilled chicken burger with lettuce and mayo.", "price": 850,
         "image_url": "https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=400&h=300&fit=crop"},
        {"name": "Cheeseburger", "description": "Beef burger with cheese.", "price": 800,
         "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop"},
        
        # Sides & Salads
        {"name": "French Fries", "description": "Crispy golden fries.", "price": 350,
         "image_url": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=300&fit=crop"},
        {"name": "Caesar Salad", "description": "Fresh lettuce with Caesar dressing.", "price": 700,
         "image_url": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=300&fit=crop"},
        
        # Drinks & Dessert
        {"name": "Soda (500ml)", "description": "Cold fizzy drink.", "price": 200,
         "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=400&h=300&fit=crop"},
        {"name": "Ice Cream (1 scoop)", "description": "Vanilla ice cream.", "price": 250,
         "image_url": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400&h=300&fit=crop"},

        # Kenyan Food
        {"name": "Ugali", "description": "Maize flour stiff porridge.", "price": 300,
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzb-6bIRDnF_6uGAzFV4bi9dqKkQx8NHZ_Ug&s"},
        {"name": "Nyama Choma", "description": "Grilled meat with kachumbari.", "price": 1400,
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4zDkfi_PatswZ6kHYo3wwEFKmyFFo0VbpPQ&s"},
        {"name": "Sukuma Wiki", "description": "Stir-fried greens.", "price": 350,
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTveEg6PysUTItwItGRMdZqJ921vojqGaNg2w&s"},
        {"name": "Mchuzi wa Samaki", "description": "Fish stew in coconut sauce.", "price": 900,
         "image_url": "https://i.ytimg.com/vi/j_e91hLZtG0/hq720.jpg"},
        {"name": "Chapati", "description": "Soft flatbread.", "price": 250,
         "image_url": "https://i.pinimg.com/736x/2a/27/09/2a27096c2010304ec371e3ee9371a070.jpg"},
        {"name": "Githeri", "description": "Beans and maize stew.", "price": 450,
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPa8cQ5fQE4p8AB1765z-NgvJ-QEPdiKfwsA&s"},
        {"name": "Mandazi", "description": "Sweet fried dough.", "price": 120,
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbeXdkLVLLrUF3QJox3gUVZICWw32P5XlV0g&s"},
        {"name": "Kuku Paka", "description": "Chicken coconut curry.", "price": 1100,
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkL92GzZ2LAZjJBKljNoRg9Xko6appOOc4dQ&s"},
        {"name": "Chilli Sachet", "description": "Spicy chili sachet for extra flavor.", "price": 10,
         "image_url": "https://daganghalal.blob.core.windows.net/19128/Product/500x500__chilli-sauce-9g.png"}
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

