// Efek fade-in saat halaman pertama kali dimuat
document.addEventListener("DOMContentLoaded", function () {
    // Tambahkan class fade ke body
    const body = document.body;
    body.style.opacity = "0";
    body.style.transition = "opacity 1.5s ease-in-out";

    // Jalankan fade-in
    requestAnimationFrame(() => {
        body.style.opacity = "1";
    });
});
