// Fonctions utilitaires pour les modales
function openModal(modalId) {
    document.getElementById(modalId).classList.add('is-active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('is-active');
}

function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(modal => {
        modal.classList.remove('is-active');
    });
}

// Gestion des modales
document.addEventListener('DOMContentLoaded', () => {

    // Gestionnaires d'événements pour les modales
    document.querySelectorAll('.modal-background, .modal .delete, .modal .button:not(.is-success)').forEach(element => {
        element.addEventListener('click', () => {
            closeAllModals();
        });
    });

    // Boutons d'ouverture des modales
    document.getElementById('newTemplateBtn').addEventListener('click', () => openModal('templateModal'));
    document.getElementById('newPrinterBtn').addEventListener('click', () => openModal('printerModal'));

    // Gestion du glisser-déposer
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('is-dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('is-dragover');
        });
    });

    dropZone.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.name.endsWith('.csv') || file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
                processFile(file);
            } else {
                alert('Format de fichier non supporté. Veuillez utiliser un fichier CSV ou Excel.');
            }
        }
    }

    // Gestion des templates
    document.getElementById('saveTemplateBtn').addEventListener('click', async () => {
        const templateData = {
            name: document.getElementById('templateName').value,
            zpl_code: document.getElementById('templateZPL').value,
            width: parseFloat(document.getElementById('templateWidth').value),
            height: parseFloat(document.getElementById('templateHeight').value),
            dpmm: parseInt(document.getElementById('templateDPI').value),
            variables_count: (document.getElementById('templateZPL').value.match(/\$[0-9]+/g) || []).length
        };

        try {
            const response = await fetch('/api/templates', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(templateData)
            });

            if (response.ok) {
                closeModal('templateModal');
                loadTemplates();
            } else {
                alert('Erreur lors de la création du modèle');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la création du modèle');
        }
    });

    // Gestion des imprimantes
    document.getElementById('savePrinterBtn').addEventListener('click', async () => {
        const printerData = {
            name: document.getElementById('printerName').value,
            ip_address: document.getElementById('printerIP').value,
            port: parseInt(document.getElementById('printerPort').value)
        };

        try {
            const response = await fetch('/api/printers', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(printerData)
            });

            if (response.ok) {
                closeModal('printerModal');
                loadPrinters();
            } else {
                alert('Erreur lors de l\'ajout de l\'imprimante');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de l\'ajout de l\'imprimante');
        }
    });

    // Chargement initial des données
    loadTemplates();
    loadPrinters();
});

// Fonctions de chargement des données
async function loadTemplates() {
    try {
        const response = await fetch('/api/templates');
        const templates = await response.json();
        const templatesList = document.getElementById('templatesList');
        
        templatesList.innerHTML = '<ul class="menu-list">' + 
            templates.map(template => `
                <li>
                    <a href="#" class="template-item" data-template-id="${template.id}">
                        ${template.name}
                        <div class="template-actions">
                            <span class="icon has-text-danger delete-template" data-template-id="${template.id}">
                                <i class="fas fa-trash"></i>
                            </span>
                        </div>
                    </a>
                </li>
            `).join('') + '</ul>';

        // Gestionnaires d'événements pour les modèles
        document.querySelectorAll('.template-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                if (!e.target.closest('.delete-template')) {
                    document.querySelectorAll('.template-item').forEach(i => i.classList.remove('is-active'));
                    item.classList.add('is-active');
                    window.selectedTemplateId = item.dataset.templateId;
                }
            });
        });

        document.querySelectorAll('.delete-template').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.preventDefault();
                e.stopPropagation();
                if (confirm('Voulez-vous vraiment supprimer ce modèle ?')) {
                    const templateId = btn.dataset.templateId;
                    try {
                        const response = await fetch(`/api/templates/${templateId}`, {
                            method: 'DELETE'
                        });
                        if (response.ok) {
                            loadTemplates();
                        } else {
                            alert('Erreur lors de la suppression du modèle');
                        }
                    } catch (error) {
                        console.error('Erreur:', error);
                        alert('Erreur lors de la suppression du modèle');
                    }
                }
            });
        });
    } catch (error) {
        console.error('Erreur lors du chargement des modèles:', error);
    }
}

