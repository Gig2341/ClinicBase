function medHistoryAPICalls () {
  const searchText = document.getElementById('searchText').value;
  const searchFilter = document.getElementById('searchFilter').value;
  const radioList = document.getElementById('emp-radio-button-list');
  let patientId = null;

  const requestData = {
    [searchFilter]: searchText
  };

  const getMedicalRecords = (patientId) => {
    fetch(`https://clinicbase.tech/api/medical_records/${patientId}`)
      .then(response => response.json())
      .then(data => {
        displayMedicalRecords(data);
        radioList.innerHTML = '';
      });
  };

  const handleSelection = () => {
    const selectedRadio = document.querySelector('input[name="patient"]:checked');
    if (selectedRadio) {
      patientId = selectedRadio.value;
    }
  };

  const handleSearchButtonClick = () => {
    fetch('https://clinicbase.tech/api/patients/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    })
      .then(response => response.json())
      .then(data => {
        data.forEach(patient => {
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
        radioList.addEventListener('click', handleSelection);
      });
  };

  function displayMedicalRecords (data) {
    const medicalRecordsElement = document.getElementById('medicalRecordsContainer');
    medicalRecordsElement.innerHTML = '<h3>Medical Records:</h3>';

    data.forEach(record => {
      medicalRecordsElement.innerHTML += `<p>Case ID: ${record.id}</p>
                                       <p>Date Created: ${record.created_at}</p>
                                       <p>Prescription: ${record.prescription}</p>
                                       <h4>History:</h4>
                                       <p>POHx: ${record.p_ocular_hx}</p>
                                       <p>PMHx: ${record.p_medical_hx}</p>
                                       <p>FOHx: ${record.f_ocular_hx}</p>
                                       <p>FMHx: ${record.f_medical_hx}</p>
                                       <h4>Examination:</h4>
                                       <p>Visual Acuity: ${record.visual_acuity}</p>
                                       <p>Ocular Examination: ${record.ocular_exam}</p>
                                       <p>Chief Complaint: ${record.chief_complaint}</p>
                                       <p>On Direct Questions: ${record.on_direct_questions}</p>
                                       <p>Intraocular Pressure (IOP): ${record.iop}</p>
                                       <p>Blood Pressure: ${record.blood_pressure}</p>
                                       <p>Blood Sugar: ${record.blood_sugar}</p>
                                       <h4>Tests:</h4>
                                       <p>Retinoscopy: ${record.retinoscopy}</p>
                                       <p>Autorefraction: ${record.autorefraction}</p>
                                       <p>Subjective Refraction: ${record.subj_refraction}</p>
                                       <p>Other Tests: ${record.other_test}</p>
                                       <h4>Diagnosis:</h4>
                                       <p>Principal Diagnosis: ${record.principal_diagnosis}</p>
                                       <p>Other Diagnosis 1: ${record.other_diagnosis_1}</p>
                                       <p>Other Diagnosis 2: ${record.other_diagnosis_2}</p>
                                       <h4>Medication:</h4>
                                       <p>Prescribed Medication: ${record.drug}</p>
                                       <h4>Lens Prescription:</h4>
                                       <p>Lens Prescription: ${record.lens_rx}</p>`;
    });
  }

  document.getElementById('searchPatientForm').addEventListener('submit', function () {
    handleSearchButtonClick();
  });
  document.getElementById('patientRecordButton').addEventListener('click', () => {
    if (patientId) {
      getMedicalRecords(patientId);
    }
  });
}

medHistoryAPICalls();
