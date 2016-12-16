from robotpico import app

if __name__ == '__main__':
    if app.DEBUG_MODE:
        app.app.run(debug=True, use_reloader=False, host='0.0.0.0')
    else:
        app.app.run(host='0.0.0.0')