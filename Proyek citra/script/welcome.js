document.addEventListener("DOMContentLoaded", () => {
    // Animasi masuk untuk teks section (fade dan translate)
    const textSection = document.querySelector(".text-section");
    textSection.style.opacity = 0;
    textSection.style.transform = "translateY(30px)";
    
    setTimeout(() => {
        textSection.style.transition = "all 0.8s ease-out";
        textSection.style.opacity = 1;
        textSection.style.transform = "translateY(0)";
    }, 300);

    // Efek hover untuk tombol
    const button = document.querySelector(".btn");
    button.addEventListener("mouseover", () => {
        button.style.boxShadow = "0 8px 16px rgba(0,0,0,0.3)";
    });
    button.addEventListener("mouseout", () => {
        button.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.2)";
    });

    // Animasi gambar muncul satu per satu
    const images = document.querySelectorAll(".image-container");
    images.forEach((img, index) => {
        img.style.opacity = 0;
        img.style.transform = "scale(0.8)";
        setTimeout(() => {
            img.style.transition = "all 0.8s ease";
            img.style.opacity = 1;
            img.style.transform = "scale(1)";
        }, 500 + index * 300);
    });

    // Efek mengetik (typing effect)
    const heading = document.querySelector(".text-section h1");
    const fullText = heading.innerText;
    heading.innerText = "";
    let index = 0;

    function typeEffect() {
        if (index < fullText.length) {
            heading.innerText += fullText.charAt(index);
            index++;
            setTimeout(typeEffect, 100); // kecepatan mengetik
        }
    }

    setTimeout(() => {
        typeEffect(); // mulai efek mengetik setelah teks fade-in
    }, 1000);
});
