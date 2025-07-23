
const response = pm.response.json();


const currentTimestamp = Math.floor(Date.now() / 1000);


const activeMaintenances = response.result.filter(maintenance => {
    return maintenance.active_since <= currentTimestamp && maintenance.active_till >= currentTimestamp;
});


console.log("Mantenimientos activos:", activeMaintenances);


pm.variables.set("active_maintenances", JSON.stringify(activeMaintenances));

if (activeMaintenances.length > 0) {
    console.log("Hay " + activeMaintenances.length + " mantenimientos activos.");
} else {
    console.log("No hay mantenimientos activos.");
}