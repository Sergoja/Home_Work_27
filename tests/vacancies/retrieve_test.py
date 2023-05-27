from datetime import date

import pytest


@pytest.mark.django_db
def test_retrieve_vacancy(client, vacancy, hr_token):
    expected_response = {
        "id": vacancy.pk,
        "created": str(date.today()),
        "skills": [],
        "slug": "test",
        "username": vacancy.username,
        "text": "test text",
        "status": "draft",
        "min_exp": None,
        "likes": 0,
        "update_at": None,
        "user": vacancy.user_id
    }

    response = client.get(
        f"/vacancy/{vacancy.pk}",
        HTTP_AUTHORIZATION="Token " + hr_token
    )

    assert response.status_code == 200
    assert response.data == expected_response
