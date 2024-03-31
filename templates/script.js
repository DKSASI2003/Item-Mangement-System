async function addItem(event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    const itemName = document.getElementById('itemName').value;
    const itemQuantity = document.getElementById('itemQuantity').value;

    try {
        const response = await fetch('/add_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({item_name: itemName, quantity: Number(itemQuantity)}),
        });
        const data = await response.json();
        console.log('Item added:', data);
        fetchItems(); // Refresh the items list
    } catch (error) {
        console.error('Error adding item:', error);
    }
}

async function fetchItems() {
    const response = await fetch('/items');
    const items = await response.json();
    const itemsList = document.getElementById('itemsList');
    itemsList.innerHTML = ''; // Clear the list before adding new items
    items.forEach(item => {
        const itemElement = document.createElement('li');
        itemElement.textContent = `Item ID: ${item.item_id},Item Name: ${item.item_name}, Quantity: ${item.quantity}`;
        itemsList.appendChild(itemElement);
    });
}

async function deleteItem() {
    const itemId = document.getElementById('deleteItemId').value;
    try {
        const response = await fetch(`/delete_item/${itemId}`, {
            method: 'DELETE',
        });
        const data = await response.json();
        console.log(data);
        fetchItems(); // Refresh the items list
    } catch (error) {
        console.error('Error deleting item:', error);
    }
}

async function updateItem() {
    const itemName = document.getElementById('updateItemName').value;
    //const newItemName = document.getElementById('newItemName').value;
    const newItemQuantity = document.getElementById('newItemQuantity').value;

    try {
        const response = await fetch(`/update_item/${itemName}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({quantity: Number(newItemQuantity)}),
        });
        const data = await response.json();
        console.log('Item updated:', data);
        fetchItems(); // Refresh the items list
    } catch (error) {
        console.error('Error updating item:', error);
    }
}

// Initial fetch of items to display
fetchItems();