# FastHTML L402 Marketplace

Welcome to the FastHTML L402 Marketplace project! This project demonstrates a working marketplace with L402 payments, built using FastHTML and deployed on Replit.

## Quick Start

1. **Clone the Repository:** 
   ```
   git clone https://github.com/Fewsats/fasthtml-marketplace.git
   cd fasthtml-marketplace/00_market_full_example
   ```

2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Set Up Fewsats Invoice Provider:**
   - Sign up at [app.fewsats.com](https://app.fewsats.com)
   - Create an API Key
   - Set the API Key:
     - Option A: Export the environment variable `FEWSATS_API_KEY`
     - Option B: Pass the API key directly in the code:
       ```python
       fewsats_provider = FewsatsInvoiceProvider(api_key="your_api_key_here")
       ```

4. **Run the Server:** 
   ```
   python main.py
   ```

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

### storage.py
Defines the storage interface and implementations for file handling.

Key components:
- `StorageInterface` abstract base class
- `LocalFileStorage` implementation for local file storage
- `ReplitObjectStorage` implementation for Replit's object storage

## Key Features

- FastHTML for rapid prototyping and deployment
- L402 payment integration using Fewsats
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
- `/upload`: Handles file uploads for new items
- `/items`: Returns a list of all items in the marketplace
- `/item/{id}`: Displays details for a specific item
- `/download/{id}`: L402-protected endpoint for file downloads
- `/l402/{id}`: Generates L402 invoice for a specific item
- `/verify/{id}`: Verifies L402 payment and provides download link

## Deployment

The project is automatically deployed on Replit. Your deployment URL will be in the format:

`https://your-repl-name.your-username.repl.co`

## Testing L402 Payments

1. Navigate to an item
2. Click Pay with [Hub](https://paywithhub.com)) 
3. This will open a new tab with the payment details and the invoice (doesn't work with localhost links)
3. Copy credentials back to marketplace & download the file

### Storage Selection
To switch between local file storage and Replit object storage, update the `get_storage()` function in the storage file. Both options are ready to use, with Replit object storage being particularly useful for deployed applications.

## Acknowledgements

- [FastHTML](https://github.com/AnswerDotAI/fasthtml) by Answer.ai
- [L402-python](https://github.com/Fewsats/L402-python) by Fewsats
- [Replit](https://replit.com) for hosting and easy deployment
- [Repo on Github](https://github.com/Fewsats/fasthtml-marketplace)

## License

[MIT License](LICENSE)