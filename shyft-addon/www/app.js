const outsideHomeAssistant = "http://localhost:8000/0";
const insideHomeAssistant = window.location.pathname;
const configUri = insideHomeAssistant + "/config";
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
        console.log("saveConfiguration aufgerufen");
        const sensorValues = {};
        for (const [key] of Object.entries(configData["sensorMappings"])) {
            document.getElementById(key + VALUE_POSTFIX);
            sensorValues[key] = document.getElementById(key + VALUE_POSTFIX).value;
        }
        const actorValues = {};
        for (const [key] of Object.entries(configData["actorMappings"])) {
            document.getElementById(key + VALUE_POSTFIX);
            actorValues[key] = document.getElementById(key + VALUE_POSTFIX).value;
        }

        const toBeWritten = {"sensorMappings" : sensorValues, "actorMappings" : actorValues};
        await putJson(configUri, toBeWritten);
    }
}

function loadConfiguration() {
    return async () => {
        try {
            console.log("loadConfiguration called");
            configData = await getJson(configUri);
            const sensorIds = await getJson(sensorIdsUri);
            const sensorIdsGUIElement = document.getElementById('sensorIds');

            for (const sensorId of sensorIds) {
                const option = document.createElement("option");
                option.value = sensorId;
                sensorIdsGUIElement.appendChild(option);
            }
            renderSensorMappings(configData["sensorMappings"]);
        } catch (err) {
        }
    };
}

function renderSensorMappings(configData) {
    const tbody = document.getElementById('sensorMappingId');
    tbody.innerHTML = '';
    for (const [key, value] of Object.entries(configData)) {
        const row = document.createElement('tr');
        const keyCell = document.createElement('td');
        keyCell.textContent = key;

        const inputValue = document.createElement('input');
        inputValue.id = key + VALUE_POSTFIX;
        inputValue.value = value;
        inputValue.setAttribute("list", "sensorIds");
        inputValue.setAttribute("class", "sensorInput");

        const valueCell = document.createElement('td');
        valueCell.appendChild(inputValue);

        row.appendChild(keyCell);
        row.appendChild(valueCell);
        tbody.appendChild(row);
    }
}


function setup() {
    const showConfigButton = document.getElementById('showConfig');
    const saveConfigButton = document.getElementById('saveConfig');

    showConfigButton.addEventListener('click', loadConfiguration());
    saveConfigButton.addEventListener('click', saveConfiguration());
}

// wait until DOM is ready
window.addEventListener('DOMContentLoaded', setup);