# Fixing Chromium Gatekeeper Issue on macOS

## Problem
macOS Gatekeeper blocks Chromium because it doesn't have a valid signature. This is why Homebrew's Chromium cask is deprecated.

## Solution 1: Remove Quarantine Attribute (Quick Fix)

Run this command:
```bash
xattr -d com.apple.quarantine /Applications/Chromium.app
```

If that doesn't work, try:
```bash
sudo xattr -rd com.apple.quarantine /Applications/Chromium.app
```

## Solution 2: Use Chrome Instead (Recommended)

Chrome is Chromium-based and works identically for Selenium tests. The test configuration will automatically use Chrome if Chromium is not available.

**Chrome is already installed on most macOS systems.** The tests will automatically detect and use it.

## Solution 3: Allow Chromium in System Settings

1. Open **System Settings** (or System Preferences on older macOS)
2. Go to **Privacy & Security**
3. Scroll down to find the blocked Chromium message
4. Click **"Open Anyway"** or **"Allow"**

## Verify Installation

After fixing, verify Chromium works:
```bash
/Applications/Chromium.app/Contents/MacOS/Chromium --version
```

Or test with Selenium:
```bash
cd tests
pytest test_homepage.py::TestHomepage::test_homepage_loads -v
```

## Note

The test configuration has been updated to automatically fall back to Chrome if Chromium has issues. Chrome works perfectly for Selenium testing since it's based on Chromium.

