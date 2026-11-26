import pandas as pd
import pytest

from src.validation import validate_data


@pytest.fixture
def valid_sales():

    return pd.DataFrame({
        "Quantity": [2, 4],
        "UnitPrice": [10.0, 5.0],
        "IsCancellation": [False, False],
        "InvoiceDate": pd.to_datetime(
            ["2011-01-01", "2011-01-02"]
        ),
        "CustomerID": [12345, 12346],
        "Revenue": [20.0, 20.0]
    })


def test_valid_data(valid_sales):

    assert validate_data(valid_sales, valid_sales.copy()) is True


def test_empty_dataset(valid_sales):

    with pytest.raises(ValueError):
        validate_data(pd.DataFrame(), valid_sales)


def test_invalid_quantity(valid_sales):

    valid_sales.loc[0, "Quantity"] = -1

    with pytest.raises(ValueError):
        validate_data(valid_sales, valid_sales.copy())


def test_invalid_price(valid_sales):

    valid_sales.loc[0, "UnitPrice"] = 0

    with pytest.raises(ValueError):
        validate_data(valid_sales, valid_sales.copy())


def test_cancelled_invoice(valid_sales):

    valid_sales.loc[0, "IsCancellation"] = True

    with pytest.raises(ValueError):
        validate_data(valid_sales, valid_sales.copy())


def test_missing_date(valid_sales):

    valid_sales.loc[0, "InvoiceDate"] = pd.NaT

    with pytest.raises(ValueError):
        validate_data(valid_sales, valid_sales.copy())


def test_missing_customer_id(valid_sales):

    customers = valid_sales.copy()
    customers.loc[0, "CustomerID"] = None

    with pytest.raises(ValueError):
        validate_data(valid_sales, customers)


def test_invalid_revenue(valid_sales):

    valid_sales.loc[0, "Revenue"] = -20

    with pytest.raises(ValueError):
        validate_data(valid_sales, valid_sales.copy())