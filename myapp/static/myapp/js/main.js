//Attivo i tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

//Test Hidden
// Funzione JavaScript per abilitare/disabilitare il MAC Vendor quando si seleziona l'host
    function toggleMacVendor(ip, checkbox) {
        let macVendorInput = document.getElementById("hidden_mac_" + ip);
        if (checkbox.checked) {
            macVendorInput.disabled = false;  // Abilita l'input hidden se la checkbox è selezionata
        } else {
            macVendorInput.disabled = true;   // Disabilita l'input hidden se la checkbox è deselezionata
        }
    }



// Modale

const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})


