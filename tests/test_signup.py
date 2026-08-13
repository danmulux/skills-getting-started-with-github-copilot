from src.app import activities


def test_signup_when_valid_request_registers_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    before_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert len(activities[activity_name]["participants"]) == before_count + 1
    assert email in activities[activity_name]["participants"]


def test_signup_when_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    payload = response.json()
    assert "detail" in payload
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_when_activity_is_full_returns_400(client):
    # Arrange
    activity_name = "Math Olympiad"
    activity = activities[activity_name]
    activity["participants"] = [
        f"student{i}@mergington.edu" for i in range(activity["max_participants"])
    ]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "waitlist.student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    payload = response.json()
    assert "detail" in payload
    assert payload["detail"] == "Activity is full"


def test_signup_when_activity_does_not_exist_returns_404(client):
    # Arrange
    missing_activity_name = "Nonexistent Club"

    # Act
    response = client.post(
        f"/activities/{missing_activity_name}/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload
    assert payload["detail"] == "Activity not found"
