import pytest
from sqlalchemy.orm import Session
from app.models.calculation import Calculation
from app.models.user import User # Assuming you have a User model
from app.schemas.calculation import CalculationRead

def test_create_and_read_calculation(db_session: Session):

    test_user = User(username="testuser", email="test@example.com", hashed_password="abc")
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    new_calc = Calculation(
        a=100,
        b=25,
        type="divide",
        user_id=test_user.id
    )
    db_session.add(new_calc)
    db_session.commit()
    db_session.refresh(new_calc)


    assert new_calc.id is not None
    assert new_calc.a == 100
    assert new_calc.b == 25
    assert new_calc.type == "divide"
    assert new_calc.owner.username == "testuser"

    calc_read_schema = CalculationRead.from_orm(new_calc)
    assert calc_read_schema.id == new_calc.id
    assert calc_read_schema.result == 4.0 