console.log("JavaScript file loaded correttamente.");


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
if (myModal) {  // Verifica se l'elemento esiste
    const myInput = document.getElementById('myInput');
    myModal.addEventListener('shown.bs.modal', () => {
        myInput.focus();
    });
}


// Visualizzazione asincrona di hosts

//console.log(window.location.pathname);

document.addEventListener("DOMContentLoaded", function() {
    // Avvia la funzione fetchHosts quando la pagina hosts è caricata
    if (window.location.pathname === "/hosts/") { // Verifica il percorso per evitare chiamate indesiderate
        fetchHosts(true);
    }
});


let allHosts = [];  // Variabile globale per memorizzare tutti gli host

function fetchHosts(showSpinner = false) {
    if (showSpinner) {
        document.getElementById("loading-spinner").style.display = "flex";
    }

    fetch('/get_hosts/')
        .then(response => response.json())
        .then(data => {
            allHosts = data.devices;  // Memorizza tutti gli host
            renderPage(1);  // Mostra la prima pagina
            setupPagination(Math.ceil(allHosts.length / 10), 1);  // Imposta la paginazione
        })
        .catch(error => console.error('Errore nel caricamento degli hosts:', error))
        .finally(() => {
            if (showSpinner) {
                document.getElementById("loading-spinner").style.display = "none";
            }
        });
}

function renderPage(page) {
    const itemsPerPage = 10;
    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const hostsToDisplay = allHosts.slice(start, end);

    renderHosts(hostsToDisplay);  // Usa la funzione per visualizzare solo gli host della pagina
}


        
// Funzione per visualizzare gli hosts nella tabella
function renderHosts(devices) {
    const tableBody = document.getElementById("hosts-table-body");
    tableBody.innerHTML = ""; // Svuota la tabella

    devices.forEach(device => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <th scope="row">
                <input class="form-check-input" type="checkbox" value="${device.IP}" name="selected_hosts" onchange="toggleMacVendor('${device.IP}', this)">
                <input type="hidden" name="mac_vendors_${device.IP}" value="${device.MAC_Vendor}">
            </th>
            <td>${device.IP}</td>
            <td>${device.MAC_Address}</td>
            <td>${device.MAC_Vendor}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Funzione per creare i pulsanti di navigazione

function setupPagination(totalPages, currentPage) {
    const paginationContainer = document.getElementById("pagination");
    paginationContainer.innerHTML = "";

    // Bottone per pagina precedente
    if (currentPage > 1) {
        const prevButton = document.createElement("button");
        prevButton.innerHTML = "&laquo;";  // Freccia sinistra
        prevButton.classList.add("page-link");
        prevButton.type = "button";
        prevButton.addEventListener("click", () => renderPage(currentPage - 1));
        
        const prevItem = document.createElement("li");
        prevItem.classList.add("page-item");
        prevItem.appendChild(prevButton);
        paginationContainer.appendChild(prevItem);
    }

    //Pagine numerate
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement("button");
        button.innerText = i;
        button.classList.add("page-link");
        button.type = "button"
        if (i === currentPage) button.classList.add("active");

        button.addEventListener("click", () => renderPage(i));  // Passa solo la pagina
        const listItem = document.createElement("li");
        listItem.classList.add("page-item");
        listItem.appendChild(button);
        paginationContainer.appendChild(listItem);
        // paginationContainer.appendChild(button);
    }

    if (currentPage < totalPages) {
        const nextButton = document.createElement("button");
        nextButton.innerHTML = "&raquo;";  // Freccia destra
        nextButton.classList.add("page-link");
        nextButton.type = "button";
        nextButton.addEventListener("click", () => renderPage(currentPage + 1));
        
        const nextItem = document.createElement("li");
        nextItem.classList.add("page-item");
        nextItem.appendChild(nextButton);
        paginationContainer.appendChild(nextItem);
    }
}

/*
// Funzione per creare i pulsanti di navigazione con frecce
function setupPagination(totalPages, currentPage) {
    const paginationContainer = document.getElementById("pagination");
    paginationContainer.innerHTML = "";

    // Bottone per pagina precedente (disabilitato se siamo alla prima pagina)
    const prevItem = document.createElement("li");
    prevItem.classList.add("page-item");
    if (currentPage === 1) prevItem.classList.add("disabled");

    const prevButton = document.createElement("button");
    prevButton.innerHTML = "&laquo;"; // Freccia sinistra
    prevButton.classList.add("page-link");
    prevButton.type = "button";
    prevButton.addEventListener("click", () => {
        if (currentPage > 1) renderPage(currentPage - 1); // Vai alla pagina precedente
    });
    prevItem.appendChild(prevButton);
    paginationContainer.appendChild(prevItem);

    // Pagine numerate
    for (let i = 1; i <= totalPages; i++) {
        const listItem = document.createElement("li");
        listItem.classList.add("page-item");

        const button = document.createElement("button");
        button.innerText = i;
        button.classList.add("page-link");
        button.classList.add("rounded-circle");
        button.type = "button";
        if (i === currentPage) button.classList.add("active");

        button.addEventListener("click", () => renderPage(i));
        listItem.appendChild(button);
        paginationContainer.appendChild(listItem);
    }

    // Bottone per pagina successiva (disabilitato se siamo all'ultima pagina)
    const nextItem = document.createElement("li");
    nextItem.classList.add("page-item");
    if (currentPage === totalPages) nextItem.classList.add("disabled");

    const nextButton = document.createElement("button");
    nextButton.innerHTML = "&raquo;"; // Freccia destra
    nextButton.classList.add("page-link");
    nextButton.type = "button";
    nextButton.addEventListener("click", () => {
        if (currentPage < totalPages) renderPage(currentPage + 1); // Vai alla pagina successiva
    });
    nextItem.appendChild(nextButton);
    paginationContainer.appendChild(nextItem);
}
*/


