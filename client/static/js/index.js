function getStorageItem(key1, key2=undefined, default_val=undefined) {
    let val = window.localStorage.getItem(key1);

    if (val) {
        if (key2 === undefined) {
            return val;
        } else {
            val = JSON.parse(val);

            if (key2 in val) {
                return val[key2];
            } else {
                return default_val;
            }
        }
    } else {
        return default_val;
    }
}

window.addEventListener('load', (ev) => {
    let codeSelector = document.getElementById('code-selector');
    let typeSelector = document.getElementById('type-selector');
    let dateSelector = document.getElementById('date-selector');
    let strikeSelector = document.getElementById('strike-selector');
    let priceContainer = document.getElementById('price-container');

    let subscribing = false;

    let updateCode = (ev) => {
        typeSelector.value = getStorageItem('cur-option-type', undefined, typeSelector.value);
        window.localStorage.setItem('cur-stock-code', codeSelector.value);
        subscribing = false;
        updateDate(ev);
    };

    let updateDate = (ev) => {
        subscribing = false;
        dateSelector.innerHTML = '';
        strikeSelector.innerHTML = '';
        priceContainer.children[0].innerHTML = '-';
        priceContainer.children[1].innerHTML = '-';
        priceContainer.children[2].innerHTML = '-';
        priceContainer.children[3].innerHTML = '-';

        fetch(`/dates?stock-code=${codeSelector.value}`).then((resp) => resp.json()).then((dates) => {
            if (dates.length) {
                for (let date of dates) {
                    dateSelector.innerHTML += `<option value="${date}">${date}</option>`;
                }

                let date = getStorageItem(codeSelector.value + typeSelector.value, 'expr-date', dateSelector.children[0].value);

                dateSelector.value = dates.includes(date) ? date : dates[0];
                updateStrike(ev);
            } else {
                alert('无日期数据');
            }
        }).catch((err) => {
            alert('获取日期失败');
        });
    };

    let updateStrike = (ev) => {
        subscribing = false;
        strikeSelector.innerHTML = '';
        priceContainer.children[0].innerHTML = '-';
        priceContainer.children[1].innerHTML = '-';
        priceContainer.children[2].innerHTML = '-';
        priceContainer.children[3].innerHTML = '-';

        fetch(`/strikes?stock-code=${codeSelector.value}&expr-date=${dateSelector.value}&option-type=${typeSelector.value}`).then((resp) => resp.json()).then((strikes) => {
            if (strikes.length) {
                let code = getStorageItem(codeSelector.value + typeSelector.value, 'option-code');
                let hasCode = false;

                for (let strike of strikes) {
                    hasCode = hasCode || code == strike.code;
                    console.log(strike.code, code);
                    strikeSelector.innerHTML += `<option value="${strike.code}">${strike.price}</option>`;
                }

                if (hasCode) {
                    strikeSelector.value = code;
                } else {
                    strikeSelector.value = strikeSelector.children[parseInt(strikes.length / 2)].value;
                }

                updateAll(ev);
            } else {
                alert('无行权价数据');
            }
        }).catch((err) => {
            console.log(err);
            alert('获取行权价失败');
        });
    };

    let updateAll = (ev) => {
        window.localStorage.setItem('cur-option-type', typeSelector.value);
        window.localStorage.setItem(codeSelector.value + typeSelector.value, JSON.stringify({
            'expr-date': dateSelector.value,
            'option-code': strikeSelector.value,
        }));

        subscribing = false;
        fetch(`/subscribe?option-code=${strikeSelector.value}`).then((resp) => {subscribing = true;});
    };

    codeSelector.addEventListener('change', updateCode);
    typeSelector.addEventListener('change', updateDate);
    dateSelector.addEventListener('change', updateStrike);
    strikeSelector.addEventListener('change', updateAll);

    codeSelector.value = getStorageItem('cur-stock-code', undefined, codeSelector.value);

    updateCode();

    let updatePrice = () => {
        if (subscribing == false) {
            setTimeout(updatePrice, 100);
        } else {
            fetch('/price').then((resp) => resp.json()).then((resp) => {
                if (resp['code'] != undefined) {

                    priceContainer.children[0].innerHTML = `${resp['Bid'][0][1]}`;
                    priceContainer.children[1].innerHTML = `${resp['Bid'][0][0]}`;
                    priceContainer.children[2].innerHTML = `${resp['Ask'][0][0]}`;
                    priceContainer.children[3].innerHTML = `${resp['Ask'][0][1]}`;
                }

                updatePrice();
            });
        }
    };

    updatePrice();
});

window.addEventListener('beforeunload', (ev) => {
    fetch('/unsubscribe');
});
