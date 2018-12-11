from flask import Flask, redirect
from blueprints.stock_viewer import stock_viewer_blueprint


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Blueprints
app.register_blueprint(stock_viewer_blueprint)

@app.route('/')
def index():
    return redirect("/stock-viewer/")

if __name__ == '__main__':
    app.run()