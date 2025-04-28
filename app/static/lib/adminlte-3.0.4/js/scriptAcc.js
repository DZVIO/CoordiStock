// MOVIMIENTO DE ACTIVOS //
document.addEventListener('DOMContentLoaded', function () {
    $('.movement-title').click(function () {
        console.log("Clicked");
        $(this).closest('.member-infos').find('.activoinfo').slideToggle(600);
    });

    $('.activoinfo').each(function () {
        let categoria = $(this).find('tr:has(th:contains("Categoria")) td').text().trim().toLowerCase();

        if (categoria === "monitor") {
            $(this).find('tr:has(th:contains("Renting")), tr:has(th:contains("Nomenclatura"))').hide();
        }
    });

    $('.activoinfo').each(function () {
        let tipo = $(this).find('tr:has(th:contains("Tipo")) td').text().trim().toLowerCase();

        if (tipo === "periferico") {
            $(this).find('tr:has(th:contains("Renting")), tr:has(th:contains("Activo"))').hide();
        }
    });

    function setupSearchComponent({
        searchInputId,
        listContainerId,
        hiddenInputId,
        apiUrl,
        getExtraParams = () => '',
        formatItem,
    }) {
        const $searchInput = $(`#${searchInputId}`);
        const $list = $(`#${listContainerId}`);

        function fetchItems(query = '') {
            const extraParams = getExtraParams();
            $.ajax({
                url: `${apiUrl}?search=${query}${extraParams}`,
                type: 'GET',
                success: function (data) {
                    $list.empty().show();

                    if (data.length === 0) {
                        $list.append('<div class="list-group-item disabled">Sin resultados</div>');
                    } else {
                        data.forEach(item => {
                            $list.append(
                                `<button type="button" class="list-group-item list-group-item-action" data-id="${item.id}" data-item-data='${JSON.stringify(item)}'>
                                    ${formatItem(item)}
                                </button>`
                            );
                        });
                    }
                }
            });
        }

        $searchInput.on('focus', () => fetchItems());

        $searchInput.on('input', function () {
            const query = $(this).val();
            fetchItems(query);
        });

        $list.on('click', '.list-group-item', function () {
            const selectedText = $(this).text();
            const selectedId = $(this).data('id');
        
            $searchInput.val(selectedText);
            $(`#${hiddenInputId}`).val(selectedId);
            $list.hide();
        
            const selectedItem = $(this).data('itemData');
        
            if (selectedItem && selectedItem.renting === true) {
                $('#mensaje-renting').show();
            } else {
                $('#mensaje-renting').hide();
            }
        });

        $(document).on('click', function (e) {
            if (!$(e.target).closest(`#${searchInputId}, #${listContainerId}`).length) {
                $list.hide();
            }
        });
    }

    // Terminales
    setupSearchComponent({
        searchInputId: 'terminal-search',
        listContainerId: 'terminal-list',
        hiddenInputId: 'terminal-id',
        apiUrl: '/app/movimiento/terminal_api/',
        formatItem: item => `${item.terminal} - ${item.nombre} - ${item.direccion}`
    });

    // Activos
    setupSearchComponent({
        searchInputId: 'asset-search',
        listContainerId: 'asset-list',
        hiddenInputId: 'asset-id',
        apiUrl: '/app/movimiento/activo_api/',
        getExtraParams: () => {
            const tipo = $('#asset_type').val();
            const categoria = $('#asset_category').val();
            return `&tipo=${tipo}&categoria=${categoria}`;
        },
        formatItem: item => `${item.disponibilidad ? 'Disponible' : 'No disponible'}: ${item.nombre_marca} - ${item.activo} - ${item.modelo} - ${item.n_serie}`
    });

    // Agentes
    setupSearchComponent({
        searchInputId: 'agent-search',
        listContainerId: 'agent-list',
        hiddenInputId: 'agent-id',
        apiUrl: '/app/movimiento/agente_api/',
        getExtraParams: () => {
            const activoId = $('#asset-id').val();
            if (activoId) {
                return `&activo=${activoId}`;
            }
            return '';
        },
        formatItem: item => `${item.nombre} - ${item.codigo} - ${item.email} - ${item.nombre_area} - ${item.nombre_terminal}`
    });

    // Áreas
    setupSearchComponent({
        searchInputId: 'area-search',
        listContainerId: 'area-list',
        hiddenInputId: 'area-id',
        apiUrl: '/app/movimiento/area_api/',
        formatItem: item => `${item.area}`
    });

    document.querySelector('form').addEventListener('submit', function (e) {
        const idactivo = document.getElementById('asset-id').value;
        const idagente = document.getElementById('agent-id').value;
        const idarea = document.getElementById('area-id').value;
    
        if (!idactivo || !idagente || !idarea) {
            e.preventDefault();
            Swal.fire('Error', 'Debes seleccionar activo, agente y área.', 'error');
            return;
        }
    
        const detalle = {
            idactivo,
            motivo: document.getElementById('motivo-textarea').value,
            idagente,
            nomenclature: document.getElementById('nomenclature-textarea').value,
            idarea,
            observaciones: document.getElementById('observaciones-textarea').value
        };
    
        console.log("Enviando detalle:", detalle);
        document.getElementById('detalle_movimiento').value = JSON.stringify([detalle]);
    });

    document.querySelector('form').addEventListener('submit', function (e) {
        const detalle = {
            idactivo: document.getElementById('asset-id').value,
            motivo: document.getElementById('motivo-textarea').value,
            idagente: document.getElementById('agent-id').value,
            nomenclature: document.getElementById('nomenclature-textarea').value,
            idarea: document.getElementById('area-id').value,
            observaciones: document.getElementById('observaciones-textarea').value
        };
        
        console.log("Detalle movimiento enviado:", JSON.stringify([detalle]));
        document.getElementById('detalle_movimiento').value = JSON.stringify([detalle]);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const assetTypeSelect = document.getElementById('asset_type');
    const assetCategorySelect = document.getElementById('asset_category');
    const nomenclatureField = document.querySelector('.nomenclatura');

    const categorias = {
        True: ["PC", "Laptop", "Monitor"],
        False: ["Diadema", "Teclado", "Mouse", "Base refrigerante"]
    };

    function actualizarCategorias(tipo) {
        assetCategorySelect.innerHTML = '';

        categorias[tipo].forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            assetCategorySelect.appendChild(option);
        });
    }

    function toggleNomenclature() {
        const tipoActivo = assetTypeSelect.value;
        const categoriaSeleccionada = assetCategorySelect.value;

        if (tipoActivo === "False" || categoriaSeleccionada === "Monitor") {
            nomenclatureField.style.display = 'none';
            document.getElementById('nomenclature-textarea').value = '';
        } else {
            nomenclatureField.style.display = 'block';
        }
    }

    assetTypeSelect.addEventListener('change', function () {
        actualizarCategorias(this.value);
        toggleNomenclature();
    });

    assetCategorySelect.addEventListener('change', toggleNomenclature);

    toggleNomenclature();
    actualizarCategorias(assetTypeSelect.value);
});