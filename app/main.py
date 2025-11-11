from flask import Flask

app = Flask(__name__)

# 导入蓝图
from api.routes import api_bp
from function.routes import function_bp

# 注册蓝图
app.register_blueprint(
    api_bp, url_prefix="/api", static_folder="static", template_folder="templates"
)
app.register_blueprint(
    function_bp, url_prefix="/function", static_folder="static", template_folder="templates"
)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
