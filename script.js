let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(item, price) {
  cart.push({ name: item, price: price });
  localStorage.setItem("cart", JSON.stringify(cart));
  alert(item + " added to cart!");
}

function loadCart() {
  let cartList = document.getElementById("cart-list");
  let totalSpan = document.getElementById("total");

  if (cartList) {
    cartList.innerHTML = "";
    let total = 0;
    cart.forEach((item, index) => {
      let li = document.createElement("li");
      li.textContent = `${item.name} - $${item.price.toFixed(2)}`;
      cartList.appendChild(li);
      total += item.price;
    });
    totalSpan.textContent = total.toFixed(2);
  }
}

window.onload = loadCart;


