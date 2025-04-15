// VM állapotok megjelenítése Chart.js segítségével


const vmChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Running', 'Stopped', 'Idle'],
    datasets: [{
      data: [8, 2, 3], // Módosítsd a számokat, ha szükséges
      backgroundColor: [
        'rgba(40, 167, 69, 0.8)',   // Zöld - Running
        'rgba(220, 53, 69, 0.8)',   // Piros - Stopped
        'rgba(255, 193, 7, 0.8)'    // Sárga - Idle
      ],
      borderColor: ['#fff', '#fff', '#fff'],
      borderWidth: 2
    }]
  },
  options: {
    responsive: true,
    cutout: '60%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#333',
          font: {
            size: 14
          }
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.raw || 0;
            return `${label}: ${value} VM`;
          }
        }
      }
    }
  }
});