This is a simple CLI tool to track Berlin's public transport in real time. Powered by [VBB Transport API](v6.vbb.transport.rest).

It's a learning project for me, so nothing crazy.

## Features:
- Automatically finds the station ID based on the name of the station
- Fetches live data for any station in Berlin
- Simple caching implemented with local json file
- Colorful Berlin-themed UI using the `rich` library

## To-Do:

- Add command-line arguments
- Refactor code, make it modular

## Installation

1. Clone the repository
    ```bash
    git clone https://github.com/ataraxiavibin/tramweg.git
    cd tramweg
    ```
2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Simply run the script: 

  ```bash
  python tramweg.py
  ```

## License

This project is free software licensed under the **GNU General Public License v3.0**.
See the [LICENSE](LICENSE.md) file for details.
