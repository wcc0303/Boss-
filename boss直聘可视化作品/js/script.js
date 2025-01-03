var html = document.querySelector('html');
var nav_menu = document.querySelector(".nav_menu");
var menu_btn = document.querySelector(".menu_btn");
var animates = document.querySelectorAll('.animate');
var goTop = document.querySelector('.goTop')

var screenWidth = window.screen.width;
var rem = screenWidth / 1920 * 1.25;
html.style.fontSize = rem * 16 + "px";

var targetHeight = window.screen.height * 0.8;

menu_btn.addEventListener("click", function() {
	nav_menu.classList.toggle("active");
	menu_btn.classList.toggle("active");
})

window.addEventListener("scroll", function() {
	var height = document.documentElement.scrollTop || document.body.scrollTop;

	if (height >= 300) {
		goTop.style.display = 'block'
	} else {
		goTop.style.display = 'none'
	}

	animates.forEach(function(animate) {
		var Top = animate.getBoundingClientRect().top
		if (Top <= targetHeight) {
			animate.classList.add('show')
		}
	})
})

goTop.onclick = function() {
	window.scrollTo({
		top: 0,
		behavior: 'smooth'
	})
}