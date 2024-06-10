import connexion as cn

app = cn.App(__name__, specification_dir='./')

app.add_api('swagger.yml')

@app.route('/')
def home():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(port=5555)