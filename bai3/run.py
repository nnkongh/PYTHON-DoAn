from blog import create_app

app = create_app()
if __name__ == '__main__':
    create_app()
    app.run(debug=True)



