<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">BerniceBot</h3>

  <p align="center">
    **[TODO: Add a short description of your card collection bot theme]**
    <br />
    <a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME">View Demo</a>
    &middot;
    <a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#customization">Customization</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

BerniceBot is a Discord bot that implements a gacha-style card collection system. **[TODO: Describe your specific theme - e.g., "featuring Pokemon characters", "collecting Magic: The Gathering cards", "anime waifu collection", etc.]**

Here's why this project stands out:
* **Engaging Collection System**: Features a complete gacha mechanics with randomized card pulls
* **Persistent Storage**: Uses PostgreSQL for reliable data persistence across sessions
* **Containerized Deployment**: Full Docker support for easy deployment and scaling
* **Modular Architecture**: Clean separation of concerns with dedicated services for gacha, cards, and data management
* **Rich Discord Integration**: Interactive commands with embeds and user-friendly responses

The bot includes commands for pulling cards (`bdrop`/`bd`), viewing inventory (`binv`/`bi`), and checking collection statistics.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![Discord.py][Discord.py]][Discord-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![AsyncPG][AsyncPG]][AsyncPG-url]
* [![Docker][Docker]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow these instructions to get BerniceBot running on your local machine or deploy it to a server.

### Prerequisites

Before running BerniceBot, ensure you have the following installed:

* **Docker and Docker Compose**
  - [Install Docker](https://docs.docker.com/get-docker/)
  - [Install Docker Compose](https://docs.docker.com/compose/install/)

* **Discord Bot Token**
  - Create a Discord application at [Discord Developer Portal](https://discord.com/developers/applications)
  - Go to the "Bot" section and create a bot
  - Copy the bot token (you'll need this for the `.env` file)

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Set up environment variables**
   ```sh
   cp .env.docker .env
   ```
   Edit `.env` and replace the placeholder values:
   - `DISCORD_TOKEN`: Your Discord bot token from step 2 in Prerequisites
   - Database settings (can keep defaults for local development)

3. **Start the application with Docker Compose**
   ```sh
   docker-compose up --build
   ```

4. **Invite the bot to your Discord server**
   - In Discord Developer Portal, go to OAuth2 > URL Generator
   - Select `bot` scope and appropriate permissions (send messages, embed links, etc.)
   - Use the generated URL to invite the bot to your server

### Local Development Setup

For local development with direct Python execution instead of Docker:

1. **Set up Python virtual environment**
   ```sh
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Start only the database with Docker**
   ```sh
   docker-compose up db
   ```
   This runs PostgreSQL on port 5433 with automatic table and data initialization.

4. **Run the bot directly**
   ```sh
   python src/bot/bot.py
   ```

5. **Invite the bot to your Discord server**
   - Follow the same steps as above for inviting the bot to your server

**Note**: When using local development, ensure your `.env` file has the correct database URL pointing to the Docker database (`postgresql://devuser:devpass@localhost:5433/devdb`).

#### Database Administration with pgAdmin

To view and manage the BerniceBot database during development:

1. **Install pgAdmin**
   - Download and install pgAdmin from [pgadmin.org](https://www.pgadmin.org/download/)
   - Or use Docker: `docker run -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=admin@example.com -e PGADMIN_DEFAULT_PASSWORD=admin dpage/pgadmin4`

2. **Connect to the database**
   - Open pgAdmin
   - Right-click "Servers" → "Create" → "Server"
   - Enter connection details:
     - **Host name/address**: `localhost`
     - **Port**: `5433`
     - **Username**: `devuser`
     - **Password**: `devpass`
     - **Database**: `devdb`

3. **Explore the data**
   - Navigate to `devdb` → `Schemas` → `public` → `Tables`
   - **Key tables to explore**:
     - `card`: All user card collections with codes, tiers, and ownership
     - `character`: Character information **[TODO: update for your theme]**
     - `anime`: **[TODO: update category for your theme]**
     - `card_supply`: Print run tracking for each character
     - `user`: Discord user records

4. **Useful queries**
   ```sql
   -- View all cards owned by a specific user
   SELECT c.card_id, ch.character_name, a.anime_name, c.tier, c.print_number
   FROM card c
   JOIN character ch ON c.character_id = ch.character_id
   JOIN anime a ON ch.anime_id = a.anime_id
   WHERE c.owner_id = 'YOUR_DISCORD_USER_ID';

   -- **[TODO: Add theme-specific queries]**
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Once the bot is running and invited to your server, use these commands:

### Basic Commands

* **`bdrop` or `bd`** - Pull a random character card from the gacha **[TODO: update for your theme]**
* **`binv` or `bi`** - View your card inventory (paginated)
* **`bview <code>` or `bv <code>`** - View details of a specific card by its code
* **`bstats` or `bs`** - View circulation statistics for all cards

### Command Prefix
All commands use the prefix `b` (e.g., `bdrop`, `binv`, `bview`). **[TODO: Change prefix if desired]**

### Example Usage
```
bdrop          # Pull a new card
binv           # View your collection
binv 2         # View page 2 of your inventory
bview A        # View card with code "A"
bstats         # See how many of each card exist
```

_For more detailed command documentation, see the bot's help command in Discord._

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Customization

This bot is designed to be easily customizable for different themes. Here's how to adapt it:

### 1. **Change Bot Identity**
- Update bot name in `src/bot/bot.py` (currently "Bernice")
- Change command prefix (currently `b`) in the bot initialization
- Update bot status/activity message

### 2. **Customize Database Schema**
- Modify table structures in `init/1_init_tables.sql`
- Update data initialization in `init/2_init_data.sql`
- Change model classes in `src/app/models/` to match your theme

### 3. **Adapt Card System**
- Update card pool logic in `src/app/card_pool/`
- Modify character data structure for your theme (Pokemon, games, etc.)
- Change embed formatting in `src/bot/bot.py` for your card types

### 4. **Theme-Specific Features**
- Add new commands in `src/bot/commands/`
- Implement theme-specific logic (rarity systems, special events, etc.)
- Customize card images and descriptions

### 5. **Configuration**
- Update `.env` variables for your theme
- Modify Docker configuration if needed
- Change database connection settings

### Quick Theme Conversion Guide

For **[TODO: your theme]**, you'll need to:

1. **Replace character data** with **[TODO: your card/item type]**
2. **Update categories** from "anime" to **[TODO: your category]**
3. **Change card terminology** throughout the codebase
4. **Customize embed messages** for your theme
5. **Update command descriptions** and help text

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Basic gacha system with character pulls
- [x] PostgreSQL database integration
- [x] Docker containerization
- [x] Card inventory management
- [x] Statistics and circulation tracking
- [ ] **[TODO: Add theme-specific features]**
- [ ] Multi-server support enhancements
- [ ] Card trading system between users
- [ ] Rarity tiers and special events
- [ ] Web dashboard for collection management
- [ ] Admin commands for pool management

See the [open issues](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=YOUR_USERNAME/YOUR_REPO_NAME" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

**[TODO: Add your license information here]**

See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

**[TODO: Add your contact information here]**

Project Link: [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
* [AsyncPG](https://magicstack.github.io/asyncpg/) - PostgreSQL driver for asyncio
* [Python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management
* [Choose an Open Source License](https://choosealicense.com)
* [Best README Template](https://github.com/othneildrew/Best-README-Template) - Template used for this README
* **[TODO: Add theme-specific acknowledgments]**

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/YOUR_USERNAME/YOUR_REPO_NAME.svg?style=for-the-badge
[contributors-url]: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/YOUR_USERNAME/YOUR_REPO_NAME.svg?style=for-the-badge
[forks-url]: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/network/members
[stars-shield]: https://img.shields.io/github/stars/YOUR_USERNAME/YOUR_REPO_NAME.svg?style=for-the-badge
[stars-url]: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/stargazers
[issues-shield]: https://img.shields.io/github/issues/YOUR_USERNAME/YOUR_REPO_NAME.svg?style=for-the-badge
[issues-url]: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/issues
[license-shield]: https://img.shields.io/github/license/YOUR_USERNAME/YOUR_REPO_NAME.svg?style=for-the-badge
[license-url]: https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[Discord.py]: https://img.shields.io/badge/Discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white
[Discord-url]: https://discordpy.readthedocs.io/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://postgresql.org/
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://docker.com/
[AsyncPG]: https://img.shields.io/badge/AsyncPG-000000?style=for-the-badge&logo=postgresql&logoColor=white
[AsyncPG-url]: https://magicstack.github.io/asyncpg/
