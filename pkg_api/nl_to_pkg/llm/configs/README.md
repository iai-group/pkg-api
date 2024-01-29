# This folder contains the config files needed to use the Ollama instance.

* The config yaml must contain:
    - host: replace ADD_OLLAMA_HOST with an instance of Ollama installed following the instructions [here](https://ollama.ai/download/linux).
    - model: `llama2`, `mistral` etc.
    - options: Hyperparameters for the model.
    - stream: If it is a chat response set stream to true otherwise false.

* Following configs are currently in the folder:
    - `llm_config_llama2.yaml`: Contains config for the `llama2` model.
    - `llm_config_mistral.yaml`: Contains config for the `mistral` model.
