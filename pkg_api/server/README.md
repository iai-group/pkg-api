# PKG API Backend Server

The backend server is a Flask server that connects the frontend users and services to PKGs.

## Starting the server

Before starting the server, make sure that the requirements are installed and that CORS is disabled in your web browser.

To start the server, run the following command:

```bash
flask --app pkg_api/server run --debug
```

Note the `--debug` flag is optional, but it is recommended to use it during development.

By default, the server will run locally on port 5000.
In case you want to run the server on a different port, you can specify the port using the `--port` flag.
However, you will also need to update `PKG_API_BASE_URL` in `pkg_client/public/config.json` to ensure that the client uses the correct URL.
