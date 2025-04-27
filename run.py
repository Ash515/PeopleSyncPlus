from server import app
from ClientScript import ClientApp
from AdminScript import AdminApp

# Register Blueprints
app.register_blueprint(ClientApp)
app.register_blueprint(AdminApp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)