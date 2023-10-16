# Discord Success

The Discord Success bot is designed to track and reward success stories and vouches within a Discord community.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Data Management](#data-management)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

- [Bot Script](./Discord_success_bot.py) - The main script that runs the functionalities of the Discord Success bot.
- [Configuration File](./Config.json) - Contains the bot's configuration parameters.
- [Points Data](./Points.json) - Manages user points based on their success stories.
- [Vouches Data](./Vouches.json) - Tracks vouches given to users.
- [Requirements](./requirements.txt) - Lists all the dependencies needed for the project.

## Getting Started

1. Clone the repository: `git clone <repository_url>`
2. Navigate to the directory: `cd Discord_Success`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Update the [Config.json](./Config.json) with your Discord bot token and other necessary configurations.
5. Run the bot script: `python Discord_success_bot.py`

## Requirements

Install all the necessary dependencies for this project using the following command:

```bash
pip install -r requirements.txt
```

## Configuration

The [Config.json](./Config.json) file allows you to set various parameters for the bot, such as the bot token, prefix, and other relevant settings.

## Data Management

- [Points.json](./Points.json): All user points, based on their success stories, are stored in this file.
- [Vouches.json](./Vouches.json): This file keeps a record of vouches given to users within the community.
