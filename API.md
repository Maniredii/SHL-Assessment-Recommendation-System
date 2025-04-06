# SHL Test Recommender API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Health Check
```http
GET /
```
Checks if the API is running.

**Response**
```json
{
    "status": "ok",
    "message": "SHL Test Recommender API is running"
}
```

### 2. Get Test Recommendations
```http
POST /api/recommend
```

Get test recommendations based on a natural language query or job description URL.

**Request Body**
```json
{
    "query": "string",  // Optional: Natural language query
    "url": "string"     // Optional: Job description URL
}
```

At least one of `query` or `url` must be provided.

**Response**
```json
{
    "recommendations": [
        {
            "name": "string",
            "url": "string",
            "description": "string",
            "remote_testing": boolean,
            "adaptive_support": boolean,
            "duration": "string",
            "test_type": "string",
            "features": [
                "string"
            ]
        }
    ],
    "message": "string"
}
```

**Example Request**
```json
{
    "query": "coding assessment for Java developers"
}
```

**Example Response**
```json
{
    "recommendations": [
        {
            "name": "SHL Coding Assessment",
            "url": "https://www.shl.com/solutions/products/coding-assessment/",
            "description": "Technical assessment for software developers testing coding skills and problem-solving",
            "remote_testing": true,
            "adaptive_support": true,
            "duration": "60 minutes",
            "test_type": "Skills",
            "features": [
                "Remote testing supported",
                "60 minutes to complete",
                "Multiple programming languages",
                "Real-world coding challenges"
            ]
        },
        {
            "name": "IT Developer Assessment",
            "url": "https://www.shl.com/solutions/products/it-developer-assessment/",
            "description": "Comprehensive assessment for software development roles",
            "remote_testing": true,
            "adaptive_support": true,
            "duration": "90 minutes",
            "test_type": "Technical",
            "features": [
                "Programming skills evaluation",
                "Problem-solving scenarios",
                "Technical knowledge assessment",
                "Code quality analysis"
            ]
        }
    ],
    "message": "Found 2 relevant tests."
}
```

## Error Responses

### 1. Bad Request (400)
```json
{
    "error": "Please provide either a query or URL"
}
```

### 2. Server Error (500)
```json
{
    "error": "An error occurred while processing your request"
}
```

## Rate Limiting

- Maximum 100 requests per hour per IP address
- Rate limit headers included in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Authentication

Currently, the API is open and does not require authentication. Future versions may implement API key authentication. 