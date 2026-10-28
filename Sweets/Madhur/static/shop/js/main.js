document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(isOpen));
      toggle.textContent = isOpen ? "✕" : "☰";
    });
  }

  // Small confirmation before submitting an order form.
  const orderForm = document.querySelector(".order-form");
  if (orderForm) {
    orderForm.addEventListener("submit", (event) => {
      const quantity = Number(orderForm.querySelector('[name="quantity_kg"]')?.value || 0);
      if (quantity < 0.25) {
        event.preventDefault();
        alert("Please order at least 0.25 kg.");
      }
    });
  }
});
