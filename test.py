# test.py

from score import score
import subprocess
import pytest
import time
import requests

@pytest.fixture
def example_text():
    return "URGENT: Exclusive Insurance Offer! Act Now to Secure Your Future! Limited Time Only: Claim Your Policy Before It's Too Late! Don't Miss Out on This Life-Saving Opportunity!"


@pytest.fixture
def example_threshold():
    return 0.5

# Function to check if the container is ready by sending a sample request
def wait_for_container_ready():
    # Retry for a maximum of 10 times
    for _ in range(10):
        try:
            # Send a sample request to the container
            response = requests.post("http://127.0.0.1:5000/score", json={"text": "sample_text", "threshold": 0.5}, timeout=15)
            # If the response status code is 200, container is ready
            if response.status_code == 200:
                print("Container is ready")
                return True
        except Exception as e:
            print(f"Error checking container status: {e}")
        # If container is not ready, retry after a delay
        print("Container is not ready yet, retrying...")
        time.sleep(30)
    # If max retries exceeded, container is not ready
    print("Max retries exceeded, container is not ready")
    return False


# Function to build the Docker image
def run_image():
    subprocess.run(["docker", "build", "-t", "spam-classifier", "."])


# Function to run the Docker container
def run_container():
    subprocess.run(["docker", "run", "-d", "-p", "5000:5000", "--name", "spam-container", "spam-classifier"])


# Function to test the Docker container
def test_docker(example_text, example_threshold):
    
    # Build Docker image
    run_image()
    
    # Wait for image to build
    time.sleep(75)
    
    # Run Docker container
    run_container()
    
    # Check if the container is ready
    if wait_for_container_ready():
        print("Test passed!")
    else:
        print("Test failed!")
    
    # Send a request to the container for testing
    payload = {'text': example_text, 'threshold': example_threshold}
    response = requests.post('http://127.0.0.1:5000/score', json=payload)
    data = response.json()
    prediction = data['prediction']
    propensity = data['propensity']
    
    # Print the test results
    print(f'Text: "{example_text}", Classified as: {"spam" if prediction else "non-spam"}, Score: {propensity}')
    
    # Stop and remove the Docker container
    subprocess.run(["docker", "stop", "spam-container"])
    subprocess.run(["docker", "rm", "spam-container"])
    subprocess.run(["docker", "rmi", "spam-classifier"])

    