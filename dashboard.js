function renderPerformanceChart(
      labels,
      scores
  ) {
  
      const canvas =
          document.getElementById(
              "performanceChart"
          );
  
      if (!canvas) {
          return;
      }
  
      new Chart(
          canvas,
          {
              type: "line",
  
              data: {
  
                  labels: labels,
  
                  datasets: [
  
                      {
                          label:
                              "Interview Score",
  
                          data: scores,
  
                          borderWidth: 3,
  
                          tension: 0.4,
  
                          fill: false,
  
                          pointRadius: 5
                      }
  
                  ]
  
              },
  
              options: {
  
                  responsive: true,
  
                  scales: {
  
                      y: {
  
                          beginAtZero: true,
  
                          max: 100
  
                      }
  
                  }
  
              }
  
          }
      );
  }