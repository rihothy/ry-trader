window.addEventListener('load', (ev) => {
    let codeSelector = document.getElementById('code-selector');
    let typeSelector = document.getElementById('type-selector');
    let dateSelector = document.getElementById('date-selector');
    let strikeSelector = document.getElementById('strike-selector');

    let updateDate = () => {
        dateSelector.innerHTML = '';
        strikeSelector.innerHTML = '';

        fetch(`/dates?code=${codeSelector.value}`).then((resp) => resp.json()).then((resp) => {
            if (resp.length) {
                for (let date of resp) {
                    dateSelector.innerHTML += `<option value="${date}">${date}</option>`;
                }

                dateSelector.firstChild.selected = true;
                updateStrike();
            }
        });
    };

    let updateStrike = () => {
        strikeSelector.innerHTML = '';

        fetch(`/strikes?code=${codeSelector.value}&type=${typeSelector.value}&date=${dateSelector.value}`).then((resp) => resp.json()).then((resp) => {
            if (resp.length) {
                for (let strike of resp) {
                    strikeSelector.innerHTML += `<option value="${strike}">${strike}</option>`;
                }

                strikeSelector.children[parseInt(resp.length / 2)].selected = true;
            }
        });
    };

    codeSelector.addEventListener('change', updateDate);
    typeSelector.addEventListener('change', updateDate);
    dateSelector.addEventListener('change', updateStrike);

    updateDate();
});