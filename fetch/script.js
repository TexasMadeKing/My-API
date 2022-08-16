const element = document.querySelector('.all_truck_items');
console.log(element);


fetch("http://127.0.0.1:5000/Food/get")
    .then((response) => response.json())
    .then((response) => {
        response.map((item) => {
            const newItemElement = document.createElement("div");
            const newItemText = document.createTextNode(`${item.title}`);
            const newItemPrice = document.createTextNode(`${item.price}`);
            newItemElement.appendChild(newItemText);
            newItemElement.appendChild(newItemPrice);
            newItemElement.classList.add("truck-item", `${item.menu_type}`);



            element.appendChild(newItemElement);

        });
    });













