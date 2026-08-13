def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload) > 0

    for _, details in payload.items():
        assert expected_fields.issubset(details.keys())
        assert isinstance(details["participants"], list)


def test_get_activities_includes_seeded_activity(client):
    # Arrange
    seeded_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert seeded_activity in payload
