document.addEventListener('DOMContentLoaded', function () {

    // Fetch and display total products
    fetchTotalProducts();

    // Fetch and display total stock
    fetchTotalStock();

    // Fetch and render donut chart
    fetchCategoryDistribution();

    // Fetch and render line chart
    fetchStockHistory();
});

// Fetch total products
function fetchTotalProducts() {
    fetch('/api/total_products')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-products').textContent = data.total_products;
        })
        .catch(error => console.error('Error fetching total products:', error));
}

// Fetch total stock
function fetchTotalStock() {
    fetch('/api/total_stock')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-stock').textContent = data.total_stock;
        })
        .catch(error => console.error('Error fetching total stock:', error));
}

// Fetch category distribution and render a donut chart
function fetchCategoryDistribution() {
    fetch('/api/category_distribution')
        .then(response => response.json())
        .then(data => {

            const donutCtx = document.getElementById('donut-chart').getContext('2d');
            new Chart(donutCtx, {
                type: 'doughnut',
                data: {
                    labels: data.categories,
                    datasets: [{
                        label: 'Products by Category',
                        data: data.counts,
                        backgroundColor: [
                            '#FF6B6B', '#6A0572', '#F9C74F', '#43AA8B', '#2D6A4F'
                        ],
                        borderWidth: 1,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {
                        padding: 20
                    },
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching category distribution:', error));
}

// Fetch stock history and render a line chart
function fetchStockHistory() {
    fetch('/api/stock_history')
        .then(response => response.json())
        .then(data => {

            const lineCtx = document.getElementById('line-chart').getContext('2d');
            new Chart(lineCtx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Total Stock',
                        data: data.stock,
                        borderColor: '#3A86FF',
                        backgroundColor: 'rgba(58, 134, 255, 0.2)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    layout: {
                        padding: 20
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Date',
                                color: '#333',
                                font: {
                                    weight: 'bold'
                                }
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Stock',
                                color: '#333',
                                font: {
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching stock history:', error));
}