<<<<<<< HEAD
let scale = 1.0;
const img = document.getElementById('zoom-image');

function zoomIn() {
    scale += 0.1;
    applyZoom();
}

function zoomOut() {
    if (scale > 0.2) {
        scale -= 0.1;
        applyZoom();
    }
}

function resetZoom() {
    scale = 1.0;
    applyZoom();
}

function applyZoom() {
    img.style.transform = `scale(${scale})`;
    img.style.transformOrigin = 'center';
}

=======
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
>>>>>>> 61137ae9c0fc972839ef5a5dbd218075c2337226
