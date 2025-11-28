const outsideHomeAssistant = "http://localhost:8000/0";
const insideHomeAssistant = window.location.pathname;
const configUri = insideHomeAssistant + "/config";
const sensorIdsUri = insideHomeAssistant + "/sensorids";
let configData = {}

const helpinformation = {
    "photovoltaic_powerflow_pv" : {
        "label": "Aktueller Strom - Netz",
        "description" :"Die aktuelle Leistung (in kW), die dein Haushalt aus dem öffentlichen Stromnetz bezieht bzw. dorthin einspeist."
    }
}

/**
    Aktueller Strom - Haushalt, Die Leistung (in kW), die dein Haushalt aktuell verbraucht.

    Aktueller Strom - PV, Die aktuelle Leistung (in kW) deiner PV-Anlage.

    Aktueller Strom - Netz, Die aktuelle Leistung (in kW), die dein Haushalt aus dem öffentlichen Stromnetz bezieht bzw. dorthin einspeist.

    Aktueller Strom - Batterie, Die aktuelle Leistung (in kW), mit dem deine Batterie geladen (positiver Wert) oder entladen (negativer Wert) wird.

    Ladestand, Aktueller Ladestand deiner Batterie in Prozent.

    Batterie: Steuerungsmodus, Der Modus, in den deine Batterie versetzt werden kann (z.B. Eigenverbrauchsoptimierung, Netzladen)

Batterie: Aktuelle max. Ladeleistung, Leistung (in kW), die an der Batterie als aktuelle Begrenzung für die Ladeleistung eingestellt ist.

    Batterie: Max. Entladeleistung, Mit wieviel Leistung (in kW) darf deine Batterie höchstens entladen werden?

    Temperatur Warmwassertank, Die aktuelle Temperatur im Warmwassertank (in °C)

Warmwassermodus aktiviert? An/Aus, je nachdem ob an deiner Wärmepumpe die Warmwasserbereitung aktiviert ist oder nicht.

    Warmwasser gerade erwärmt? An / Aus, je nachdem ob deine Wärmepumpe gerade Brauchwasser erwärmt oder nicht.

Zieltemperatur (aktuell), Gewünschte Raumtemperatur in °C, die du an deiner Wärmepumpe einstellst. Über die stündliche Anpassung dieses Werte steuert Shyft die Leistung deiner Wärmepumpe.

    Heizung aktiviert?, Ja / Nein, je nachdem, ob du die Heizung an deiner Wärmepumpe aktiviert hast oder nicht.

    Aktuelle Leistung Wärmepumpe (elektrisch), in kW

Wärmepumpe an/aus, An/Aus, je nachdem ob deine Wärmepumpe gerade läuft oder aus ist.

    Innenraumtemperatur gemessen, Tatsächlich gemessene Innenraumtemperatur in °C. Für diesen Sensor musst du einen Temperatursensor mit Shyft verbinden.

    Verbindungsstatus, Ja / Nein, je nachdem ob der Ladestecker deiner Wallbox im Auto eingesteckt ist oder nicht.

    Auto - Ladestrom, Aktueller Ladestrom (in kW)

EV - SOC, Ladestand deines Autos (in %)

        ]

}
**/

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
            sensorValues[key] = document.getElementById(key + VALUE_POSTFIX).value;
        }
        const actorValues = configData["actorMappings"];

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
        const context = helpinformation[key] ?? {'label':key};
        const label = context.label;
        keyCell.textContent = label;

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