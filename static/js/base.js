const menuButton = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

menuButton.addEventListener("click", () => {
	const isOpen = navLinks.classList.toggle("active");

	menuButton.setAttribute("aria-expanded", String(isOpen));
});
