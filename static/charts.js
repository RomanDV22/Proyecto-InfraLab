const cpuChart = new Chart(document.getElementById('cpuChart'), {

    type: 'line',

    data: {

        labels: cpuData.map((_, i) => i + 1),

        datasets: [{

            label: 'CPU %',

            data: cpuData

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false

    }

});



const ramChart = new Chart(document.getElementById('ramChart'), {

    type: 'line',

    data: {

        labels: ramData.map((_, i) => i + 1),

        datasets: [{

            label: 'RAM %',

            data: ramData

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false

    }

});



const latenciaChart = new Chart(document.getElementById('latenciaChart'), {

    type: 'line',

    data: {

        labels: latenciaData.map((_, i) => i + 1),

        datasets: [{

            label: 'Latencia ms',

            data: latenciaData

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false

    }

});



function actualizarDashboard(data) {

    document.getElementById("clientes").innerText = data.clientes;

    document.getElementById("requests").innerText = data.requests;

    document.getElementById("metricas").innerText = data.metricas;


    cpuChart.data.datasets[0].data = data.cpu_historial;

    cpuChart.data.labels = data.cpu_historial.map((_, i) => i + 1);


    ramChart.data.datasets[0].data = data.ram_historial;

    ramChart.data.labels = data.ram_historial.map((_, i) => i + 1);


    latenciaChart.data.datasets[0].data = data.latencia_historial;

    latenciaChart.data.labels = data.latencia_historial.map((_, i) => i + 1);


    cpuChart.update();

    ramChart.update();

    latenciaChart.update();

}


function conectarWebSocket() {

    const protocolo = location.protocol === "https:" ? "wss" : "ws";

    const socket = new WebSocket(`${protocolo}://${location.host}/ws/dashboard`);

    socket.onmessage = (evento) => {

        actualizarDashboard(JSON.parse(evento.data));

    };

    socket.onclose = () => {

        setTimeout(conectarWebSocket, 3000);

    };

}


conectarWebSocket();
