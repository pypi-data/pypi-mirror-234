# FastAPI Validation

FastAPI Validation currently work with SQLAlchemy based behind, so we need to set it global when initialize

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, pool_size=50, max_overflow=100)

global_db_session: Session = sessionmaker(
    autoflush=False, autobegin=True, bind=engine, join_transaction_mode='rollback_only'
)()

def run_with_global_session(callback):
    try:
        return callback(global_db_session)
    except Exception as e:
        global_db_session.rollback()
        raise e

GlobalVariable.set('run_with_global_session', run_with_global_session)
```
