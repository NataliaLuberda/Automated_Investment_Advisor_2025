import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.models import Base, User, Account
from application.account import (
    create_account,
    delete_account,
    update_account_balance,
    update_default_account_currency,
    get_user_accounts
)
from application.session import set_logged_user_email

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

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

def test_create_account_success(db_session, test_user):
    set_logged_user_email(test_user.email)
    result = create_account("EUR", 100.0)
    assert "✅ Dodano konto" in result
    
    account = db_session.query(Account).filter_by(
        user_id=test_user.id,
        currency="EUR"
    ).first()
    assert account is not None
    assert account.balance == 100.0

def test_create_account_duplicate(db_session, test_user):
    set_logged_user_email(test_user.email)
    create_account("EUR", 100.0)
    result = create_account("EUR", 200.0)
    assert "⚠️ Konto w tej walucie już istnieje" in result

def test_create_account_not_logged_in():
    set_logged_user_email(None)
    result = create_account("EUR", 100.0)
    assert "❌ Użytkownik niezalogowany" in result

def test_delete_account_success(db_session, test_user):
    set_logged_user_email(test_user.email)
    account = Account(currency="EUR", balance=0.0, user_id=test_user.id)
    db_session.add(account)
    db_session.commit()
    
    result = delete_account(account.id)
    assert "✅ Usunięto konto" in result
    
    deleted_account = db_session.query(Account).filter_by(id=account.id).first()
    assert deleted_account is None

def test_delete_account_with_balance(db_session, test_user):
    set_logged_user_email(test_user.email)
    account = Account(currency="EUR", balance=100.0, user_id=test_user.id)
    db_session.add(account)
    db_session.commit()
    
    with pytest.raises(Exception) as exc_info:
        delete_account(account.id)
    assert "❌ Konto zawiera środki" in str(exc_info.value)

def test_update_account_balance(db_session, test_user):
    set_logged_user_email(test_user.email)
    account = Account(currency="EUR", balance=100.0, user_id=test_user.id)
    db_session.add(account)
    db_session.commit()
    
    result = update_account_balance(account.id, 200.0)
    assert "✏️ Zaktualizowano saldo" in result
    
    updated_account = db_session.query(Account).filter_by(id=account.id).first()
    assert updated_account.balance == 200.0

def test_update_default_currency(db_session, test_user):
    set_logged_user_email(test_user.email)
    result = update_default_account_currency("EUR")
    assert "✏️ Zaktualizowano konto domyślne" in result
    
    updated_user = db_session.query(User).filter_by(id=test_user.id).first()
    assert updated_user.default_currency == "EUR"

def test_get_user_accounts(db_session, test_user):
    set_logged_user_email(test_user.email)
    account1 = Account(currency="EUR", balance=100.0, user_id=test_user.id)
    account2 = Account(currency="USD", balance=200.0, user_id=test_user.id)
    db_session.add_all([account1, account2])
    db_session.commit()
    
    accounts = get_user_accounts()
    assert len(accounts) == 2
    assert any(acc.currency == "EUR" and acc.balance == 100.0 for acc in accounts)
    assert any(acc.currency == "USD" and acc.balance == 200.0 for acc in accounts) 