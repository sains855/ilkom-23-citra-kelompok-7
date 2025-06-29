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

