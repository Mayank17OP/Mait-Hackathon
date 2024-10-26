document.addEventListener('DOMContentLoaded', () => {
    // Add fade-in animation to header
    const header = document.querySelector('header');
    header.classList.add('fade-in');

    // Add slide-in animation to nav links
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach((link, index) => {
        link.style.animationDelay = `${index * 0.1}s`;
        link.classList.add('slide-in');
    });

    // Add fade-in animation to content sections
    const contentSections = document.querySelectorAll('.left-half, .right-half');
    contentSections.forEach((section, index) => {
        section.style.animationDelay = `${0.3 + index * 0.2}s`;
        section.classList.add('fade-in');
    });

    // Add slide-in animation to chatbot
    const chatbot = document.getElementById('chatbot-container');
    chatbot.classList.add('slide-in');
});
