window.onload = function () {
    const path = window.location.pathname;
    const navButtons = {
        '/': 'dashboardBtn',
        '/alerts': 'alertsBtn',
        '/logs': 'logsBtn'
    };

    // Highlight active nav button
    if (navButtons[path]) {
        const btn = document.getElementById(navButtons[path]);
        if (btn) btn.classList.add('active');
    }

    // Setup chart instances
    let pieChart;
    let lineChart;

    const pieCtx = document.getElementById('threatChart')?.getContext('2d');
    const lineCtx = document.getElementById('logTrendChart')?.getContext('2d');

    // Pie Chart (Threat Breakdown)
    function updatePieChart(threatData) {
        if (!pieCtx) return;
        if (pieChart) pieChart.destroy();

        pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(threatData),
                datasets: [{
                    data: Object.values(threatData),
                    backgroundColor: ['#ff7f7f', '#ffb74d', '#7fbeff', '#7fff7f'],
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            font: { size: 14, weight: 'bold' }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (tooltipItem) {
                                return `${tooltipItem.label}: ${tooltipItem.raw}`;
                            }
                        }
                    }
                }
            }
        });
    }

    // Line Chart (Logs Per Minute)
    function updateLineChart(labels, values) {
        if (!lineCtx) return;
        if (lineChart) lineChart.destroy();

        lineChart = new Chart(lineCtx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Logs per Minute',
                    data: values,
                    borderColor: '#00ffe4',
                    backgroundColor: 'rgba(0, 255, 228, 0.2)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: { display: true, text: 'Time (minutes)', color: '#ccc' },
                        ticks: { color: '#aaa' }
                    },
                    y: {
                        title: { display: true, text: 'Log Count', color: '#ccc' },
                        ticks: { color: '#aaa' },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        labels: { color: '#ccc', font: { weight: 'bold' } }
                    }
                }
            }
        });
    }

    // Fetch total stats + update pie chart
    function fetchTotalStats() {
        fetch('/api/total_stats')
            .then(res => res.json())
            .then(data => {
                document.getElementById("total-logs").textContent = `Total Logs: ${data.total_logs}`;
                document.getElementById("total-alerts").textContent = `Total Alerts: ${data.total_alerts}`;
                document.getElementById("active-ip-blocks").textContent = `Active IP Blocks: ${data.active_ip_blocks}`;
                updatePieChart(data.threat_category_breakdown); // if it's returned from backend
            })
            .catch(err => console.error("Stats fetch error:", err));
    }

    // Fetch live line graph data
    function fetchLogChartData() {
        fetch('/api/log_chart')
            .then(res => res.json())
            .then(data => {
                updateLineChart(data.labels, data.values);
            })
            .catch(err => console.error("Chart fetch error:", err));
    }

    // Logs & Alerts (for Alerts/Logs Page)
    function fetchLogs() {
        fetch('/api/logs')
            .then(res => res.json())
            .then(data => {
                let container = document.getElementById("log-container");
                if (!container) return;
                container.innerHTML = "";
                data.forEach(log => {
                    let p = document.createElement("p");
                    p.classList.add("log-entry");
                    p.textContent = `[${log.timestamp}] ${log.ip} - ${log.message}`;
                    container.appendChild(p);
                });
                container.scrollTop = container.scrollHeight;
            })
            .catch(err => console.error("Logs fetch error:", err));
    }

    function fetchAlerts() {
        fetch('/api/alerts')
            .then(res => res.json())
            .then(data => {
                let container = document.getElementById("alert-container");
                if (!container) return;
                container.innerHTML = "";
                data.forEach(alert => {
                    let p = document.createElement("p");
                    p.classList.add("alert-entry");
                    p.innerHTML = `<strong>[ALERT]</strong> ${alert.timestamp} - ${alert.message}`;
                    p.style.color = "red";
                    container.appendChild(p);
                });
                container.scrollTop = container.scrollHeight;
            })
            .catch(err => console.error("Alerts fetch error:", err));
    }

    // Call once + set interval every 5s
    fetchTotalStats();
    fetchLogChartData();
    fetchLogs();
    fetchAlerts();

    setInterval(fetchTotalStats, 5000);
    setInterval(fetchLogChartData, 5000);
    setInterval(fetchLogs, 5000);
    setInterval(fetchAlerts, 5000);
};
