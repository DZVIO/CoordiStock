document.addEventListener('DOMContentLoaded', function () {

    // --- MOVIMIENTO DE ACTIVOS: Mostrar/Ocultar detalles ---
    $('.movement-title').click(function () {
        console.log("Clicked");
        $(this).closest('.member-infos').find('.activoinfo').slideToggle(600);
    });

    $('.activoinfo').each(function () {
        const categoria = $(this).find('tr:has(th:contains("Categoria")) td').text().trim().toLowerCase();
        const tipo = $(this).find('tr:has(th:contains("Tipo")) td').text().trim().toLowerCase();

        if (categoria === "monitor") {
            $(this).find('tr:has(th:contains("Renting")), tr:has(th:contains("Nomenclatura"))').hide();
        }
        if (tipo === "periferico") {
            $(this).find('tr:has(th:contains("Renting")), tr:has(th:contains("Activo"))').hide();
        }
    });

    // --- COMPONENTE DE BÚSQUEDA GENÉRICO ---
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
                            $list.append(`
                                <button type="button" class="list-group-item list-group-item-action" data-id="${item.id}" data-item-data='${JSON.stringify(item)}'>
                                    ${formatItem(item)}
                                </button>`);
                        });
                    }
                }
            });
        }

        $searchInput.on('focus', () => fetchItems());
        $searchInput.on('input', function () {
            fetchItems($(this).val());
        });

        $list.on('click', '.list-group-item', function () {
            const selectedText = $(this).text();
            const selectedId = $(this).data('id');
            const selectedItem = $(this).data('itemData');

            $searchInput.val(selectedText);
            $(`#${hiddenInputId}`).val(selectedId);
            $list.hide();

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

    // --- CONFIGURACIÓN DE BUSCADORES ---
    setupSearchComponent({
        searchInputId: 'terminal-search',
        listContainerId: 'terminal-list',
        hiddenInputId: 'terminal-id',
        apiUrl: '/app/movimiento/terminal_api/',
        formatItem: item => `${item.terminal} - ${item.nombre} - ${item.direccion}`
    });

    setupSearchComponent({
        searchInputId: 'asset-search',
        listContainerId: 'asset-list',
        hiddenInputId: 'asset-id',
        apiUrl: '/app/movimiento/activo_api/',
        getExtraParams: () => {
            const tipo = $('#asset_type').val();
            const categoria = $('#asset_category').val();
            const tipoMov = $('#tipo_mov').val();
            return `&tipo=${tipo}&categoria=${categoria}&tipo_mov=${tipoMov}`;
        },
        formatItem: item => `${item.disponibilidad ? 'Disponible' : 'No disponible'}: ${item.nombre_marca} - ${item.activo} - ${item.modelo} - ${item.n_serie}`
    });

    setupSearchComponent({
        searchInputId: 'agent-search',
        listContainerId: 'agent-list',
        hiddenInputId: 'agent-id',
        apiUrl: '/app/movimiento/agente_api/',
        getExtraParams: () => {
            const activoId = $('#asset-id').val();
            return activoId ? `&activo=${activoId}` : '';
        },
        formatItem: item => `${item.nombre} - ${item.codigo} - ${item.email} - ${item.nombre_area} - ${item.nombre_terminal}`
    });

    setupSearchComponent({
        searchInputId: 'area-search',
        listContainerId: 'area-list',
        hiddenInputId: 'area-id',
        apiUrl: '/app/movimiento/area_api/',
        formatItem: item => `${item.area}`
    });

    // --- ENVÍO DE FORMULARIO: validación y serialización ---
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

    // --- ACTUALIZAR CATEGORÍAS Y MOSTRAR NOMENCLATURA ---
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

    actualizarCategorias(assetTypeSelect.value);
    toggleNomenclature();

    // --- MENSAJE SEGÚN TIPO DE MOVIMIENTO ---
    const tipoMovSelect = document.getElementById('tipo_mov');
    const mensajeAgente = document.getElementById('mensaje-agente');
    const mantenimientoOpciones = document.getElementById('tipo-mantenimiento-opciones');

    const mensajesPorMovimiento = {
        "Asignación": "Seleccione el agente al cual va a asignar el activo",
        "Préstamo": "Seleccione el agente al cual va a prestar el activo",
        "Traslado": "Seleccione el agente al que va destinado el traslado del activo",
        "Devolución": "Seleccione el agente que recibe el equipo",
        "Disposición final": "Seleccione el agente que va a realizar la disposición final del activo",
        "Mantenimiento": "Seleccione el agente responsable del mantenimiento"
    };

    tipoMovSelect.addEventListener('change', function () {
        const movimientoSeleccionado = tipoMovSelect.options[tipoMovSelect.selectedIndex].text.trim();
        const mensaje = mensajesPorMovimiento[movimientoSeleccionado];

        if (mensaje) {
            mensajeAgente.textContent = mensaje;
            mensajeAgente.style.display = 'block';
        } else {
            mensajeAgente.style.display = 'none';
        }

        if (movimientoSeleccionado === "Mantenimiento") {
            mantenimientoOpciones.style.display = 'block';
        } else {
            mantenimientoOpciones.style.display = 'none';
            document.querySelectorAll('input[name="tipo_mantenimiento"]').forEach(radio => radio.checked = false);
        }
    });

    const form = document.getElementById('form-movimiento');

    form.addEventListener('submit', function (event) {
        const movimientoSeleccionado = tipoMovSelect.options[tipoMovSelect.selectedIndex].text.trim();

        if (movimientoSeleccionado === "Mantenimiento") {
            const tipoMantenimientoSeleccionado = document.querySelector('input[name="tipo_mantenimiento"]:checked');
            
            if (!tipoMantenimientoSeleccionado) {
                event.preventDefault();
                Swal.fire({
                    icon: 'warning',
                    title: 'Advertencia',
                    text: 'Debes seleccionar el estado del mantenimiento',
                    confirmButtonText: 'Aceptar'
                });
            }
        }
    });
});