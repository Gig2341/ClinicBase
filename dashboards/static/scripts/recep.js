let patientId = null;
let fetchedPatientData = [];

function searchPatient () {
  const searchText = document.getElementById('SearchText').value;
  const searchFilter = document.getElementById('SearchFilter').value;
  const radioList = document.getElementById('radio-button-list');

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
      document.getElementById('searchPatientForm').reset();
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

      radioList.addEventListener('click', handleSelection);
    });
}

function makeUpdateRequest (patientId) {
  const formData = new FormData(document.getElementById('updatePatientForm'));

  const jsonObject = {};
  formData.forEach((value, key) => {
    jsonObject[key] = value;
  });

  clearRadioList();

  fetch(`https://clinicbase.tech/api/patients/${patientId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(jsonObject)
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('updatePatientForm').reset();
      displayPatientInfo(data, 'Updated');
    });
}

function makeDeleteRequest (patientId) {
  clearRadioList();

  fetch(`https://clinicbase.tech/api/patients/${patientId}`, {
    method: 'DELETE'
  })
    .then(response => response.json())
    .then(data => {
      displayPatientInfo(data, 'Deleted');
    });
}

function makeSendToDoctorRequest (patientId) {
  clearRadioList();
  fetch(`https://clinicbase.tech/get_patient/${patientId}`)
    .then(response => {
      return response.json();
    })
    .then(data => {
      displayPatientInfo(data, 'Scheduled');
    });
}

function handleSelection () {
  const selectedRadio = document.querySelector('input[name="patient"]:checked');

  if (selectedRadio) {
    patientId = selectedRadio.value;
    const selectedPatient = fetchedPatientData.find(patient => patient.id === patientId);

    if (selectedPatient) {
      displayPatientInfo(selectedPatient);
    }
  }
}

function displayPatientInfo (data, estatus) {
  const patientInfoElement = document.getElementById('responseContainer');
  let statusHTML = '';

  if (estatus) {
    statusHTML = `<h4>Status:</h4><p>Patient with the information below has been successfully ${estatus}</p>`;
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

function clearRadioList () {
  const radioList = document.getElementById('radio-button-list');
  radioList.innerHTML = '';
}

function createPatient () {
  const formData = new FormData(document.getElementById('createPatientForm'));

  const jsonObject = {};
  formData.forEach((value, key) => {
    jsonObject[key] = value;
  });

  fetch('https://clinicbase.tech/api/patients', {
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
      document.getElementById('createPatientForm').reset();
      displayPatientInfo(data, 'created');
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

function getCompletedCases () {
  fetch('http://clinicbase.tech/cases/completed')
    .then(response => {
      return response.json();
    })
    .then(data => {
      displayCompletedCases(data);
    });
}

function displayCompletedCases (data) {
  const completedCasesElement = document.getElementById('patientPrescriptionContainer');
  completedCasesElement.innerHTML = '<h5>Medication and Lenses:</h5>';

  data.forEach(data => {
    completedCasesElement.innerHTML += `<div>
                                            <p>Patient Name: ${data.patient.firstname} ${data.patient.surname}</p>
                                            <p>Drug: ${data.drugs.drug}</p>
                                            <p>Lens: ${data.lenses.lens_rx}</p>
                                        </div>`;
  });
}

document.getElementById('patientPrescriptionButton').addEventListener('click', getCompletedCases);

document.getElementById('searchPatientForm').addEventListener('submit', function (event) {
  event.preventDefault();
  searchPatient();
});

document.getElementById('updatePatientForm').addEventListener('submit', function (event) {
  event.preventDefault();
  if (patientId) {
    makeUpdateRequest(patientId);
  }
});

document.getElementById('sendToDoctorButton').addEventListener('click', () => {
  if (patientId) {
    makeSendToDoctorRequest(patientId);
  }
});

document.getElementById('deletePatientButton').addEventListener('click', () => {
  if (patientId) {
    makeDeleteRequest(patientId);
  }
});

document.getElementById('createPatientForm').addEventListener('submit', function (event) {
  event.preventDefault();
  createPatient();
});
