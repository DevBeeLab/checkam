document.addEventListener("DOMContentLoaded", function () {

    const data = window.dashboardData;

    const canvas = document.getElementById("incomeExpenseChart");

    new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: ["Income", "Expense"],
            datasets: [{
                data: [data.income, data.expense],
                backgroundColor: ["#2ecc71", "#e74c3c"]
            }]
        }
    });
});