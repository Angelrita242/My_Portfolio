// script.js — simple interactions: mobile nav, footer year, contact form validation
document.addEventListener('DOMContentLoaded', () => {
  // year in footer
document.getElementById('year').textContent = new Date().getFullYear();

  // mobile nav toggle
const toggle = document.getElementById('nav-toggle');
const nav = document.getElementById('main-nav');

toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    nav.classList.toggle('open');
  });

  // contact form validation only (no mailto)
  const form = document.getElementById('contact-form');
  const status = document.getElementById('form-status');

  form.addEventListener('submit', () => {
    // e.preventDefault(); // prevent default submission

    const name = form.name.value.trim();
    const email = form.email.value.trim();
    const message = form.message.value.trim();

    // clear previous status
    status.textContent = '';

    // validate fields
    if (!name || !email || !message) {
      status.textContent = 'Please fill in all fields.';
      status.style.color = 'red';
      return;
    }

    const emailRegex = /^\S+@\S+\.\S+$/;
    if (!emailRegex.test(email)) {
      status.textContent = 'Please enter a valid email address.';
      status.style.color = 'red';
      return;
    }

    // If all fields are valid
    status.textContent = 'All fields look good!'; 
    status.style.color = 'green';

    // At this point, you can submit to backend (Flask) via fetch/ajax
    // e.g.,
    // fetch('/send', { method: 'POST', body: new FormData(form) });
  });
});