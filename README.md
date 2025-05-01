# SHL Test Recommender

A web application that helps users find relevant SHL tests based on job descriptions or search queries. The application provides intelligent recommendations by analyzing user input and matching it with a comprehensive database of SHL assessments.

## Repository Links
- Frontend Repository: [https://github.com/Maniredii/shl-assessment-frontend.git](https://github.com/Maniredii/shl-assessment-frontend.git)
- Backend Repository: [https://github.com/Maniredii/shl-assessment-backend.git](https://github.com/Maniredii/shl-assessment-backend.git)

## Solution
For a detailed explanation of the approach and implementation, refer to the SOLUTION.md file.

## Features

- Natural language search for test recommendations
- URL-based job description analysis
- Detailed test information including:
  - Test descriptions
  - Remote testing availability
  - Adaptive testing support
  - Related keywords
  - Direct links to the SHL product catalog

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install flask flask-cors requests beautifulsoup4
```

3. Start the backend server:
```bash
python app.py
```

The backend server will run on `http://127.0.0.1:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend application will run on `http://localhost:3000`

## Usage

1. Open your web browser and navigate to `http://localhost:3000`

2. You can search for test recommendations in two ways:
   - Enter a text query describing the role or skills you're looking for
   - Paste a job description URL for automatic analysis

3. Click "Get Recommendations" to see matching SHL tests

4. For each recommended test, you can:
   - View detailed information by clicking the info icon
   - Open the test in the SHL product catalog by clicking the external link icon
   - See features like remote testing availability and adaptive testing support

## API Endpoints

The backend provides the following API endpoints:

- `GET /` - Health check endpoint
- `POST /api/recommend` - Get test recommendations
  - Request body:
    ```json
    {
      "query": "string",  // Optional: Text search query
      "url": "string"     // Optional: Job description URL
    }
    ```
  - At least one of query or url must be provided

## Development

- Backend code is in `backend/app.py`
- Frontend code is in `frontend/src/`
- Main application component is in `frontend/src/App.js`
- API configuration is in `frontend/src/api.js`

## Error Handling

The application includes comprehensive error handling for:
- Network connectivity issues
- Invalid URLs
- Empty search queries
- Server errors

## Browser Support

The application is compatible with modern web browsers:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Support

If you like this project, consider buying me a coffee!

<a href="https://www.buymeacoffee.com/Manideep" target="_blank">
    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;">
</a>

## Developer

This project is developed by **MANIDEEP REDDY EEVURI**.

- [GitHub Profile](https://github.com/Maniredii)
- [LinkedIn Profile](https://www.linkedin.com/in/manideep-reddy-eevuri-661659268)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
