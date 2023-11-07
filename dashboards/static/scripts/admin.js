let employeeId = null;

function searchEmployee () {
  const searchText = document.getElementById('empSearchText').value;
  const searchFilter = document.getElementById('empSearchFilter').value;
  const radioList = document.getElementById('emp-radio-button-list');

  radioList.innerHTML = '';

  const requestData = {
    [searchFilter]: searchText
  };

  fetch('https://clinicbase.tech/api/patients/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => response.json())
    .then(data => {
      data.forEach(employee => {
        const listItem = document.createElement('li');
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.id = `employee${employee.id}`;
        radio.name = 'employee';
        radio.value = employee.id;
        const label = document.createElement('label');
        label.htmlFor = `employee${employee.id}`;
        label.textContent = `Name: ${employee.name}, Email: ${employee.email}`;
        listItem.appendChild(radio);
        listItem.appendChild(label);
        radioList.appendChild(listItem);
      });

      radioList.addEventListener('click', handleSelection);
    });
}

function makeUpdateRequest (employeeId) {
  const formData = new FormData(document.getElementById('updateEmployeeForm'));

  const jsonObject = {};
  formData.forEach((value, key) => {
    jsonObject[key] = value;
  });

  clearRadioList();

  fetch(`https://clinicbase.tech/api/employees/${employeeId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(jsonObject)
  })
    .then(response => response.json())
    .then(data => {
      displayMessage(data, 'Updated');
    });
}

function makeDeleteRequest (employeeId) {
  clearRadioList();

  fetch(`https://clinicbase.tech/api/employees/${employeeId}`, {
    method: 'DELETE'
  })
    .then(response => response.json())
    .then(data => {
      displayMessage(data, 'Deleted');
    });
}

function handleSelection () {
  const selectedRadio = document.querySelector('input[name="employee"]:checked');

  if (selectedRadio) {
    employeeId = selectedRadio.value;
  }
}

function displayMessage (data, estatus) {
  const responseElement = document.getElementById('responseContainer');
  responseElement.innerHTML = `<p>Employee ${data.name} has been ${estatus} successfully</p>`;
}

function clearRadioList () {
  const radioList = document.getElementById('emp-radio-button-list');
  radioList.innerHTML = '';
}

function createEmployee () {
  const formData = new FormData(document.getElementById('createEmployeeForm'));

  const jsonObject = {};
  formData.forEach((value, key) => {
    jsonObject[key] = value;
  });

  fetch('https://clinicbase.tech/api/employees', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(jsonObject)
  })
    .then(response => {
      return response.json();
    })
    .then(data => {
      displayMessage(data, 'created');
    });
}

function findPatientCount () {
  const startDate = document.getElementById('startDate').value;
  const endDate = document.getElementById('endDate').value;
  const patientCountElement = document.getElementById('patientCount');
  const today = new Date();
  const todayISO = today.toISOString().split('T')[0];

  if (!startDate.trim() || startDate > todayISO) {
    patientCountElement.textContent = 'Start date is invalid';
    return;
  }
  if (!endDate.trim() || endDate > todayISO) {
    patientCountElement.textContent = 'End date is invalid';
    return;
  }
  if (startDate > endDate) {
    patientCountElement.textContent = 'End date must be greater than start date';
    return;
  }

  fetch('https://clinicbase.tech/api/patient_count', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ start_date: startDate, end_date: endDate })
  })
    .then(response => response.json())
    .then(data => {
      patientCountElement.textContent = `Total Patients: ${data.patient_count}`;
    });
}

function findCaseCount () {
  const startDate = document.getElementById('startDate').value;
  const endDate = document.getElementById('endDate').value;
  const caseCountElement = document.getElementById('caseCount');
  const today = new Date();
  const todayISO = today.toISOString().split('T')[0];

  if (!startDate.trim() || startDate > todayISO) {
    caseCountElement.textContent = 'Start date cannot be in future';
    return;
  }
  if (!endDate.trim() || endDate > todayISO) {
    caseCountElement.textContent = 'End date cannot be in future';
    return;
  }
  if (startDate > endDate) {
    caseCountElement.textContent = 'End date must be greater than start date';
    return;
  }

  fetch('https://clinicbase.tech/api/case_count', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ start_date: startDate, end_date: endDate })
  })
    .then(response => response.json())
    .then(data => {
      caseCountElement.textContent = `Total Case: ${data.case_count}`;
    });
}

document.addEventListener('DOMContentLoaded', function () {
  const apiStatusElement = document.getElementById('api_status');

  fetch('https://clinicbase.tech/api/status')
    .then(response => response.json())
    .then(data => {
      if (data.status === 'OK') {
        apiStatusElement.classList.add('available');
      } else {
        apiStatusElement.classList.remove('available');
      }
    });
});

document.getElementById('patientCountBtn').addEventListener('click', findPatientCount);

document.getElementById('caseCountBtn').addEventListener('click', findCaseCount);

document.getElementById('searchEmployeeForm').addEventListener('submit', function () {
  searchEmployee();
});

document.getElementById('updateEmployeeButton').addEventListener('click', () => {
  if (employeeId) {
    makeUpdateRequest(employeeId);
  }
});

document.getElementById('deleteEmployeeButton').addEventListener('click', () => {
  if (employeeId) {
    makeDeleteRequest(employeeId);
  }
});

document.getElementById('createEmployeeButton').addEventListener('click', createEmployee);
