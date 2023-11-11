let employeeId = null;

function searchEmployee () {
  const searchText = document.getElementById('empSearchText').value;
  const searchFilter = document.getElementById('empSearchFilter').value;
  const radioList = document.getElementById('emp-radio-button-list');

  radioList.innerHTML = '';

  const requestData = {
    [searchFilter]: searchText
  };

  fetch('https://clinicbase.tech/api/employees/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('searchEmployeeForm').reset();
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
      const radioButtons = document.querySelectorAll('input[name="employee"]');
      radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
          employeeId = this.value;
        });
      });
    });
}

function handleUpdateRequest () {
  if (employeeId) {
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
        document.getElementById('updateEmployeeForm').reset();
        displayMessage(data, 'Updated');
      });
  }
}

function handleDeleteRequest () {
  if (employeeId) {
    clearRadioList();

    fetch(`https://clinicbase.tech/api/employees/${employeeId}`, {
      method: 'DELETE'
    })
      .then(response => response.json())
      .then(data => {
        displayMessage(data, 'Deleted');
      });
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

  fetch('https://clinicbase.tech/api/employee', {
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
      document.getElementById('createEmployeeForm').reset();
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
    patientCountElement.textContent = 'Select a valid Start date';
    return;
  }
  if (!endDate.trim() || endDate > todayISO) {
    patientCountElement.textContent = 'Select a valid End date';
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
    caseCountElement.textContent = 'Select a valid Start date';
    return;
  }
  if (!endDate.trim() || endDate > todayISO) {
    caseCountElement.textContent = 'Select a valid End date';
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

document.getElementById('searchEmployeeForm').addEventListener('submit', function (event) {
  event.preventDefault();
  searchEmployee();
});

document.getElementById('createEmployeeForm').addEventListener('submit', function (event) {
  event.preventDefault();
  createEmployee();
});

document.getElementById('updateEmployeeForm').addEventListener('submit', function (event) {
  event.preventDefault();
  handleUpdateRequest();
});

document.getElementById('deleteEmployeeButton').addEventListener('click', function () {
  handleDeleteRequest();
});
