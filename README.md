
# Route Finder App Documentation

## Overview

The Route Finder App is a full-stack application that provides users with directions and route information between two locations. It utilizes the MapQuest API for route data, a Flask backend for handling API requests, and a React frontend for user interaction.

## Backend (Flask)

### Setup

- **Dependencies**: Flask, Flask-CORS, requests, python-dotenv
- **Environment**: Requires a `.env` file with `MAPQUEST_API_KEY` set to your MapQuest API key.

### Running the Backend

Activate your virtual environment and run:

```bash
flask run
```

### Endpoints

- **POST /route**
  - **Body**: `{"origin": "start location", "destination": "end location"}`
  - **Response**: Route information including distance, estimated time, and step-by-step directions.

## Frontend (React with Vite)

### Setup

- **Dependencies**: React, Vite, TypeScript (optional)
- **Environment**: Ensure the backend Flask server is running.

### Running the Frontend

Navigate to the frontend directory and run:

```bash
npm run dev
```

### Features

- Input fields for origin and destination locations.
- Displays route details and directions upon form submission.

## Development Notes

- **CORS**: Ensure Flask-CORS is configured to allow requests from your frontend development server.
- **MapQuest API**: Ensure valid API key is set in the `.env` file for backend requests.

## Future Enhancements

- Implement additional MapQuest API features.
- Improve UI/UX design.
- Add user authentication for personalized routes.
