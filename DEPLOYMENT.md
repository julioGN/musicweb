# Deployment Guide

## For Streamlit Cloud

1. **Requirements**: The app uses `requirements.txt` for dependencies
2. **Entry Point**: Use `src/musicweb/web/app.py` as the main file
3. **Python Path**: The app automatically handles Python path configuration for deployment environments

## For Local Development

1. Install in editable mode:
   ```bash
   pip install -e .
   ```

2. Run the web app:
   ```bash
   streamlit run src/musicweb/web/app.py
   ```

## For Other Deployment Platforms

The app includes fallback import logic that automatically detects deployment environments and adjusts the Python path accordingly. No additional configuration should be needed.

## Environment Detection

The app automatically:
- Tries to import the installed package first
- Falls back to adding the `src/` directory to Python path
- Handles both development and deployment scenarios seamlessly