document.addEventListener("DOMContentLoaded", function() {
  // Grayscale image transition
  const grayscaleBefore = document.querySelector('.feature-card:nth-child(1) .before-image');
  const grayscaleAfter = document.querySelector('.feature-card:nth-child(1) .after-image');
  
  // Remove BG image transition
  const removeBgBefore = document.querySelector('.feature-card:nth-child(2) .before-image');
  const removeBgAfter = document.querySelector('.feature-card:nth-child(2) .after-image');
  
  function toggleImages(before, after) {
      const currentOpacity = parseFloat(window.getComputedStyle(before).opacity);
      
      if (currentOpacity === 1) {
          before.style.opacity = '0';
          after.style.opacity = '1';
      } else {
          before.style.opacity = '1';
          after.style.opacity = '0';
      }
  }
  
  // Set initial states
  grayscaleBefore.style.opacity = '1';
  grayscaleAfter.style.opacity = '0';
  removeBgBefore.style.opacity = '1';
  removeBgAfter.style.opacity = '0';
  
  // Set intervals for automatic transitions
  setInterval(() => {
      toggleImages(grayscaleBefore, grayscaleAfter);
  }, 3000);
  
  setInterval(() => {
      toggleImages(removeBgBefore, removeBgAfter);
  }, 3000);
  
  // Add hover effect for manual control
  const featureCards = document.querySelectorAll('.feature-card');
  featureCards.forEach(card => {
      card.addEventListener('mouseenter', function() {
          const before = this.querySelector('.before-image');
          const after = this.querySelector('.after-image');
          if (before && after) {
              before.style.transition = 'opacity 0.5s ease';
              after.style.transition = 'opacity 0.5s ease';
              before.style.opacity = '0';
              after.style.opacity = '1';
          }
      });
      
      card.addEventListener('mouseleave', function() {
          const before = this.querySelector('.before-image');
          const after = this.querySelector('.after-image');
          if (before && after) {
              before.style.transition = 'opacity 0.5s ease';
              after.style.transition = 'opacity 0.5s ease';
              before.style.opacity = '1';
              after.style.opacity = '0';
          }
      });
  });
});