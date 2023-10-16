document.addEventListener('DOMContentLoaded', () => {
    const navElements = document.querySelectorAll('.accrete-navbar-menu');
    const burger = document.getElementById('navbar-burger');
    navElements.forEach(el => {
        el.addEventListener('mousedown', toggleNavDropDown);
        el.addEventListener('blur', deactivateNavDropDown);
        el.classList.add('is-hoverable');
    })
    burger.addEventListener('click', toggleHamburger)
})


function toggleHamburger() {
    const burgerElements = document.querySelectorAll('.accrete-burger');
    burgerElements.forEach(el => {
        el.classList.toggle('is-active');
    })
}


function toggleNavDropDown() {
    const active = this.classList.toggle('is-active');
    if (active) {
        this.setAttribute('tabindex', '0');
    } else {
        this.removeAttribute('tabindex');
    }
}


function deactivateNavDropDown() {
    this.classList.remove('is-active');
    this.removeAttribute('tabindex');
}