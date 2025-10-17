async function loadJson(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();

    return result;
}

function loadConfiguration() {
    return async () => {
        try {
            const data = await loadJson('http://localhost:8000/defaultShyftConfig.json');
            const tbody = document.getElementById('mappingData');
            tbody.innerHTML = ''; // clear any existing rows

            for (const [key, value] of Object.entries(data)) {
                const row = document.createElement('tr');
                const keyCell = document.createElement('td');
                const valueCell = document.createElement('td');
                const inputValue = document.createElement('input');
                valueCell.appendChild(inputValue);

                keyCell.textContent = key;
                inputValue.value = value;

                row.appendChild(keyCell);
                row.appendChild(valueCell);
                tbody.appendChild(row);
            }
        } catch (err) {
        }
    };
}

function setup() {
    const btn = document.getElementById('showConfig');

    btn.addEventListener('click', loadConfiguration());
}

// wait until DOM is ready
window.addEventListener('DOMContentLoaded', setup);