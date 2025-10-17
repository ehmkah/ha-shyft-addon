const dataUri = "http://localhost:8000/0";
let data = {}

async function getJson(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();

    return result;
}

async function putJson(url, data) {
    const response = await fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
}


const VALUE_POSTFIX = "_value";

function saveConfiguration() {
    return async () => {
        const toBeWritten = {};
        for (const [key] of Object.entries(data)) {
            document.getElementById(key + VALUE_POSTFIX);
            toBeWritten[key] = document.getElementById(key + VALUE_POSTFIX).value;
        }

        await putJson(dataUri, toBeWritten);
    }

}

function loadConfiguration() {
    return async () => {
        try {
            data = await getJson(dataUri);
            const tbody = document.getElementById('mappingData');
            tbody.innerHTML = ''; // clear any existing rows

            for (const [key, value] of Object.entries(data)) {
                const row = document.createElement('tr');
                const keyCell = document.createElement('td');
                keyCell.textContent = key;

                const inputValue = document.createElement('input');
                inputValue.id = key + VALUE_POSTFIX;
                inputValue.value = value;

                const valueCell = document.createElement('td');
                valueCell.appendChild(inputValue);

                row.appendChild(keyCell);
                row.appendChild(valueCell);
                tbody.appendChild(row);
            }
        } catch (err) {
        }
    };
}

function setup() {
    const showConfigButton = document.getElementById('showConfig');
    const saveConfigButton = document.getElementById('saveConfig');

    showConfigButton.addEventListener('click', loadConfiguration());
    saveConfigButton.addEventListener('click', saveConfiguration());
}

// wait until DOM is ready
window.addEventListener('DOMContentLoaded', setup);