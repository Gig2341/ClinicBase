let patientId = null;

function getMedicalRecords () {
  if (patientId) {
    fetch(`https://clinicbase.tech/api/medical_records/${patientId}`)
      .then((response) => response.json())
      .then((data) => {
        generateAndPreviewHtml(data);
        document.getElementById('radio-button-list').innerHTML = '';
      });
  }
}

function handleSearchButtonClick () {
  const searchText = document.getElementById('searchText').value;
  const searchFilter = document.getElementById('searchFilter').value;
  const radioList = document.getElementById('radio-button-list');

  document.getElementById('medicalRecordsContainer').innerHTML = '';

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
    .then((response) => response.json())
    .then((data) => {
      radioList.innerHTML = '';

      document.getElementById('searchPatientForm').reset();
      data.forEach((patient) => {
        const listItem = document.createElement('li');
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'patient';
        radio.id = `patient${patient.id}`;
        radio.value = patient.id;
        const label = document.createElement('label');
        label.htmlFor = `patient${patient.id}`;
        label.textContent = `Name: ${patient.firstname} ${patient.surname}, DOB: ${patient.dob}`;
        listItem.appendChild(radio);
        listItem.appendChild(label);
        radioList.appendChild(listItem);
      });
      const radioButtons = document.querySelectorAll('input[name="patient"]');
      radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
          patientId = this.value;
        });
      });
    });
}

function generateAndPreviewHtml (responseData) {
  const container = document.getElementById('medicalRecordsContainer');

  function generateHtmlContent (data) {
    for (const sectionName in data) {
      if (Object.prototype.hasOwnProperty.call(data, sectionName)) {
        const sectionData = data[sectionName];
        const sectionContainer = document.createElement('div');
        sectionContainer.className = 'patient-info';

        const sectionHeading = document.createElement('h5');
        sectionHeading.textContent = sectionName;
        sectionContainer.appendChild(sectionHeading);

        for (const [fieldName, fieldValue] of Object.entries(sectionData)) {
          const label = document.createElement('label');
          label.textContent = fieldName;

          const fieldDisplay = document.createElement('p');
          fieldDisplay.textContent = fieldValue;

          sectionContainer.appendChild(label);
          sectionContainer.appendChild(fieldDisplay);
        }

        container.appendChild(sectionContainer);
      }
    }
  }

  container.innerHTML = '';
  generateHtmlContent(responseData);
}

document.getElementById('searchPatientForm').addEventListener('submit', function (event) {
  event.preventDefault();
  handleSearchButtonClick();
});

document.getElementById('patientRecordButton').addEventListener('click', getMedicalRecords);
