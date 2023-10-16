# Dev Assistant

Welcome to the [Dev Assistant](https://devassistant.tonet.dev) plugin for ChatGPT.

## What is it?

[Dev Assistant](https://devassistant.tonet.dev) is a plugin for ChatGPT that assists us developers by executing tasks directly on our clients.

Dev Assistant Client (this repo) is a Python package that is basically the core component of the project. It receives instructions from ChatGPT via Dev Assistant plugin, executes it on any of your clients and send the response back.

## Features

The Dev Assistant Local Client is designed to streamline your development process by offering a range of functionalities:

- **File Management**: Create, read, update, and delete files. List the contents of a directory. You can manage your files without leaving your conversation with ChatGPT.

- **Git Version Control**: Initialize a Git repository, add changes to the staging area, commit changes, and push changes to a remote repository. Get the status of the Git repository. You can manage your Git repositories directly through ChatGPT.

- **Terminal Commands Execution**: Execute commands directly in the terminal. You can run any command in your terminal directly from ChatGPT.

## Requirements

- 👌🏼 Python 3.6+
- 👌🏼 pip
- 💸 ChatGPT Plus subscription _(for plugins store access)_

## Installation

- Create a Dev Assistant account at [devassistant.tonet.dev](https://devassistant.tonet.dev)
- Generate a token at [https://devassistant.tonet.dev/user/api-tokens](https://devassistant.tonet.dev/user/api-tokens) for ChatGPT and save it. You'll need it later.
- Install the local client:
  - [Install Python](https://www.python.org/downloads/)
  - [Install pip](https://pip.pypa.io/en/stable/)
  - Run `pip install dev-assistant-client` in your terminal  
- Install the ChatGPT plugin:
  - On the [ChatGPT Plugins Store](https://chat.openai.com/plugins), click in the **"Install an unverified plugin"** at bottom of Plugin store dialog window, paste the <https://devassistant.tonet.dev> and click on "Find plugin".
  - ChatGPT will ask you to enter your credentials. Insert the token generated in the second step and click "Install plugin".
  - Enable the plugin in the list of installed plugins and you're good to go!

## Usage

Once installed, just run the following:

```bash
dev-assistant
```

You will be prompted to enter your email and password, if you're not already logged in. Once authenticated, the client will automatically establish a connection with the server.

If everything runs well, you will see the Dev Assistant CLI presentation and a exclusive _CLIENT ID_, like this:

```
# dev-assistant

    .-----.   Dev Assistant
    | >_< |   v0.1.28
    '-----'   https://devassistant.tonet.dev

31/07/2023 00:43:19     Connecting...
31/07/2023 00:43:20     Connected.      CLIENT ID 654c5jf7-7993-4b44-ae92-ec51t88339cd
...
```

You can now ask ChatGPT to help you directly on that client.

You can do `CRTL+C` to stop the client at any time.

To log out, use:

```bash
dev-assistant logout
```

This command will remove your saved authentication token, ensuring your security.

## Contributing

We welcome contributions! If you have an idea for an improvement or have found a bug, please open an issue. Feel free to fork the repository and submit a pull request if you'd like to contribute code. Please follow the code style and conventions used in the existing codebase.

## License

The Dev Assistant Local Client is open-source software, licensed under the [MIT license](LICENSE).

## Support

If you encounter any problems or have any questions, don't hesitate to open an issue on GitHub. We're here to help!

## Acknowledgements

A big thank you to all contributors and users for your support! We couldn't do it without you.

## Authors

- [Luciano T.](https://github.com/lucianotonet)
- [ChatGPT](https://chat.openai.com/)
- [GitHub Copilot](https://copilot.github.com/)
