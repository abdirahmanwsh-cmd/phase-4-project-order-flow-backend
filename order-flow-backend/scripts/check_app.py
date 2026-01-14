import traceback

try:
    from app import create_app, db
    app = create_app()
    print('App created')
    with app.app_context():
        db.create_all()
        print('DB tables created; engine =', db.engine)
except Exception:
    print('Exception during startup:')
    traceback.print_exc()
