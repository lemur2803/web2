var pageScrollPosition = 0;
function upOrDown() {
	if (pageScrollPosition) {
		window.scrollTo(0, pageScrollPosition);
		pageScrollPosition = 0;
	}
	else {
		pageScrollPosition = window.pageYOffset;
		window.scrollTo(0, 0);
	}
}
function loginShow() {
    document.getElementById('login').style.display = 'block';
}
function loginClose() {
    document.getElementById('login').style.display = 'none';
}