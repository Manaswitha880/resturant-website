let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(item, price) {
  cart.push({ item, price });
  localStorage.setItem("cart", JSON.stringify(cart));
  alert(item + " added to cart!");
}

function displayCart() {
  let cartItems = document.getElementById("cart-items");
  let cartTotal = document.getElementById("cart-total");
  if (!cartItems || !cartTotal) return;

  cartItems.innerHTML = "";
  let total = 0;
  cart.forEach((c, index) => {
    let li = document.createElement("li");
    li.textContent = `${c.item} - ₹${c.price}`;
    cartItems.appendChild(li);
    total += c.price;
  });
  cartTotal.textContent = total;
}

window.onload = displayCart;
