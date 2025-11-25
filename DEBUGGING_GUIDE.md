# Debugging Guide

## Visible Debug Output

I've added a **visible debug panel** on the page that will show:
- When the page loads
- When buttons are clicked
- When files are selected
- Upload progress
- Any errors

The debug panel appears **below the upload area** and will automatically show messages.

## How to Test

1. **Refresh the page** (hard refresh: Cmd+Shift+R or Ctrl+Shift+R)
2. Look for the **"Debug Output"** panel below the upload section
3. Click "Choose File" - you should see debug messages
4. Select a file - you should see file selection messages

## What to Check

### If Debug Panel Doesn't Appear:
- Check browser console (F12) for JavaScript errors
- Verify JavaScript files are loading (Network tab)
- Check if Flask app is running

### If Nothing Happens When Clicking "Choose File":
- Check debug panel for error messages
- Check browser console for errors
- Verify the button click is being registered

### If File Selection Doesn't Work:
- Check debug panel for file selection messages
- Verify file is MP4 format
- Check browser console for upload errors

## Browser Console

Open browser console (F12 or Cmd+Option+I) to see:
- Detailed logging
- JavaScript errors
- Network requests
- Response details

## Server Logs

Check the terminal where Flask is running for:
- Upload request logs
- File processing logs
- Error messages

## Common Issues

1. **JavaScript not loading**: Check Network tab, verify files exist
2. **CORS errors**: Check nginx configuration
3. **File too large**: Check nginx `client_max_body_size` setting
4. **404 errors**: Verify Flask app is running on port 5000

