# Automated_Investment_Advisor_2025

**Automated Investment Advisor** is a full-stack fintech web application built with [NiceGUI](https://nicegui.io/) and MySQL. The project replicates core digital banking features such as user registration, money transfers, balance overview — all within a modern and intuitive UI. It replicates key digital banking functionalities such as user authentication, real-time account dashboards, transaction histories, and peer-to-peer transfers.

## 📌 Features

- 🔐 Secure user registration and login
- 💰 Account dashboard with real-time balance updates
- 📊 Transaction history with detailed views
- 🔄 Instant money transfers between users
- 💱 Simple currency exchange functionality
- 🖥️ Responsive and interactive UI via NiceGUI

## 🛠️ Tech Stack

- **Frontend & Backend**: [NiceGUI](https://nicegui.io/)
- **Language**: Python 3.11+
- **Database**: MySQL
- **Deployment**: Docker
- **ORM / DB Migrations**: SQLAlchemy & Alembic

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NataliaLuberda/Automated_Investment_Advisor_2025.git
cd Automated_Investment_Advisor_2025
```

### 2. Set Up with Docker (Recommended)

```bash
docker-compose up --build
```
Access the app at: http://localhost:8080 (or the port configured in docker-compose.yml)


### 3. Manual Setup (Without Docker)
Make sure you have MySQL running locally and configure config.py accordingly.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head  # Run DB migrations
python run.py
```


⚙️Configuration
   - config.py: Main application settings
   - env (optional): Environment-specific variables
   - alembic.ini: Alembic migration config
   - docker-compose.yml: Service definitions


📂 Project Structure

```bash
Automated_Investment_Advisor_2025/
├── run.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic/
├── app/                
│   └── ...
└── README.md
```



## 🧭 User Interface Overview

Here's a breakdown of the main pages visible to authenticated users within the application:

### 🔐 Login / Registration Page
- **Purpose**: Allow users to securely sign up or log in.
- **Main Features**:
  - Email and password authentication
  - Basic form validation
  - Redirects to the dashboard upon success

 ![image](https://github.com/user-attachments/assets/0f0b6023-4548-4008-bc92-9b58033272c9)


### 🏠 Dashboard
- **Purpose**: Serve as the user's main landing page.
- **Main Features**:
  - Display current account balance
  - Widgets with tips
  - Navigation to transfers and history
  - Ability of changing current account

![image](https://github.com/user-attachments/assets/60f1810b-5c79-4b8c-b710-9640166ebef0)



### 💸 Money Transfer Page
- **Purpose**: Send money to another registered user.
- **Main Features**:
  - Form to enter transfer amount
  - Validation of balance and recipient details
  - Displays confirmation on success
  - Transactions history

![image](https://github.com/user-attachments/assets/62abab6a-7034-482c-a1fa-fd8613d2e38f)


### 📜 Transaction History Page
- **Purpose**: View detailed logs of past transactions.
- **Main Features**:
  - Table view of sent and received transactions
  - Filters for date, type, or amount
  - Access to full details of each transaction
  - Ability of exporting .csv file with transactions history

 ![image](https://github.com/user-attachments/assets/80d01d72-5563-4117-b2ba-003a92d30178)
 ![image](https://github.com/user-attachments/assets/2d7ad08d-101d-46b0-a5ac-7c887f849907)


### 🧾 Account Page
- **Purpose**: View detailed information about the user's account.
- **Main Features**:
  - Shows current account balance
  - Ability of adding account, exchanging money

![image](https://github.com/user-attachments/assets/813e0297-854f-4859-9675-f347dc3e67a6)


