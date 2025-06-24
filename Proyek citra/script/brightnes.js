const slider = document.getElementById("brightness-slider");
const preview = document.getElementById("preview");
const brightnessValue = document.getElementById("brightness-value");
const uploadInput = document.getElementById("upload");

slider.addEventListener("input", () => {
  const value = slider.value;
  preview.style.filter = `brightness(${value}%)`;
  brightnessValue.textContent = `${value}%`;
});

uploadInput.addEventListener("change", (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

function uploadImage() {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  const img = new Image();
  img.src = preview.src;
  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.filter = `brightness(${slider.value}%)`;
    ctx.drawImage(img, 0, 0);

    canvas.toBlob((blob) => {
      const formData = new FormData();
      formData.append("image", blob, "adjusted.png");
      fetch("/adjust", {
        method: "POST",
        body: formData
      }).then(res => res.blob()).then(blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "brightness-adjusted.png";
        a.click();
      });
    }, "image/png");
  };
}
