async function loadChartData(chartId, summaryId, type) {
      const response = await fetch("/stats"); // backend /stats endpoint
      const data = await response.json();
      const stats = data[type] // Use specific type or default to overall data

      const ctx = document.getElementById(chartId).getContext('2d');
      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: ['Passed scripts', 'Failed scripts'],
          datasets: [{
            data: [stats.success, stats.failed],
            backgroundColor: ['#90CAF9', '#FF8A80'],
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      });
      document.querySelector(`#${summaryId} .bg-primary`).textContent = stats.success;
      document.querySelector(`#${summaryId} .bg-warning`).textContent = stats.failed;
    }
loadChartData('summary_chart', 'summary', 'summary');
loadChartData('vm_chart', 'vm_summary', 'vm');
loadChartData('container_chart', 'container_summary', 'container');