from datetime import date

import pytest

from vacancies.models import Vacancy


@pytest.mark.django_db
def test_vacancy_create(client, hr_token):
    expected_response = {
        "id": 1,
        "created": str(date.today()),
        "skills": [],
        "slug": "123",
        "text": "123",
        "status": "draft",
        "min_exp": None,
        "likes": 0,
        "update_at": None,
        "user": None
    }

    data = {
        "slug": "123",
        "text": "123",
        "status": "draft"
    }

    response = client.post(
        "/vacancy/create/",
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION="Token " + hr_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
