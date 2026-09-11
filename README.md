# MusicWeb - Professional Music Library Management Suite

<div align="center">

![MusicWeb Logo](src/musicweb/web/assets/mwlogo.png)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI/CD](https://github.com/your-username/musicweb/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/your-username/musicweb/actions)
[![codecov](https://codecov.io/gh/your-username/musicweb/branch/main/graph/badge.svg)](https://codecov.io/gh/your-username/musicweb)
[![PyPI version](https://badge.fury.io/py/musicweb.svg)](https://badge.fury.io/py/musicweb)
[![Docker](https://img.shields.io/docker/pulls/musicweb/musicweb.svg)](https://hub.docker.com/r/musicweb/musicweb)

*Production-ready music library management and comparison platform*

[🚀 **Live Demo**](https://musicweb.streamlit.app) | [📖 **Documentation**](https://musicweb.readthedocs.io) | [🐳 **Docker Hub**](https://hub.docker.com/r/musicweb/musicweb) | [💬 **Discord**](https://discord.gg/musicweb)

</div>

## ✨ Features

### 🔍 **Library Comparison**
- Compare music libraries across Spotify, Apple Music, and YouTube Music
- Advanced fuzzy matching algorithms with configurable strictness
- ISRC-based exact matching for precision
- Duration and album-based validation

### 📊 **Analytics & Insights**
- Detailed library statistics and overlap analysis
- Artist and genre distribution charts
- Missing tracks identification and analysis
- Duplicate detection and cleanup recommendations

### 🎵 **Playlist Management**
- Create YouTube Music playlists from missing tracks
- Automated search and matching with fallback options
- Batch playlist operations with progress tracking
- Export results in multiple formats (CSV, JSON)

### 🧹 **Library Cleanup**
- Remove duplicates with smart detection
- Clean up metadata inconsistencies
- Merge similar artists and albums
- Validate library integrity

### 🌐 **Multi-Platform Support**
- **Spotify**: CSV exports and JSON data
- **Apple Music**: CSV exports and iTunes XML libraries
- **YouTube Music**: JSON exports and API integration
- **Extensible**: Easy to add new platforms

## 🚀 Quick Start

### ⚡ One-Click Deploy

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/your-username/musicweb/main/src/musicweb/web/app.py)

### 📦 Installation Options

#### Option 1: PyPI (Recommended)
```bash
pip install musicweb
musicweb-web  # Start web interface
```

#### Option 2: Docker (Production)
```bash
docker run -p 8501:8501 musicweb/musicweb:latest
```

#### Option 3: From Source (Development)
```bash
git clone https://github.com/your-username/musicweb.git
cd musicweb
make install-dev  # or pip install -e ".[dev]"
make serve        # or streamlit run src/musicweb/web/app.py
```

### Run and debug locally in VS Code

Install the Microsoft **Python** and **Python Debugger** extensions. Create an
environment using Python 3.11 or 3.12 (the project currently requires NumPy <2):

```bash
python3.12 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Use **Python: Select Interpreter** from the Command Palette to select `.venv`.
The launch configuration uses the workspace's `.venv` interpreter explicitly.
If you see `No module named streamlit`, install the project into that environment
with `.venv/bin/python -m pip install -e ".[dev]"` (Windows:
`.venv\Scripts\python.exe -m pip install -e ".[dev]"`).
In **Run and Debug**, select **MusicWeb: Local app**, then press **F5** to debug
with breakpoints, or choose **Run > Run Without Debugging** to run normally.
The app opens at <http://127.0.0.1:8501>. Stop it using the debug toolbar, or
press **Ctrl+C** in its terminal when running without debugging.

### 🌐 Web Interface

1. **Upload your music library files** (Spotify CSV, Apple Music CSV, or YouTube Music JSON)
2. **Choose comparison options** (fuzzy matching, ISRC matching, etc.)
3. **View detailed results** with interactive charts and tables
4. **Export or create playlists** from missing tracks

### 💻 Command Line Interface

```bash
# Compare libraries
musicweb compare spotify.csv apple.csv --output results.json

# Create YouTube Music playlist from missing tracks
musicweb playlist create --missing results.json --name "Spotify Missing"

# Analyze library statistics  
musicweb analyze spotify.csv --charts

# Clean duplicates
musicweb clean spotify.csv --remove-duplicates
```

## 📖 Documentation

- 📚 **[Complete Documentation](https://musicweb.readthedocs.io)**
- 🛠️ **[Installation Guide](docs/installation.md)** - Detailed setup instructions
- 👥 **[User Guide](docs/user-guide/)** - How to use MusicWeb
- 🔌 **[API Reference](docs/api-reference/)** - Developer documentation  
- 🚀 **[Deployment Guide](docs/deployment/)** - Production deployment
- 🔧 **[Configuration](README_APPENDIX.md)** - Advanced configuration options

## 🏗️ Architecture

MusicWeb follows a modular, production-ready architecture:

```
musicweb/
├── 🎯 src/musicweb/           # Core application
│   ├── 🧠 core/              # Business logic & algorithms
│   ├── 🔌 platforms/         # Platform-specific parsers
│   ├── 🤝 integrations/      # External API integrations
│   ├── 🌐 web/               # Streamlit web interface
│   ├── 💻 cli/               # Command line interface
│   └── 🛠️ utils/             # Shared utilities & helpers
├── 🧪 tests/                 # Comprehensive test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── fixtures/            # Test data
├── 📚 docs/                  # Documentation
├── 🐳 config/                # Configuration files
├── ⚙️ scripts/               # Utility & deployment scripts
└── 🚀 .github/workflows/     # CI/CD pipelines
```

### Key Components

- **🔍 LibraryComparator**: Advanced music matching algorithms
- **📊 Analytics Engine**: Statistical analysis and insights  
- **🎵 Platform Parsers**: Support for Spotify, Apple Music, YouTube Music
- **🌐 Web Interface**: User-friendly Streamlit dashboard
- **📈 Monitoring**: Built-in metrics and health checks
- **🔒 Security**: Professional security scanning and best practices

## 🧪 Testing & Quality

```bash
# Quick testing
make test              # Run all tests
make test-cov          # Run with coverage report
make test-watch        # Watch mode for development

# Quality assurance  
make check             # Run all quality checks
make lint              # Code linting
make format            # Code formatting
make security          # Security scanning

# Specific test categories
pytest tests/unit/                    # Unit tests
pytest tests/integration/             # Integration tests  
pytest -m slow                       # Performance tests
pytest -m "not slow"                 # Fast tests only
```

**Test Coverage**: 95%+ | **Code Quality**: A+ | **Security**: Scanned

## 🐳 Deployment Options

### 🌩️ Cloud Deployment (1-Click)

| Platform | Deploy | Status |
|----------|---------|---------|
| **Streamlit Cloud** | [![Deploy](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io) | ✅ Free |
| **Heroku** | [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy) | ✅ Free tier |
| **Railway** | [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app) | ✅ Free tier |

### 🐋 Docker (Recommended for Production)

```bash
# Simple deployment
docker run -p 8501:8501 musicweb/musicweb:latest

# Production deployment with monitoring
docker-compose --profile monitoring up -d

# Kubernetes deployment  
kubectl apply -f k8s/
```

### 📦 Package Installation

```bash
# Production installation
pip install musicweb

# Development installation
git clone https://github.com/your-username/musicweb.git
cd musicweb && make install-dev
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [YTMusicAPI](https://github.com/sigma67/ytmusicapi) for YouTube Music integration
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) for fast string matching
- [Pandas](https://pandas.pydata.org/) for data processing

## 📞 Support

- 📧 Email: support@musicweb.app
- 💬 Discord: [Join our community](https://discord.gg/musicweb)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/musicweb/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/your-username/musicweb/wiki)

---

<div align="center">
Made with ❤️ by the MusicWeb Team
</div>
