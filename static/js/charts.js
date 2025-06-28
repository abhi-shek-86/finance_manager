function renderCharts(monthlyData, categoryData) {
  // Format Monthly Chart Data
  const monthlyLabels = monthlyData.map(row => row.month);
  const monthlyValues = monthlyData.map(row => row.total);

  const monthlyCtx = document.getElementById("monthlyChart").getContext("2d");
  new Chart(monthlyCtx, {
    type: "bar",
    data: {
      labels: monthlyLabels,
      datasets: [{
        label: "Monthly Total",
        data: monthlyValues,
        backgroundColor: "#858796",
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: "Monthly Income/Expenses",
        }
      }
    },
  });

  // Format Category Pie Chart
  const catLabels = categoryData.map(row => row.category);
  const catValues = categoryData.map(row => row.total);

  const categoryCtx = document.getElementById("categoryChart").getContext("2d");
  new Chart(categoryCtx, {
    type: "pie",
    data: {
      labels: catLabels,
      datasets: [{
        label: "Top Categories",
        data: catValues,
        backgroundColor: [
          "#1cc88a",
          "#36b9cc",
          "#f6c23e",
          "#e74a3b",
          "#858796"
        ],
      }],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Top 5 Expense Categories",
        }
      }
    },
  });
}
