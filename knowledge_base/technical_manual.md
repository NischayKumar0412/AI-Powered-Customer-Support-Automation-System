# Technical Manual

## Installation Issues
- **Windows:** Ensure you are running Windows 10 or later. If the installer fails, try running it as an Administrator. Check that your antivirus is not blocking the executable.
- **Mac:** Our application supports macOS 11 (Big Sur) and newer. If you receive an "unidentified developer" error, go to System Preferences -> Security & Privacy and click "Open Anyway".

## Application Errors
- **File Upload Crashes:** If the application crashes when uploading a file, ensure the file is under 50MB and in a supported format (.pdf, .docx, .csv). Clear the application cache from the settings menu and try again.
- **Sync Issues:** If data is not syncing across devices, verify your internet connection. Log out and log back in to force a token refresh.

## Configuration Issues
- **SSO Setup:** To configure SAML SSO, navigate to Admin Settings -> Security. You will need your Identity Provider's metadata XML file.
- **Webhooks:** Webhooks can be configured under Developer Settings. Ensure your endpoint returns a 200 OK status within 3 seconds, or the webhook will be marked as failed.
