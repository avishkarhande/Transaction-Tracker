# Push Notification System

A Python-based push notification system that polls Google Sheets for new email data and processes it through a FastAPI backend. The system extracts payment details from email bodies and stores them in a SQLite database.

## 🏗️ Architecture

This project consists of two main components:

1. **Polling Service** (`poll.py`) - Continuously polls a Google Sheet for new email data
2. **FastAPI Backend** (`app/`) - REST API that receives and stores the processed data

### Data Flow

```
Google Sheet → poll.py → FastAPI Backend → SQLite Database
```

## 📁 Project Structure

```
push-notification/
├── poll.py              # Main polling script
├── requirements.txt      # Python dependencies
├── data.db              # SQLite database
├── README.md            # This file
└── app/                 # FastAPI application
    ├── main.py          # FastAPI routes and server
    ├── models.py        # SQLAlchemy database models
    ├── schemas.py       # Pydantic data schemas
    └── database.py      # Database configuration
```

## 🚀 Features

- **Real-time Polling**: Continuously monitors Google Sheets for new data
- **Email Processing**: Extracts payment details (amount, date, VPA) from email bodies
- **Data Storage**: Stores processed data in SQLite database
- **REST API**: FastAPI backend for data ingestion and retrieval
- **Data Validation**: Pydantic schemas ensure data integrity

## 📋 Prerequisites

- Python 3.7+
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd push-notification
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🧹 Code Quality & Linting

This project uses several tools to maintain code quality:

### Linters & Formatters

- **Black**: Code formatter for consistent Python code style
- **isort**: Import sorter to organize imports
- **Flake8**: Style guide enforcement
- **MyPy**: Static type checking

### Quick Commands

```bash
# Install linting dependencies
make install

# Format code (Black + isort)
make format

# Run style checks (Flake8)
make lint

# Run type checking (MyPy)
make type-check

# Run all checks
make check-all

# Or use the Python script
python lint.py
```

### Configuration Files

- `setup.cfg`: Flake8 configuration
- `pyproject.toml`: Black and isort configuration
- `mypy.ini`: MyPy type checking configuration

## ⚙️ Configuration

Before running the application, you need to configure the following in `poll.py`:

1. **Google Sheet URL**: Replace `URL = "URL FOR GOOGLE SHEET"` with your actual Google Sheet URL
2. **Target Email**: Replace `"EMAIL TO BE CHECKED"` with the email address you want to monitor
3. **API URL**: The default is `"http://127.0.0.1:8000/push"` - change if needed

## 🏃‍♂️ Usage

### 1. Start the FastAPI Backend

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Start the Polling Service

In a separate terminal:

```bash
python poll.py
```

The polling service will:
- Check for new rows every 10 seconds (configurable via `POLL_INTERVAL`)
- Process emails and extract payment details
- Send data to the FastAPI backend

## 📊 API Endpoints

### POST `/push`
Receives and stores polled data.

**Request Body:**
```json
{
  "timestamp": "2024-01-01T10:00:00",
  "email": "user@example.com",
  "name": "User Name",
  "subject": "Email Subject",
  "body": "Email body content",
  "status": "processed",
  "amount": "30.00",
  "date": "2024-01-01",
  "vpa": "user@bank"
}
```

### POST `/get_all_records`
Retrieves all stored records from the database.

### GET `/`
Health check endpoint.

## 🔍 Data Processing

The system automatically extracts the following information from email bodies:

- **Amount**: Extracts payment amounts in format "Rs.XX.XX"
- **Date**: Extracts dates in DD-MM-YY format
- **VPA**: Extracts Virtual Payment Addresses (format: user@bank)

### Example Email Processing

**Input Email Body:**
```
Payment received: Rs.30.00 on 15-12-24 from gametheory.96169739@hdfcbank
```

**Extracted Data:**
```json
{
  "amount": "30.00",
  "date": "2024-12-15",
  "vpa": "gametheory.96169739@hdfcbank"
}
```

## 🗄️ Database Schema

The `polled_data` table stores:

| Column    | Type      | Description                    |
|-----------|-----------|--------------------------------|
| id        | Integer   | Primary key                    |
| timestamp | DateTime  | Email timestamp                |
| email     | String    | Sender email address           |
| name      | String    | Sender name                    |
| subject   | String    | Email subject                  |
| body      | String    | Email body content             |
| status    | String    | Processing status              |
| amount    | String    | Extracted payment amount       |
| date      | Date      | Extracted payment date         |
| vpa       | String    | Virtual Payment Address        |

## 🔧 Customization

### Polling Interval
Change the polling frequency by modifying `POLL_INTERVAL` in `poll.py`:

```python
POLL_INTERVAL = 30  # Poll every 30 seconds
```

### Email Filtering
Modify the email filtering logic in `poll.py`:

```python
if parsed["email"] == "your-target-email@domain.com":
    # Process specific email
```

### Data Extraction
Customize the `extract_details_from_body()` function to match your email format.

## 🐛 Troubleshooting

### Common Issues

1. **Connection Error**: Ensure the FastAPI server is running before starting the polling service
2. **Google Sheet Access**: Verify the Google Sheet URL is accessible and contains the expected data format
3. **Database Errors**: Check that the `data.db` file has proper write permissions

### Logs

The polling service provides detailed logs:
- New row detection
- Data processing steps
- API call results
- Error messages

## 📦 Dependencies

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Requests**: HTTP library for API calls
- **Uvicorn**: ASGI server for FastAPI
- **Python-dotenv**: Environment variable management
- **Schedule**: Task scheduling (if needed)
- **PyWhatKit**: Additional utilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions, please open an issue in the repository or contact the development team. 