
// Attivo i tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

let allHosts = [];  // Variabile globale per memorizzare tutti gli host
let currentPage = 1;  // Variabile globale per tenere traccia della pagina corrente

// Funzione JavaScript per abilitare/disabilitare il MAC Vendor quando si seleziona l'host
function toggleMacVendor(ip, checkbox) {
    let macVendorInput = document.getElementById("hidden_mac_" + ip);
    macVendorInput.disabled = !checkbox.checked;  // Abilita l'input hidden se la checkbox è selezionata

    
}


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

            currentPage = page;  // Aggiorna la pagina corrente
            renderHosts(hostsToDisplay);  // Visualizza solo gli host della pagina
            setupPagination(Math.ceil(allHosts.length / 10), page);  // Ricarica i pulsanti di paginazione
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
                        <input type="hidden" name="mac_vendors_${device.IP}" value="${device.MAC_Vendor}" id="hidden_mac_${device.IP}" disabled>
                    </th>
                    <td>${device.IP}</td>
                    <td>${device.MAC_Address}</td>
                    <td>${device.MAC_Vendor}</td>
                `;
                tableBody.appendChild(row);
            });
            updateAddTargetsButton(); // Aggiorna lo stato del pulsante dopo il rendering degli hosts
        }

        function setupPagination(totalPages, currentPage) {
            const paginationContainer = document.getElementById("pagination");
            paginationContainer.innerHTML = "";

            // Bottone per pagina precedente
            const prevItem = document.createElement("li");
            prevItem.classList.add("page-item");
            if (currentPage === 1) prevItem.classList.add("disabled");

            const prevButton = document.createElement("button");
            prevButton.innerHTML = "&laquo;";  // Freccia sinistra
            prevButton.classList.add("page-link", "rounded-circle");
            prevButton.type = "button";
            prevButton.addEventListener("click", () => {
                if (currentPage > 1) renderPage(currentPage - 1);
            });
            prevItem.appendChild(prevButton);
            paginationContainer.appendChild(prevItem);

            // Pagine numerate
            for (let i = 1; i <= totalPages; i++) {
                const listItem = document.createElement("li");
                listItem.classList.add("page-item");

                const button = document.createElement("button");
                button.innerText = i;
                button.classList.add("page-link", "rounded-circle");
                button.type = "button";

                if (i === currentPage) {
                    button.classList.add("page-active");
                    button.setAttribute("aria-current", "page");
                }

                button.addEventListener("click", () => renderPage(i));
                listItem.appendChild(button);
                paginationContainer.appendChild(listItem);
            }

            // Bottone per pagina successiva
            const nextItem = document.createElement("li");
            nextItem.classList.add("page-item");
            if (currentPage === totalPages) nextItem.classList.add("disabled");

            const nextButton = document.createElement("button");
            nextButton.innerHTML = "&raquo;";  // Freccia destra
            nextButton.classList.add("page-link", "rounded-circle");
            nextButton.type = "button";
            nextButton.addEventListener("click", () => {
                if (currentPage < totalPages) renderPage(currentPage + 1);
            });
            nextItem.appendChild(nextButton);
            paginationContainer.appendChild(nextItem);
        }




// Funzione per gestire lo stato del pulsante "Aggiungi a Targets"
        function updateAddTargetsButton() {
            const addTargetsBtn = document.getElementById("addTargetsBtn");
            const tooltipContainer = document.getElementById("tooltipContainer");
            const checkboxes = document.querySelectorAll('input[name="selected_hosts"]:checked');
            
            if (checkboxes.length > 0) {
                addTargetsBtn.disabled = false;
                addTargetsBtn.style.cursor = "pointer";
                
                // Rimuovi il tooltip se esiste
                const tooltipInstance = bootstrap.Tooltip.getInstance(tooltipContainer);
                if (tooltipInstance) tooltipInstance.dispose(); 
            } else {
                addTargetsBtn.disabled = true;
                // addTargetsBtn.setAttribute("title", "Seleziona almeno un host per continuare");
                tooltipContainer.style.cursor = "not-allowed";
                
                // Crea o aggiorna il tooltip
                bootstrap.Tooltip.getOrCreateInstance(tooltipContainer);
            }
        }

// Visualizzazione asincrona di hosts
document.addEventListener("DOMContentLoaded", function() {
    if (window.location.pathname === "/hosts/") {
        fetchHosts(true);
        // Event Delegation per monitorare i cambiamenti delle checkbox
        document.getElementById("hosts-table-body").addEventListener("change", (event) => {
            if (event.target && event.target.name === "selected_hosts") {
                updateAddTargetsButton();
            }
        });
    }
});



document.addEventListener("DOMContentLoaded", function () {
    const toast = document.getElementById("toast");
    
    if (toast) {
        // Mostra il toast con l'animazione
        toast.classList.add("toast-show");

        // Nasconde il toast dopo 3 secondi
        setTimeout(() => {
            toast.classList.remove("toast-show");
        }, 3000); // Tempo di visualizzazione in millisecondi

        // Rimuove il toast dal DOM dopo la transizione
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3500); // Dopo la fine della transizione
    }
});

//Percentuale completamento scan

// Aggiorna la barra di avanzamento di un singolo task
const taskIds = JSON.parse(document.getElementById("taskIds").textContent);

function updateAllTaskProgress() {
    taskIds.forEach(task_uuid => {
        updateTaskProgress(task_uuid);
    });
}

function updateTaskProgress(task_uuid) {
    fetch(`/tasks/status/${task_uuid}/`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json()
        })
        .then(data => {
            if (data.progress !== undefined) {
                const progressBar = document.getElementById(`progress-bar-${task_uuid}`);
                progressBar.style.width = `${data.progress}%`;
                progressBar.setAttribute("aria-valuenow", data.progress);
            }
        })
        .catch(error => console.error("Errore nell'aggiornamento dello stato:", error));
}



// Esegui updateAllTaskProgress ogni ...
setInterval(updateAllTaskProgress, 36000);

