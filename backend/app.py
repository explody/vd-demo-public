import config
from connexion.resolver import MethodViewResolver

app = config.connex_app
app.add_api(f"{config.basedir}/swagger.yml")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
