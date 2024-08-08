# FastHTML L402 Marketplace

Welcome to the FastHTML L402 Marketplace project! This project demonstrates a working marketplace with L402 payments, built using FastHTML and deployed on Replit.

## Quick Start

1. **Fork the Repl:** Click the "Fork" button at the top right of the Replit interface to create your own copy.

2. **Set Up Fewsats Invoice Provider:**
   - Sign up at [app.fewsats.com](https://app.fewsats.com)
   - Create an API Key
   - Set the API Key:
     - Option A: Export the environment variable `FEWSATS_API_KEY`
     - Option B: Pass the API key directly in the code:
       ```python
       fewsats_provider = FewsatsInvoiceProvider(api_key="your_api_key_here")
       ```

3. **Configure Database and Storage:**
   - The project uses SQLite by default, with the option to use PostgreSQL.
   - For storage, local file storage is used by default.
   - To use PostgreSQL, set the `DATABASE_URL` environment variable.

4. **Run the Server:** Click the "Run" button in Replit to start the server.

## Project Overview

This marketplace allows users to:
- Upload items for sale (including title, description, price, cover image, and file)
- View a gallery of items
- Download items using L402 payments

## Project Structure

The project is organized into several key files:

### main.py
The main application file that sets up the FastHTML app, routes, and handles the core functionality of the marketplace.

Key components:
- FastHTML app setup with CORS middleware
- Database and storage initialization
- L402 authentication setup
- Route handlers for the main page, file uploads, and downloads

### store.py
Handles database operations and defines the Item model.

Key components:
- `Item` dataclass definition
- Database connection and table creation
- CRUD operations for items

### storage.py
Defines the storage interface and implementations for file handling.

Key components:
- `StorageInterface` abstract base class
- `LocalFileStorage` implementation for local file storage
- `ReplitObjectStorage` implementation for Replit's object storage

### credentials.py
Implements the MacaroonService for L402 authentication.

Key components:
- `FastSQLMacaroonService` class for storing and retrieving authentication tokens

## Key Features

- FastHTML for rapid prototyping and deployment
- L402 payment integration using Fewsats
- Flexible database support (SQLite and PostgreSQL)
- Versatile storage options (Local file storage and Replit object storage)
- File upload handling for cover images and item files
- HTMX for dynamic content updates

## Understanding the Code

### Main Components

- `FastHTML` app setup with CORS middleware
- Database abstraction for storing item information
- Storage abstraction for handling file uploads
- L402 authentication for protected downloads

### Key Endpoints

- `/`: Main page with item gallery and upload form
- `/download/{id}`: L402-protected endpoint for file downloads

## Deployment

The project is automatically deployed on Replit. Your deployment URL will be in the format:

`https://your-repl-name.your-username.repl.co`

## Testing L402 Payments

1. Navigate to an item's download link
2. The L402 challenge will be presented
3. Use a compatible wallet (e.g., [Hub](https://paywithhub.com)) to complete the payment
4. Access the downloaded file

## Customization

### Database Selection
To switch between SQLite and PostgreSQL, update the `get_database()` function in the database file. Both options work out of the box, but make sure to set up the necessary environment variables for PostgreSQL if you choose that option.

### Storage Selection
To switch between local file storage and Replit object storage, update the `get_storage()` function in the storage file. Both options are ready to use, with Replit object storage being particularly useful for deployed applications.

## Future Improvements

- Implement user authentication
- Enhance styling and UI/UX
- Allow to use credentials to download in the marketplace

## Acknowledgements

- [FastHTML](https://github.com/AnswerDotAI/fasthtml) by Answer.ai
- [L402-python](https://github.com/Fewsats/L402-python) by Fewsats
- [Replit](https://replit.com) for hosting and easy deployment
- [Repo on Github](https://github.com/Fewsats/fasthtml-marketplace)

## License

[MIT License](LICENSE)