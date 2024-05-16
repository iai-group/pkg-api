# Run PKG API demo

This document explains how to run the PKG API demo. It includes the requirements, starting commands for the client and server, and additional information on its usage.

## Requirements

Below you have the requirements for running the PKG API demo.

### PKG Client

  - Node.js
  - npm
  - Disable CORS in your web browser, see how for [Chrome](https://stackoverflow.com/a/6083677) and [Safari](https://stackoverflow.com/a/12158217)

### PKG Server

  - Python 3.9
  - requirements.txt, can be installed by running: `pip install -r requirements.txt`
  - GraphViz, download from [here](https://graphviz.org/download/) (the recommended version is 9.0.0)

## Start PKG Client

Run the following commands:

```bash
cd pkg_client
npm install
npm start
```

The client will start and listen on port 3000. Note that `npm install` should be run only once.

## Start PKG Server

Update `ADD_OLLAMA_HOST` in `pkg_api/nl_to_pkg/llm/configs/llm_config_mistral.yaml` to the address of your instance of Ollama (see [documentation](https://ollama.com/)).
Then, run the following command:

```bash
flask --app pkg_api/server run --debug
```

The server will start and listen on port 5000. Note that the configuration of the server may be modified in `pkg_api/server/config.py`.

## Additional information

  - The population form does not empty itself after submission
  - Always use the button to send forms, if you press enter you will be redirected to the logging page
  - In the population form, you should use the switches for predicate and object when they cannot be associated with an URI
