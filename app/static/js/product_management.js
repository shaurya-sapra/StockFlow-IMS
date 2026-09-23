document.addEventListener('DOMContentLoaded', function () {
    const addProductBtn = document.getElementById('add-product-btn');
    const addProductForm = document.getElementById('add-product-form');
    const productForm = document.getElementById('product-form');
    const deleteProductBtn = document.getElementById('delete-product-btn');
    const deleteProductForm = document.getElementById('delete-product-form');
    const deleteForm = document.getElementById('delete-form');
    const productSelect = document.getElementById('product-select');

    // Show the Add Product form
    addProductBtn.addEventListener('click', () => {
        addProductForm.style.display = 'block';
    });

    // Add Product form submission
    productForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default/empty form submission

        // Create new product object from form data
        const newProduct = {
            category: document.getElementById('category-select').value,
            name: document.getElementById('product-name').value,
            price: parseFloat(document.getElementById('price').value),
            weight: parseFloat(document.getElementById('weight').value),
            calories: parseInt(document.getElementById('calories').value),
            carbs: parseFloat(document.getElementById('carbs').value),
            protein: parseFloat(document.getElementById('protein').value),
            fat: parseFloat(document.getElementById('fat').value),
            expiry_date: document.getElementById('expiry-date').value,
            supplier: document.getElementById('supplier').value,
            stock: parseInt(document.getElementById('stock').value),
            date_added: document.getElementById('date-added').value,
        };

        try {
            // Send POST request to add product
            const response = await fetch('/api/add_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newProduct),
            });

            if (response.ok) {
                alert('Product added successfully!');
                addProductForm.style.display = 'none'; // Hide the form
                productForm.reset(); // Clear the form
                fetchProducts(); // Refresh the product list
            } else {
                const errorData = await response.json();
                alert(`Failed to add product: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error adding product:', error);
        }
    });

    // Show the Delete Product form
    deleteProductBtn.addEventListener('click', () => {
        // Fetch products and populate the dropdown
        fetch('/api/products')
            .then(response => response.json())
            .then(data => {
                productSelect.innerHTML = ''; // Clear existing options

                // Add options for each product
                data.forEach(product => {
                    const option = document.createElement('option');
                    option.value = product.product_id;
                    option.textContent = product.name;
                    productSelect.appendChild(option);
                });

                deleteProductForm.style.display = 'block'; // Show the form
            })
            .catch(error => console.error('Error fetching products:', error));
    });

    // Delete Product form submission
    deleteForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default/empty form submission

        const productId = productSelect.value; // Get selected product ID

        try {
            // Send DELETE request to delete product
            const response = await fetch(`/api/delete_product/${productId}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                alert('Product deleted successfully!');
                deleteProductForm.style.display = 'none'; // Hide the form
                fetchProducts(); // Refresh the product list
            } else {
                const errorData = await response.json();
                alert(`Failed to delete product: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error deleting product:', error);
        }
    });
});