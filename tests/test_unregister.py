from src.app import activities


def test_unregister_when_student_is_registered_removes_student(client):
    # Arrange
    activity_name = "Programming Class"
    email = activities[activity_name]["participants"][0]
    before_count = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert len(activities[activity_name]["participants"]) == before_count - 1
    assert email not in activities[activity_name]["participants"]


def test_unregister_when_activity_does_not_exist_returns_404(client):
    # Arrange
    missing_activity_name = "Nonexistent Club"

    # Act
    response = client.delete(
        f"/activities/{missing_activity_name}/participants/student@mergington.edu"
    )

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload
    assert payload["detail"] == "Activity not found"


def test_unregister_when_student_not_registered_returns_404(client):
    # Arrange
    activity_name = "Gym Class"
    missing_email = "not.registered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{missing_email}")

    # Assert
    assert response.status_code == 404
    payload = response.json()
    assert "detail" in payload
    assert payload["detail"] == "Student is not signed up for this activity"
