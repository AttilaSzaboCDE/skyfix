document.addEventListener('DOMContentLoaded', () => {
    // Configuration for the VM status chart
    const vm_config = {
    type: 'doughnut',
    data: {
      labels: ['RUNNING', 'IDLE', 'STOPPED'],
      datasets: [{
        data: [70, 20, 10],
        backgroundColor: ['#20c343ff', '#d13628ff', '#FFCE56']
      }]
    },
    options: {
      plugins: {
        legend: {
          position: 'bottom'
        }
      },
      cutout: '70%'
    },
    plugins: [{
      id: 'centerCircle',
      beforeDraw: (chart) => {
        const { width, height, ctx } = chart;
        ctx.save();
        ctx.fillStyle = '#ccc';
        ctx.beginPath();
        ctx.arc(width / 2, height / 2, 30, 0, 2 * Math.PI);
        ctx.fill();
        ctx.restore();
      }
    }]
  };
   // Issues chart configuration
  const issues_config = {
    type: 'doughnut',
    data: {
      labels: ['Resolved', 'Issues'],
      datasets: [{
        data: [55, 45],
        backgroundColor: ['#20c343ff', '#d13628ff']
      }]
    },
    options: {
      plugins: {
        legend: {
          position: 'bottom'
        }
      },
      cutout: '70%'
    },
    plugins: [{
      id: 'centerCircle',
      beforeDraw: (chart) => {
        const { width, height, ctx } = chart;
        ctx.save();
        ctx.fillStyle = '#ccc';
        ctx.beginPath();
        ctx.arc(width / 2, height / 2, 30, 0, 2 * Math.PI);
        ctx.fill();
        ctx.restore();
      }
    }]
  };

  new Chart(document.getElementById('chart1'), vm_config);
  new Chart(document.getElementById('chart2'), issues_config);
});