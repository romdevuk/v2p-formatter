# Troubleshooting File Upload Issue

## Current Problem
Nothing happens when clicking "Choose File" button.

## Debugging Steps

### 1. Check if Flask App is Running
```bash
curl http://localhost:5000/v2p-formatter/
```
Should return HTML. If not, start Flask:
```bash
cd /Users/rom/Documents/nvq/apps/v2p-formatter
source venv/bin/activate
python run.py
```

### 2. Check Browser Console
1. Open browser (F12 or Cmd+Option+I)
2. Go to Console tab
3. Look for:
   - JavaScript errors (red messages)
   - Debug messages starting with `[DEBUG]`
   - Any messages about file input

### 3. Check Debug Panel
The debug panel should be visible below the upload area. It shows:
- When page loads
- When button is clicked
- When file is selected
- Any errors

### 4. Test File Input Directly
In browser console, try:
```javascript
document.getElementById('videoInput').click()
```
This should open file dialog. If it doesn't, there's a browser security issue.

### 5. Check Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Click "Choose File" and select a file
4. Look for:
   - POST request to `/v2p-formatter/upload`
   - Any failed requests (red)
   - Response status codes

### 6. Common Issues

**Issue: No debug messages appear**
- JavaScript might not be loading
- Check Network tab for 404 errors on JS files
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

**Issue: Button click works but file dialog doesn't open**
- Browser security restriction
- Try different browser
- Check browser console for security errors

**Issue: File selected but upload doesn't start**
- Check Network tab for upload request
- Check server logs for errors
- Verify file is MP4 format

**Issue: Upload starts but fails**
- Check server terminal for error messages
- Check Network tab for response status
- Verify file size isn't too large

## Quick Test

Open browser console and run:
```javascript
// Test 1: Check if elements exist
console.log('Input:', document.getElementById('videoInput'));
console.log('Button:', document.getElementById('chooseFileBtn'));

// Test 2: Try to trigger file input
document.getElementById('videoInput').click();

// Test 3: Check if debugOutput function exists
console.log('debugOutput:', typeof debugOutput);
```

## Still Not Working?

1. **Hard refresh the page** (Cmd+Shift+R)
2. **Clear browser cache**
3. **Check browser console for errors**
4. **Try a different browser**
5. **Check Flask app is running and accessible**

