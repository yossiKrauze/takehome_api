# Take home assignment
You’re building a simplified version of a virtual dermatology clinic. Patients can book appointments, and the system should assign them to the right provider.

## Goal

### 1. **POST /appointment**
Create an API endpoint to book an appointment.
**Input** (JSON):
```json
{
  "patient": {
    "name": "John Doe",
    "email": "john@example.com",
    "state": "CT",
    "insurance": "Aetna"
  }
}
```

### 2. **Provider Matching Logic**
Assign the patient to a provider that:
- Is licensed in the **same state** as the patient
- Accepts the patient’s **insurance**

**This step will need some schema design work** 
  - I have provided a basic schema for you to start with. You can modify it as needed.
  - (hint: You can create new tables—ProviderState and ProviderInsurance or use the Provider table to store the related information and use it to filter and match them with the patients)

### 3. **Scheduling Simulation**
Call a mocked external service to simulate appointment scheduling.
- I've included a mock api for you to use. You can use a real 3rd party scheduling API if you want to but not necessary.

### 4. **Output**
```json
{
  "patient": "John Doe",
  "scheduled": true,
  "appointment_id": "apt_1234",
  "provider": "Dr. Jane Doe",
  "time": "2023-10-01T10:00:00Z"
}
```

---

## Users
This feature will be used by clinicians or by the ops team to schedule appointments for patients.

## Submission
- Fork this github repository and check in your code.
- Create a new branch with your name and start working on the assignment.
- Once you are done, push your changes to your forked repository and share the link with me.
- Please include any documentation of your implementation in your README file.


## Getting started
- Fork this repository and clone it to your local machine.
- Setup/configure python3.12, poetry.
- Install packages: Run `poetry install`. This will install the required dependencies/packages and create a virtual environment.
- Find your Python interpreter: Run `poetry shell` to find your Python interpreter. It will spawn a shell within your virtual environment and should print the interpreter path to the screen.

### Activate shell
- To activate shell run `poetry shell`
- Run `poetry run server` from the command line to start the server.
