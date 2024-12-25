# HTML Page Translator

A lightweight, efficient service that provides on-the-fly HTML page translation using Google Translate API. This project allows you to selectively translate specific HTML elements while preserving the original structure and styling of your web pages.

## Features

- **Selective Tag Translation**: Choose which HTML elements to translate (e.g., headings, paragraphs, links)
- **Async Translation**: Utilizes asynchronous requests for improved performance
- **Caching System**: Implements LRU caching to avoid redundant translations
- **Language Support**: Supports all languages available through Google Translate
- **Original File Preservation**: Maintains the original HTML structure and only modifies text content
- **Fault Tolerance**: Includes error handling and logging for reliable operation

## Installation & Setup

You have two options for running this service:

### Option 1: Using Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed on your system
2. Clone the repository
3. Start the service:
```bash
docker-compose up
```

That's it! The service will be available at `http://localhost:80`

### Option 2: Local Python Installation

1. Clone the repository
2. Install dependencies using pip:
```bash
pip install -r requirements.txt
```
3. Start the server:
```bash
python serve.py
```

## Usage

1. Place your HTML files in the `pages` directory

2. Access your translated pages:
```
http://localhost:80/your-page.html?lang=es&tags=title,h1,p
```

### URL Parameters

- `lang`: Target language code (default: 'hi' for Hindi)
  - Example: `lang=es` for Spanish, `lang=fr` for French
- `tags`: Comma-separated list of HTML tags to translate (default: title,h1,h2,a)
  - Example: `tags=p,h1,title,span`

### Example

To translate only the headings and paragraphs of `about.html` to Spanish:
```
http://localhost:80/about.html?lang=es&tags=h1,h2,h3,p
```

## Configuration

The service runs with these default settings:
- Port: 80
- Host: 0.0.0.0
- Default language: Hindi (hi)
- Default tags: title, h1, h2, a

## Error Handling

The service includes comprehensive error handling:
- Falls back to serving the original file if translation fails
- Logs errors with detailed information
- Skips empty elements and failed translations
- Maintains page functionality even if some translations fail

## Limitations

- Relies on the free tier of Google Translate API
- May have rate limiting based on Google's policies
- Cached translations persist only during runtime

## Contributing

Feel free to open issues or submit pull requests with improvements. Some areas that could use enhancement:
- Persistent caching system
- Additional translation service providers
- Custom rate limiting
- Translation quality validation

## License

This project is open source and available under the MIT License.
