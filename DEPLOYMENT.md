# Deployment Guide

## 🚀 For Streamlit Cloud

### Files Required
- **Entry Point**: `src/musicweb/web/app.py`
- **Dependencies**: Uses `requirements.txt`
- **Python Version**: `runtime.txt` specifies Python 3.11
- **System Packages**: `packages.txt` (empty - no system deps needed)

### Deployment Steps
1. Connect your GitHub repository to Streamlit Cloud
2. Set main file path: `src/musicweb/web/app.py`
3. The app will automatically install dependencies and run

### Alternative Requirements
- Use `requirements-streamlit.txt` for more conservative dependency versions
- Compatible with Python 3.8+ environments

## 💻 For Local Development

### Quick Start
```bash
# Install in editable mode
pip install -e .

# Run the web app
streamlit run src/musicweb/web/app.py
```

### Development Dependencies
```bash
# Install with development tools
pip install -e ".[dev,test]"
```

## 🐳 For Docker Deployment

The app can be containerized using the provided `Dockerfile`:

```bash
# Build image
docker build -t musicweb .

# Run container
docker run -p 8501:8501 musicweb
```

## 🔧 Dependency Management

### Requirements Files
- `requirements.txt` - Main production dependencies (conservative versions)
- `requirements-streamlit.txt` - Streamlit Cloud optimized
- `requirements-dev.txt` - Development dependencies
- `pyproject.toml` - Complete package specification

### Python Version Compatibility
- **Minimum**: Python 3.8
- **Recommended**: Python 3.11 (specified in `runtime.txt`)
- **Tested**: Python 3.8, 3.9, 3.10, 3.11, 3.12

### Dependency Notes
- `ytmusicapi` version constrained for Python 3.8+ compatibility
- `rapidfuzz` version range for broad compatibility
- All major dependencies have upper bounds for stability

## 📱 Mobile Deployment Considerations

### Performance
- Mobile CSS is injected efficiently
- JavaScript optimizations are minimal
- Responsive design works across all deployment platforms

### Features
- Auto-collapsing sidebar on mobile
- Touch-friendly interface
- Progressive enhancement

## 🔍 Troubleshooting

### Common Issues

#### Dependency Conflicts
- Use `requirements-streamlit.txt` for stricter compatibility
- Check Python version matches `runtime.txt`

#### Import Errors
- The app auto-detects deployment environments
- Falls back to local path resolution
- No manual configuration needed

#### Mobile Issues
- Mobile features work on all deployment platforms
- CSS is injected at runtime
- No additional mobile setup required

### Environment Detection

The app automatically:
- Detects if running in development vs deployment
- Handles Python path configuration
- Imports components with fallbacks
- Provides mobile-responsive interface

## 🌐 Supported Platforms

### Cloud Platforms
- ✅ Streamlit Cloud (recommended)
- ✅ Heroku
- ✅ Google Cloud Run
- ✅ AWS App Runner
- ✅ Azure Container Instances

### Local Environments
- ✅ Windows, macOS, Linux
- ✅ Virtual environments
- ✅ Conda environments
- ✅ Docker containers

---

The musicweb application is designed for easy deployment across multiple platforms with automatic environment detection and mobile-responsive design.