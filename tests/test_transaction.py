import pytest
from datetime import datetime
from application.models import Transaction, Account, User
from application.services.database import SessionLocal

@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        default_currency="USD"
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def test_accounts(db_session, test_user):
    source_account = Account(currency="USD", balance=1000.0, user_id=test_user.id)
    target_account = Account(currency="EUR", balance=500.0, user_id=test_user.id)
    db_session.add_all([source_account, target_account])
    db_session.commit()
    return source_account, target_account

def test_create_transaction(db_session, test_accounts):
    source_account, target_account = test_accounts
    
    transaction = Transaction(
        amount_numeric=100.0,
        source_account_id=source_account.id,
        target_account_id=target_account.id,
        description="Test transfer"
    )
    
    db_session.add(transaction)
    db_session.commit()
    
    saved_transaction = db_session.query(Transaction).first()
    assert saved_transaction is not None
    assert saved_transaction.amount_numeric == 100.0
    assert saved_transaction.description == "Test transfer"
    assert isinstance(saved_transaction.timestamp, datetime)

def test_transaction_description_length(db_session, test_accounts):
    source_account, target_account = test_accounts
    
    # Test with description exceeding MAX_DESC_LENGTH
    long_description = "x" * 129
    transaction = Transaction(
        amount_numeric=100.0,
        source_account_id=source_account.id,
        target_account_id=target_account.id,
        description=long_description
    )
    
    with pytest.raises(Exception):
        db_session.add(transaction)
        db_session.commit()

def test_transaction_relationships(db_session, test_accounts):
    source_account, target_account = test_accounts
    
    transaction = Transaction(
        amount_numeric=100.0,
        source_account_id=source_account.id,
        target_account_id=target_account.id,
        description="Test transfer"
    )
    
    db_session.add(transaction)
    db_session.commit()
    
    saved_transaction = db_session.query(Transaction).first()
    assert saved_transaction.source == target_account
    assert saved_transaction.target == source_account

def test_transaction_required_fields(db_session, test_accounts):
    source_account, target_account = test_accounts
    
    # Test missing required fields
    with pytest.raises(Exception):
        transaction = Transaction(
            amount_numeric=100.0,
            # Missing source_account_id
            target_account_id=target_account.id,
            description="Test transfer"
        )
        db_session.add(transaction)
        db_session.commit()

def test_transaction_amount_validation(db_session, test_accounts):
    source_account, target_account = test_accounts
    
    # Test negative amount
    with pytest.raises(Exception):
        transaction = Transaction(
            amount_numeric=-100.0,
            source_account_id=source_account.id,
            target_account_id=target_account.id,
            description="Test transfer"
        )
        db_session.add(transaction)
        db_session.commit() 