async function loadPrinters() {
    try {
        const response = await fetch('/api/printers');
        const printers = await response.json();
        const printersList = document.getElementById('printersList');
        
        printersList.innerHTML = printers.map(printer => `
            <div class="printer-item" data-printer-id="${printer.id}">
                <div class="printer-info">
                    <span class="status-indicator ${printer.status === 'connected' ? 'is-connected' : 'is-disconnected'}"></span>
                    ${printer.name}
                </div>
                <div class="printer-actions">
                    <div class="printer-status">
                        ${printer.ip_address}:${printer.port}
                    </div>
                    <span class="icon has-text-danger delete-printer" data-printer-id="${printer.id}">
                        <i class="fas fa-trash"></i>
                    </span>
                </div>
            </div>
        `).join('');

        // Gestionnaires d'événements pour les imprimantes
        document.querySelectorAll('.printer-item').forEach(item => {
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.delete-printer')) {
                    document.querySelectorAll('.printer-item').forEach(i => i.classList.remove('is-active'));
                    item.classList.add('is-active');
                    window.selectedPrinterId = item.dataset.printerId;
                }
            });
        });

        document.querySelectorAll('.delete-printer').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                if (confirm('Voulez-vous vraiment supprimer cette imprimante ?')) {
                    const printerId = btn.dataset.printerId;
                    try {
                        const response = await fetch(`/api/printers/${printerId}`, {
                            method: 'DELETE'
                        });
                        if (response.ok) {
                            loadPrinters();
                        } else {
                            alert('Erreur lors de la suppression de l\'imprimante');
                        }
                    } catch (error) {
                        console.error('Erreur:', error);
                        alert('Erreur lors de la suppression de l\'imprimante');
                    }
                }
            });
        });
    } catch (error) {
        console.error('Erreur lors du chargement des imprimantes:', error);
    }
}

// Fonction de traitement des fichiers
async function processFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        // TODO: Implémenter l'endpoint de traitement des fichiers
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            updateTable(data);
        } else {
            alert('Erreur lors du traitement du fichier');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors du traitement du fichier');
    }
}

// Fonction de mise à jour du tableau
function updateTable(data) {
    const headers = data.headers;
    const rows = data.rows;
    
    // Mise à jour des en-têtes
    const tableHeaders = document.getElementById('tableHeaders');
    tableHeaders.innerHTML = `
        <th>
            <div class="field">
                <div class="control">
                    <input type="checkbox" id="selectAll" title="Tout sélectionner">
                </div>
            </div>
        </th>
        ${headers.map(header => `<th>${header}</th>`).join('')}
        <th>Actions</th>
    `;

    // Réinitialiser les gestionnaires d'événements
    document.removeEventListener('change', handleCheckboxChange);
    document.addEventListener('change', handleCheckboxChange);

    // Mise à jour des données
    const tableData = document.getElementById('tableData');
    tableData.innerHTML = rows.map((row, index) => `
        <tr>
            <td><input type="checkbox" class="row-select" data-row="${index}"></td>
            ${row.map(cell => `<td>${cell}</td>`).join('')}
            <td class="buttons">
                <button class="button is-small is-info" onclick="previewLabel(${index})">
                    <span class="icon"><i class="fas fa-eye"></i></span>
                </button>
                <button class="button is-small is-success" onclick="printLabel(${index})">
                    <span class="icon"><i class="fas fa-print"></i></span>
                </button>
            </td>
        </tr>
    `).join('');

    // Initialiser l'état des cases à cocher
    initializeCheckboxes();

    // Gestion du bouton d'impression multiple
    document.getElementById('printSelectedBtn').addEventListener('click', printSelected);
    updatePrintSelectedButton();
}

// Fonctions de prévisualisation et d'impression
async function previewLabel(rowIndex) {
    if (!window.selectedTemplateId) {
        alert('Veuillez sélectionner un modèle d\'étiquette');
        return;
    }

    try {
        // Récupérer le modèle
        const templateResponse = await fetch('/api/templates');
        const templates = await templateResponse.json();
        const template = templates.find(t => t.id === parseInt(window.selectedTemplateId));
        
        if (!template) {
            alert('Modèle non trouvé');
            return;
        }

        // Récupérer les données de la ligne
        const row = document.querySelector(`#tableData tr:nth-child(${rowIndex + 1})`);
        const cells = Array.from(row.cells).slice(1, -1); // Exclure la checkbox et les actions
        const headers = Array.from(document.querySelectorAll('#tableHeaders th')).slice(1, -1).map(th => th.textContent);
        
        const data = {};
        headers.forEach((header, index) => {
            data[index + 1] = cells[index].textContent;
        });

        // Préparer le code ZPL avec les variables remplacées
        let zpl = template.zpl_code;
        Object.entries(data).forEach(([key, value]) => {
            zpl = zpl.replace(new RegExp(`\\$${key}`, 'g'), value);
        });

        // Afficher le code ZPL
        document.getElementById('previewZPL').value = zpl;

        // Générer la prévisualisation
        const response = await fetch('/api/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                template_id: window.selectedTemplateId,
                data: data
            })
        });

        const result = await response.json();
        const previewError = document.getElementById('previewError');
        
        if (response.ok && result.success) {
            document.getElementById('previewImage').src = 'data:image/png;base64,' + btoa(result.image);
            previewError.classList.add('is-hidden');
        } else {
            document.getElementById('previewImage').src = '';
            previewError.textContent = result.error || 'Erreur lors de la génération de l\'aperçu';
            previewError.classList.remove('is-hidden');
        }

        openModal('previewModal');
    } catch (error) {
        console.error('Erreur:', error);
        const previewError = document.getElementById('previewError');
        previewError.textContent = 'Erreur lors de la génération de l\'aperçu';
        previewError.classList.remove('is-hidden');
        openModal('previewModal');
    }
}

