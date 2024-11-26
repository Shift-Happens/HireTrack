import requests
import json

def test_api():
    base_url = 'http://localhost:5000/api'
    headers = {
        'Authorization': 'Bearer test_key_123',
        'Content-Type': 'application/json'
    }
    
    # Test connection
    response = requests.get(f'{base_url}/jobs/test', headers=headers)
    print("Connection test:", response.json())
    
    # Test job creation
    test_job = {
        "company": "Test Company",
        "position": "Python Developer",
        "location": "Warsaw",
        "work_type": "Remote",
        "salary_min": 10000,
        "salary_max": 15000,
        "salary_currency": "PLN",
        "job_link": "https://example.com/job",
        "notes": "Test job from API",
        "contract_type": "UoP" 
    }
    
    response = requests.post(
        f'{base_url}/jobs',
        headers=headers,
        json=test_job
    )
    print("Job creation test:", response.json())

if __name__ == "__main__":
    test_api()