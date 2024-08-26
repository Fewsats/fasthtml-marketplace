# FastHTML L402 Marketplace (React Port)

A working marketplace with L402 payments, built using FastHTML. It is a port of the [Fewsats Marketplace](https://marketplace.fewsats.com) built in React.

## Comparison with React Version

- **Lines of Code**: Reduced by 74% (3.5k to 900)
- **Number of Files**: Reduced by 71% (32 to 9)
- **Deployment**: Both easy (Vercel for React, Replit for FastHTML)
- **Structure**: Simpler structure with less boilerplate
- **Components**: Plain Python functions, easier to read and use than TSX

## Performance Comparison

Based on PageSpeed Insights:
- FastHTML version slightly outperforms React in overall performance
- React version has slightly better accessibility and SEO scores


## Quick Start

1. Clone and navigate to the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Fewsats API Key
4. Run: `python main.py`

## Key Features

- Create a personally-branded marketplace by filtering items with your userID
- Upload and sell digital items
- L402 payment integration
- HTMX for dynamic updates


## Endpoints


## Testing L402 Payments

1. Select an item
2. Pay with [Hub](https://paywithhub.com)
3. Copy credentials and download

Run locally at `http://localhost:8000`