// Gestionnaire d'événements pour les cases à cocher
function handleCheckboxChange(e) {
    const target = e.target;
    if (target.id === 'selectAll') {
        // Gestion du "tout sélectionner"
        const rowCheckboxes = document.querySelectorAll('.row-select');
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = target.checked;
        });
    } else if (target.classList.contains('row-select')) {
        // Mise à jour de la case "tout sélectionner"
        const selectAll = document.getElementById('selectAll');
        const rowCheckboxes = document.querySelectorAll('.row-select');
        selectAll.checked = Array.from(rowCheckboxes).every(cb => cb.checked);
    }
    updatePrintSelectedButton();
}

// Initialisation des cases à cocher
function initializeCheckboxes() {
    const selectAll = document.getElementById('selectAll');
    const rowCheckboxes = document.querySelectorAll('.row-select');

    // État initial
    selectAll.checked = rowCheckboxes.length > 0 && Array.from(rowCheckboxes).every(cb => cb.checked);
    updatePrintSelectedButton();
}

// Fonction pour mettre à jour l'état du bouton d'impression multiple
function updatePrintSelectedButton() {
    const hasSelection = Array.from(document.querySelectorAll('.row-select')).some(cb => cb.checked);
    const printSelectedBtn = document.getElementById('printSelectedBtn');
    printSelectedBtn.disabled = !hasSelection;
    
    // Mettre à jour le texte du bouton
    const selectedCount = Array.from(document.querySelectorAll('.row-select')).filter(cb => cb.checked).length;
    printSelectedBtn.innerHTML = `
        <span class="icon">
            <i class="fas fa-print"></i>
        </span>
        <span>Imprimer la sélection${selectedCount > 0 ? ` (${selectedCount})` : ''}</span>
    `;
}

// Fonction pour imprimer les lignes sélectionnées
async function printSelected() {
    if (!window.selectedTemplateId) {
        alert('Veuillez sélectionner un modèle d\'étiquette');
        return;
    }
    if (!window.selectedPrinterId) {
        alert('Veuillez sélectionner une imprimante');
        return;
    }

    const selectedRows = Array.from(document.querySelectorAll('.row-select:checked')).map(checkbox => {
        const row = checkbox.closest('tr');
        const cells = Array.from(row.cells).slice(1, -1); // Exclure la checkbox et les actions
        const headers = Array.from(document.querySelectorAll('#tableHeaders th')).slice(1, -1).map(th => th.textContent);
        
        const data = {};
        headers.forEach((header, index) => {
            data[index + 1] = cells[index].textContent;
        });
        return data;
    });

    if (selectedRows.length === 0) {
        alert('Veuillez sélectionner au moins une ligne');
        return;
    }

    let successCount = 0;
    let errorCount = 0;

    for (const data of selectedRows) {
        try {
            const response = await fetch('/api/print', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    template_id: window.selectedTemplateId,
                    printer_id: window.selectedPrinterId,
                    data: data,
                    copies: 1
                })
            });

            const result = await response.json();
            if (result.success) {
                successCount++;
            } else {
                errorCount++;
            }
        } catch (error) {
            console.error('Erreur:', error);
            errorCount++;
        }
    }

    if (errorCount === 0) {
        alert(`${successCount} étiquette(s) imprimée(s) avec succès`);
    } else {
        alert(`${successCount} étiquette(s) imprimée(s) avec succès\n${errorCount} erreur(s) d'impression`);
    }
}

async function printLabel(rowIndex) {
    if (!window.selectedTemplateId) {
        alert('Veuillez sélectionner un modèle d\'étiquette');
        return;
    }
    if (!window.selectedPrinterId) {
        alert('Veuillez sélectionner une imprimante');
        return;
    }

    try {
        // Récupérer les données de la ligne
        const row = document.querySelector(`#tableData tr:nth-child(${rowIndex + 1})`);
        const cells = Array.from(row.cells).slice(1, -1); // Exclure la checkbox et les actions
        const headers = Array.from(document.querySelectorAll('#tableHeaders th')).slice(1, -1).map(th => th.textContent);
        
        const data = {};
        headers.forEach((header, index) => {
            data[index + 1] = cells[index].textContent;
        });

        const response = await fetch('/api/print', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                template_id: window.selectedTemplateId,
                printer_id: window.selectedPrinterId,
                data: data,
                copies: 1
            })
        });

        const result = await response.json();
        if (result.success) {
            alert('Impression envoyée avec succès');
        } else {
            alert('Erreur lors de l\'impression: ' + result.message);
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de l\'impression');
    }
}
