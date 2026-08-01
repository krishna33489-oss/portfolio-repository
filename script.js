const cursorGlow = document.querySelector('.cursor-glow');
const sections = document.querySelectorAll('.section, .hero, .footer');

if (cursorGlow) {
    window.addEventListener('mousemove', (e) => {
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
    });
}

sections.forEach((section, index) => {
    section.classList.add('reveal');
    section.style.transitionDelay = `${index * 120}ms`;
});

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.2 });

sections.forEach((section) => revealObserver.observe(section));

for (let i = 0; i < 6; i++) {
    const orb = document.createElement('span');
    orb.className = 'orb';
    orb.style.width = `${20 + Math.random() * 60}px`;
    orb.style.height = orb.style.width;
    orb.style.left = `${Math.random() * 100}%`;
    orb.style.top = `${Math.random() * 100}%`;
    orb.style.animationDuration = `${10 + Math.random() * 10}s`;
    document.body.appendChild(orb);
}

document.querySelectorAll('.btn').forEach((button) => {
    button.addEventListener('click', (e) => {
        const ripple = document.createElement('span');
        ripple.className = 'ripple';
        const rect = button.getBoundingClientRect();
        ripple.style.left = `${e.clientX - rect.left}px`;
        ripple.style.top = `${e.clientY - rect.top}px`;
        button.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });
});
