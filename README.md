# Automated Investment Advisor 2025

A modern web application for managing personal finances, investments, and multi-currency accounts. Built with Python, SQLAlchemy, and NiceGUI.

## 🌟 Features

- **Multi-Currency Account Management**

  - Create and manage accounts in different currencies
  - Real-time balance tracking
  - Currency conversion support

- **Transaction Management**

  - Secure money transfers between accounts
  - Transaction history
  - Detailed transaction descriptions

- **User Authentication**

  - Secure login system
  - User registration
  - Password protection

- **Modern UI**
  - Clean and intuitive interface
  - Responsive design
  - Real-time updates

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Automated_Investment_Advisor_2025.git
cd Automated_Investment_Advisor_2025
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv local_env
local_env\Scripts\activate

# Linux/Mac
python3 -m venv local_env
source local_env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:

```env
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key-here
```

5. Initialize the database:

```bash
python -m alembic upgrade head
```

### Running the Application

1. Start the application:

```bash
python run.py
```

2. Access the application:
   Open your web browser and navigate to `http://localhost:8080`

### Docker Deployment

1. Build the Docker image:

```bash
docker build -t investment-advisor .
```

2. Run the container:

```bash
docker-compose up -d
```

## 🏗️ Project Structure

```
Automated_Investment_Advisor_2025/
├── application/
│   ├── views/           # UI components and pages
│   ├── components/      # Reusable UI components
│   ├── services/        # Business logic and services
│   ├── utils/          # Utility functions
│   ├── models.py       # Database models
│   └── auth.py         # Authentication logic
├── alembic/            # Database migrations
├── tests/              # Test files
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker configuration
└── README.md          # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
pytest tests/

# Run tests with coverage
pytest --cov=application tests/
```

## 🔒 Security Features

- Password hashing
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure session management

## 📱 Application Views

### Login Page

![Login Page](docs/images/login.png)
_Secure login interface with email and password authentication_

### Dashboard

![Dashboard](docs/images/dashboard.png)
_Main dashboard showing account overview and recent transactions_

### Account Management

![Accounts](docs/images/accounts.png)
_Multi-currency account management interface_

### Transaction History

![Transactions](docs/images/transactions.png)
_Detailed transaction history with filtering options_

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- NiceGUI for the amazing UI framework
- SQLAlchemy for robust database management
- All contributors who have helped shape this project
