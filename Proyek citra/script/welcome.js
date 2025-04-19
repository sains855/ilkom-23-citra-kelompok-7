document.addEventListener("DOMContentLoaded", function () {
    // Grayscale slide
    const before = document.querySelector(".image-before");
    const after  = document.querySelector(".image-after");
    before.style.opacity = "1"; after.style.opacity = "0";
    before.style.zIndex  = "2"; after.style.zIndex  = "1";
    before.style.transition = after.style.transition = "opacity 1s ease-in-out";
    let isBeforeVisible = true;
    setInterval(() => {
      if (isBeforeVisible) {
        before.style.opacity = "0"; before.style.zIndex = "1";
        after.style.opacity  = "1"; after.style.zIndex  = "2";
      } else {
        before.style.opacity = "1"; before.style.zIndex = "2";
        after.style.opacity  = "0"; after.style.zIndex  = "1";
      }
      isBeforeVisible = !isBeforeVisible;
    }, 3000);
  
    // Remove‑bg slide
    const beforeBG = document.querySelector(".image-before-removebg");
    const afterBG  = document.querySelector(".image-after-removebg");
    beforeBG.style.opacity = "1"; afterBG.style.opacity = "0";
    beforeBG.style.zIndex  = "2"; afterBG.style.zIndex  = "1";
    beforeBG.style.transition = afterBG.style.transition = "opacity 1s ease-in-out";
    let showBeforeBG = true;
    setInterval(() => {
      if (showBeforeBG) {
        beforeBG.style.opacity = "0"; beforeBG.style.zIndex = "1";
        afterBG.style.opacity  = "1"; afterBG.style.zIndex  = "2";
      } else {
        beforeBG.style.opacity = "1"; beforeBG.style.zIndex = "2";
        afterBG.style.opacity  = "0"; afterBG.style.zIndex  = "1";
      }
      showBeforeBG = !showBeforeBG;
    }, 3000);
  
  }); 
  
>>>>>>> 240875e14c97cee727b19c690645253c075c7649
