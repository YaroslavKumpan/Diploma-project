# Telegram Bots Marketplace

## Overview

**Telegram Bots Marketplace** is an API designed for managing Telegram bots and their associated products. This project aims to streamline the operations related to both products and users, providing a robust and scalable solution.

## Features

- **Product Management**: Create, read, update, and delete operations for managing products related to Telegram bots.
- **User Management**: Operations for handling user accounts and their interactions with products.

## API Documentation

### Version
- **Version**: 1.0.0

### OpenAPI Tags
- **Products**: Operations with products
- **Users**: Operations with users

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YaroslavKumpan/Diploma-project.git
   cd telegram-bots-marketplace
   
2. Install dependencies using Poetry:
   poetry install

3. Activate the virtual environment:
   poetry shell

## Usage
To start the API server, run:

    - python main.py

## Running Tests
To execute the test suite, use:
    
    - poetry run pytest

## Docker Support
To build and run the application using Docker, use the following commands:

1. Build the Docker image:
    
    - docker build -t telegram-bots-marketplace .

2. Run the Docker container:

    - docker run -p 8000:8000 telegram-bots-marketplace

## Contributing
Contributions are welcome! Please read the CONTRIBUTING.md for more information on how to get started.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
