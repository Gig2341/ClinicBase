// Get references to the input elements
const roleInput = document.getElementById('role');
const licenseNumberInput = document.getElementById('licenseNumber');

// Add an event listener to the role input
roleInput.addEventListener('input', function () {
  // Check if the role is "Receptionist"
  if (roleInput.value.toLowerCase() === 'receptionist') {
    // If it's "receptionist," disable the license number input
    licenseNumberInput.disabled = true;
  } else {
    // If it's not "receptionist," enable the license number input
    licenseNumberInput.disabled = false;
  }
});
