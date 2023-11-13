let patientId = null;
let caseId = null;
let fetchedPatientData = [];

function getPatientQueue () {
  const radioList = document.getElementById('radio-button-list');

  document.getElementById('medicalRecordsContainer').innerHTML = '';
  radioList.innerHTML = '';

  fetch('https://clinicbase.tech/api/cases/queue')
    .then(response => {
      return response.json();
    })
    .then(data => {
      fetchedPatientData = data;
      data.forEach(patient => {
        const listItem = document.createElement('li');
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.id = `patient${patient.id}`;
        radio.name = 'patient';
        radio.value = patient.id;
        const label = document.createElement('label');
        label.htmlFor = `patient${patient.id}`;
        label.textContent = `First Name: ${patient.firstname}, Surname: ${patient.surname}`;
        listItem.appendChild(radio);
        listItem.appendChild(label);
        radioList.appendChild(listItem);
      });
      const radioButtons = document.querySelectorAll('input[name="patient"]');
      radioButtons.forEach(radio => {
        radio.addEventListener('change', function () {
          patientId = this.value;
          const selectedPatient = fetchedPatientData.find(patient => patient.id === patientId);

          if (selectedPatient) {
            displayPatientInfo(selectedPatient);
          }
        });
      });
    });
}

function getMedicalRecords () {
  document.getElementById('radio-button-list').innerHTML = '';
  if (patientId) {
    fetch(`https://clinicbase.tech/api/medical_records/${patientId}`)
      .then(response => response.json())
      .then(data => {
        generateAndPreviewHtml(data);
      });
  }
}

function createNewCase () {
  document.getElementById('radio-button-list').innerHTML = '';
  if (patientId) {
    fetch(`https://clinicbase.tech/api/cases/${patientId}`)
      .then(response => {
        return response.json();
      })
      .then(data => {
        caseId = data.id;
        const selectedPatient = fetchedPatientData.find(patient => patient.id === patientId);

        if (selectedPatient) {
          displayPatientInfo(selectedPatient, 'created');
        }
      });
  }
}

function initializeHandler (buttonId, actionType) {
  const button = document.getElementById(buttonId);
  button.addEventListener('click', function () {
    if (caseId) {
      const allFormInfo = {};

      function collectAndAddFormDataSection (sectionName, form) {
        const formData = collectFormData(form);
        const hasNonEmptyField = Object.values(formData).some(value => value.trim() !== '');

        if (hasNonEmptyField) {
          allFormInfo[sectionName] = formData;
        }
      }

      const tabSections = document.querySelectorAll('.tabcontent');
      tabSections.forEach(section => {
        const sectionName = section.id;
        collectAndAddFormDataSection(sectionName.toLowerCase(), section);
      });

      fetch(`https://clinicbase.tech/api/cases/${actionType}/${caseId}/${patientId}`, {
        method: 'POST',
        body: JSON.stringify(allFormInfo),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          return response.json();
        })
        .then(data => {
          const selectedPatient = fetchedPatientData.find(patient => patient.id === patientId);

          if (selectedPatient) {
            displayPatientInfo(selectedPatient, actionType === 'submit' ? 'submitted' : 'saved');
          }
          if (actionType === 'submit') {
            clearFormValues();
          }
        });
    }
  });
}

function collectFormData (form) {
  const formData = {};
  const inputs = form.querySelectorAll('textarea');
  inputs.forEach(input => {
    formData[input.name] = input.value;
  });
  return formData;
}

function clearFormValues () {
  document.getElementById('medicalForm').reset();
}

function displayPatientInfo (data, estatus) {
  const patientInfoElement = document.getElementById('responseContainer');
  let statusHTML = '';

  if (estatus) {
    statusHTML = `<h4>Status:</h4><p>Case for the below Patient has been successfully ${estatus}</p>`;
  }
  patientInfoElement.innerHTML = `${statusHTML}<h4>Patient Information:</h4>
    <div>
        <p>First Name: ${data.firstname}</p>
        <p>Surname: ${data.surname}</p>
    </div>
    <div>
        <p>Date of Birth: ${data.dob}</p>
        <p>Contact: ${data.tel}</p>
    </div>
    <div>
        <p>Occupation: ${data.occupation}</p>
        <p>Insurance: ${data.insurance}</p>
    </div>`;
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

document.getElementById('refreshButton').addEventListener('click', getPatientQueue);
document.getElementById('patientRecordButton').addEventListener('click', getMedicalRecords);
document.getElementById('newCaseButton').addEventListener('click', createNewCase);
initializeHandler('saveCaseButton', 'save');
initializeHandler('submitCaseButton', 'submit');
