document.addEventListener("DOMContentLoaded", function () {
    const before = document.querySelector(".image-before");
    const after = document.querySelector(".image-after");

    // Inisialisasi: before tampil, after tersembunyi
    before.style.opacity = "1";
    after.style.opacity = "0";

    before.style.zIndex = "2";
    after.style.zIndex = "1";

    before.style.transition = "opacity 1s ease-in-out";
    after.style.transition = "opacity 1s ease-in-out";

    let isBeforeVisible = true;

    setInterval(() => {
        if (isBeforeVisible) {
            before.style.opacity = "0";
            after.style.opacity = "1";
            before.style.zIndex = "1";
            after.style.zIndex = "2";
        } else {
            before.style.opacity = "1";
            after.style.opacity = "0";
            before.style.zIndex = "2";
            after.style.zIndex = "1";
        }

        isBeforeVisible = !isBeforeVisible;
    }, 5000); // Ganti gambar setiap 5 detik
});

