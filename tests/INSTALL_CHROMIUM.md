# Installing Chromium for Selenium Tests

The Selenium tests are configured to use Chromium browser. Here are installation instructions for different platforms.

## macOS

### Option 1: Homebrew Cask (Deprecated but still works)
```bash
brew install --cask chromium
```

**Note**: Homebrew's Chromium cask is deprecated but still functional until 2026-09-01.

### Option 2: Download from Chromium.org
1. Visit: https://www.chromium.org/get-involved/download-chromium
2. Download the macOS build
3. Extract and place in `/Applications/Chromium.app`

### Option 3: Use Chrome (Chromium-based)
Chrome is Chromium-based and works identically:
- Already installed on most macOS systems
- The test configuration will automatically detect and use Chrome if Chromium is not found

## Linux

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install chromium-browser
```

### Fedora
```bash
sudo dnf install chromium
```

### Arch Linux
```bash
sudo pacman -S chromium
```

## Verify Installation

After installation, verify Chromium is available:

```bash
./tests/setup_chromium.sh
```

Or manually check:
```bash
which chromium
# or
which chromium-browser
```

## Test Configuration

The test configuration (`tests/conftest.py`) will automatically:
1. Look for Chromium in common installation paths
2. Fall back to Chrome if Chromium is not found
3. Use system default if neither is found

## Running Tests

Once Chromium (or Chrome) is installed, tests will use it automatically:

```bash
pytest tests/
```

No additional configuration needed!

