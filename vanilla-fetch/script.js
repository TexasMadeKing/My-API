// const element = document.querySelector('.all-truck-items');
// console.log(element);

const element = document.querySelectorAll = new JSDOM(html).window.document;

const jsdom = require("jsdom");
const { JSDOM } = jsdom;

// fetch("http://127.0.0.1:5000/food/get")
//     .then((response) => response.json())
//     .then((response) => {
//         response.map((item) => {
//             const newItemElement = document.createElement("div");
//             const newItemText = document.createTextNode(`${item.title}`);
//             const newItemPrice = document.createTextNode(`${item.price}`);
//             newItemElement.appendChild(newItemText);
//             newItemElement.appendChild(newItemPrice);
//             newItemElement.classList.add("food-item", `${item.menu_type}`);



//             element.appendChild(newItemElement);

//         });
//     });

fetch("http://127.0.0.1:5000/truck/get")
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













