const outsideHomeAssistant = "http://localhost:8000/0";
const insideHomeAssistant = window.location.pathname;
const configUri = insideHomeAssistant + "/config";
const toggleUri = insideHomeAssistant + "/togglewaterheater";
const sensorIdsUri = insideHomeAssistant + "/sensorids";
let configData = {}

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

async function postJson(url, data) {
    const response = await fetch(url, {
        method: "POST",
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
        for (const [key] of Object.entries(configData)) {
            document.getElementById(key + VALUE_POSTFIX);
            toBeWritten[key] = document.getElementById(key + VALUE_POSTFIX).value;
        }

        await putJson(configUri, toBeWritten);
    }
}

function toggleHeating() {
    return async () => {
        await postJson(toggleUri, {});
    }
}

function loadConfiguration() {
    return async () => {
        try {
            console.log("loadConfiguration called");
            const configData = await getJson(configUri);
            const sensorIds = await getJson(sensorIdsUri);
            const tbody = document.getElementById('mappingData');
            const sensorIdsGUIElement = document.getElementById('sensorIds');
            tbody.innerHTML = '';
            for (const sensorId of sensorIds) {
                const option = document.createElement("option");
                option.value = sensorId;
                sensorIdsGUIElement.appendChild(option);
            }

            for (const [key, value] of Object.entries(configData)) {
                const row = document.createElement('tr');
                const keyCell = document.createElement('td');
                keyCell.textContent = key;

                const inputValue = document.createElement('input');
                inputValue.id = key + VALUE_POSTFIX;
                inputValue.value = value;
                inputValue.setAttribute("list", "sensorIds");

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
    const toggleHeatingButton = document.getElementById('toggleHeating');

    showConfigButton.addEventListener('click', loadConfiguration());
    saveConfigButton.addEventListener('click', saveConfiguration());
    toggleHeatingButton.addEventListener('click', toggleHeating());
}

// wait until DOM is ready
window.addEventListener('DOMContentLoaded', setup);