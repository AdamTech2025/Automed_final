# OpenAI Model Configuration

This application uses OpenAI's GPT models for dental code extraction. You can configure which model to use through environment variables.

## Default Configuration

By default, the application uses the **gpt-4o** model (`gpt-4o`), which provides excellent results for dental code extraction with good performance.

## Changing the Model

To change the OpenAI model used by the application:

1. Create or modify your `.env` file in the project root
2. Set the `OPENAI_MODEL` environment variable to your desired model

Example `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-turbo
```

## Supported Models

The application supports any OpenAI chat model, including:

- `gpt-4o` (default) - OpenAI's latest model with excellent performance
- `gpt-4o-turbo` - A balance of quality and cost
- `gpt-3.5-turbo` - Faster but less comprehensive than gpt-4o models

## Vercel Deployment

If deploying to Vercel, add the `OPENAI_MODEL` environment variable in your Vercel project settings.

## Advanced Configuration

The model selection is implemented in all relevant files:

- `topics/diagnostics.py`
- All files in `subtopics/diagnostics/`

When the environment variable changes, the entire application automatically adapts to use the new model without requiring code changes. 