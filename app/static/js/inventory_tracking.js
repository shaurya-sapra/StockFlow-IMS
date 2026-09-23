document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('table-body');
    const searchBar = document.getElementById('search-bar');
    const categorySelect = document.getElementById('category-select');
    const sortSelect = document.getElementById('sort-select');
    const modal = document.getElementById('modal');
    const modalText = document.getElementById('modal-text');
    const closeModal = document.querySelector('.close');

    let products = []; // Store fetched products

    // Fetch products from the server
    function fetchProducts() {
        fetch('/api/products')
            .then(response => response.json())
            .then(data => {
                products = data;
                renderTable(products);
            })
            .catch(error => console.error('Error fetching products:', error));
    }

    // Mapping of product names to image file paths
    const productImages = {
        "Orange": "static/images/products/orange.png",
        "Mango": "static/images/products/mango.png",
        "Cucumber": "static/images/products/cucumber.png",
        "Milk": "static/images/products/milk.png",
        "Cheese": "static/images/products/cheese.png",
        "Eggs": "static/images/products/eggs.png",
        "Chicken": "static/images/products/chicken.png",
        "Lamb": "static/images/products/lamb.png",
        "Duck": "static/images/products/duck.png",
        "Popcorn": "static/images/products/popcorn.png",
        "Crisps": "static/images/products/crisps.png",
        "Pretzels": "static/images/products/pretzels.png",
        "Bread": "static/images/products/bread.png",
    };

    // Function to get the image URL
    function getProductImage(productName) {
        return productImages[productName] || "static/images/products/default.png";
    }

    // Render table rows
    function renderTable(data) {
        tableBody.innerHTML = ''; // Clear existing rows
        data.forEach(product => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${product.product_id}</td>
                <td>${product.name}</td>
                <td><img src="${getProductImage(product.name)}" alt="${product.name}" width="50"></td>
                <td>£${product.price.toFixed(2)}</td>
                <td>${product.stock}</td>
                <td>
                    <button class="edit-stock" data-id="${product.product_id}">Edit Stock</button>
                    <button class="view-details" data-id="${product.product_id}">View Details</button>
                </td>
            `;
            tableBody.appendChild(row);
        });

        // Add event listeners to buttons
        document.querySelectorAll('.edit-stock').forEach(button => {
            button.addEventListener('click', () => {
                const product = products.find(p => p.product_id == button.dataset.id);
                openEditStockModal(product); // Open the Edit Stock modal
            });
        });

        document.querySelectorAll('.view-details').forEach(button => {
            button.addEventListener('click', () => {
                const product = products.find(p => p.product_id == button.dataset.id);
                openViewDetailsModal(product); // Open the View Details modal
            });
        });
    }

    // Function to open Edit Stock
    function openEditStockModal(product) {
        modalText.innerText = `Edit Stock for ${product.name}`;
        modal.style.display = 'flex';

        // Add the Edit Stock form
        const modalContent = document.querySelector('.modal-content');
        modalContent.innerHTML = `
            <span class="close">&times;</span>
            <p>Edit Stock for ${product.name}</p>
            <form id="edit-stock-form">
                <label for="stock-input">Stock:</label>
                <input type="number" id="stock-input" name="stock" min="0" required>
                <button type="submit">Update</button>
            </form>
        `;

        // Pre-fill the current stock value in form
        document.getElementById('stock-input').value = product.stock;

        const editStockForm = document.getElementById('edit-stock-form');
        editStockForm.onsubmit = async (e) => {
            e.preventDefault(); // Prevent default/empty form submission

            const newStock = parseInt(document.getElementById('stock-input').value);

            try {
                const response = await fetch(`/api/update_stock/${product.product_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ stock: newStock }),
                });

                if (response.ok) {
                    alert('Stock updated successfully!');
                    fetchProducts(); // Refresh the table
                    modal.style.display = 'none'; // Close the screen
                } else {
                    const errorData = await response.json();
                    alert(`Failed to update stock: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Error updating stock:', error);
                alert('An error occurred while updating stock.');
            }
        };

        // Add event listener to close button
        document.querySelector('.close').addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // Function to open the View Details screen
    function openViewDetailsModal(product) {
        modalText.innerText = `View Details for ${product.name}`;
        modal.style.display = 'flex';

        // Clear any existing form and add the View Details form
        const modalContent = document.querySelector('.modal-content');
        modalContent.innerHTML = `
            <span class="close">&times;</span>
            <p>View Details for ${product.name}</p>
            <form id="view-details-form">
                <label for="price-input">Price:</label>
                <input type="number" id="price-input" name="price" step="0.01" required>

                <label for="weight-input">Weight (g):</label>
                <input type="number" id="weight-input" name="weight" step="0.1" required>

                <label for="calories-input">Calories:</label>
                <input type="number" id="calories-input" name="calories" required>

                <label for="carbs-input">Carbs (g):</label>
                <input type="number" id="carbs-input" name="carbs" step="0.1" required>

                <label for="protein-input">Protein (g):</label>
                <input type="number" id="protein-input" name="protein" step="0.1" required>

                <label for="fat-input">Fat (g):</label>
                <input type="number" id="fat-input" name="fat" step="0.1" required>

                <label for="expiry-date-input">Expiry Date:</label>
                <input type="date" id="expiry-date-input" name="expiry_date" required>

                <label for="supplier-input">Supplier:</label>
                <input type="text" id="supplier-input" name="supplier" required>

                <button type="submit">Update</button>
            </form>
        `;

        // Fetch product details and populate the form
        fetch(`/api/product_details/${product.product_id}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('price-input').value = data.price;
                document.getElementById('weight-input').value = data.weight;
                document.getElementById('calories-input').value = data.calories;
                document.getElementById('carbs-input').value = data.carbs;
                document.getElementById('protein-input').value = data.protein;
                document.getElementById('fat-input').value = data.fat;
                document.getElementById('expiry-date-input').value = data.expiry_date;
                document.getElementById('supplier-input').value = data.supplier;
            })
            .catch(error => console.error('Error fetching product details:', error));

        const viewDetailsForm = document.getElementById('view-details-form');
        viewDetailsForm.onsubmit = async (e) => {
            e.preventDefault(); // Prevent default/empty form submission

            const updatedProduct = {
                product_id: product.product_id,
                price: parseFloat(document.getElementById('price-input').value),
                weight: parseFloat(document.getElementById('weight-input').value),
                calories: parseInt(document.getElementById('calories-input').value),
                carbs: parseFloat(document.getElementById('carbs-input').value),
                protein: parseFloat(document.getElementById('protein-input').value),
                fat: parseFloat(document.getElementById('fat-input').value),
                expiry_date: document.getElementById('expiry-date-input').value,
                supplier: document.getElementById('supplier-input').value,
            };

            try {
                const response = await fetch(`/api/update_product/${product.product_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(updatedProduct),
                });

                if (response.ok) {
                    alert('Product updated successfully!');
                    fetchProducts(); // Refresh the table
                    modal.style.display = 'none'; // Close the screen
                } else {
                    const errorData = await response.json();
                    alert(`Failed to update product: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Error updating product:', error);
                alert('An error occurred while updating the product.');
            }
        };

        // Add event listener to close button
        document.querySelector('.close').addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // Close screen
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Filter and sort functionality
    function filterAndSort() {
        let filteredProducts = products;

        // Search by product name
        const searchTerm = searchBar.value.toLowerCase();
        if (searchTerm) {
            filteredProducts = filteredProducts.filter(product =>
                product.name.toLowerCase().includes(searchTerm)
            );
        }

        // Filter by category
        const selectedCategory = categorySelect.value;
        if (selectedCategory !== 'all') {
            filteredProducts = filteredProducts.filter(product =>
                product.category === selectedCategory
            );
        }

        // Sort by price
        const sortOption = sortSelect.value;
        if (sortOption === 'low-high') {
            filteredProducts.sort((a, b) => a.price - b.price);
        } else if (sortOption === 'high-low') {
            filteredProducts.sort((a, b) => b.price - a.price);
        }

        renderTable(filteredProducts);
    }

    // Event listeners for search, filter, and sort
    searchBar.addEventListener('input', filterAndSort);
    categorySelect.addEventListener('change', filterAndSort);
    sortSelect.addEventListener('change', filterAndSort);

    // Initial fetch
    fetchProducts();
});