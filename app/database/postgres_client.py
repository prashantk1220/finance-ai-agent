
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import (
    Index, create_engine, Column, Integer, String, Date, Numeric, BigInteger, UniqueConstraint, text
)

from app.settings import DATABASE_URL


Base = declarative_base()


# StockData parent table (partitioned)
class StockData(Base):
    __tablename__ = "stock_data"

    data_id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    trade_date = Column(Date, nullable=False)
    open_price = Column(Numeric(12, 4))
    high_price = Column(Numeric(12, 4))
    low_price = Column(Numeric(12, 4))
    close_price = Column(Numeric(12, 4))
    volume = Column(BigInteger)

    # Add index and unique constraint
    __table_args__ = (
        Index('ix_stock_data_ticker', 'ticker'),  # Index named 'ix_stock_data_ticker' on the 'ticker' column
        UniqueConstraint('ticker', 'trade_date', name='_ticker_date_uc'),
    )


def create_partition(engine, partition_name: str, ticker: str):
    """
    Create a partition for a specific ticker
    to dynamically to scale the Database, if required
    """
    partition_query = text(f"""
    CREATE TABLE IF NOT EXISTS {partition_name}
    PARTITION OF stock_data
    FOR VALUES IN ({ticker});
    """)
    with engine.connect() as connection:
        connection.execute(partition_query)


def setup_database():
    """Create the tables and setup partitions"""
    engine = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine)

    # create_partition(engine, "stock_data_aapl", "AAPL")  # Not required in this scope

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Initialize session factory once
SessionFactory = setup_database()


# Dependecies used by FastAPI
def get_db():
    """Function to get a new session from the session factory
    while maintaing the context"""
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


def get_stock_data_by_ticker(ticker: str):
    """Query using SQLAlchemy ORM"""
    session = next(get_db())
    try:
        stock_data = session.query(StockData).filter(StockData.ticker == ticker).all()
        return stock_data
    finally:
        session.close()


# ans = get_stock_data_by_ticker("AAPL")
