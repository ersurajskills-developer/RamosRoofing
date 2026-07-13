/* ==========================================================================
   Ramos Roofing Plus - Before/After Image Slider Logic
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const sliders = document.querySelectorAll('.slider-view-wrapper');

  sliders.forEach(slider => {
    const beforeWrapper = slider.querySelector('.slider-image-before');
    const afterWrapper = slider.querySelector('.slider-image-after');
    const resizeBar = slider.querySelector('.slider-resize-bar');
    const handle = slider.querySelector('.slider-handle-circle');
    
    if (!afterWrapper || !resizeBar || !handle) return;

    // Ensure wrappers stay at 100% width so images don't resize or scale
    if (beforeWrapper) beforeWrapper.style.width = '100%';
    afterWrapper.style.width = '100%';
    
    let isDragging = false;
    let currentPercentage = 50; // Initial percentage
    let animationFrameId = null;
    
    // Function to apply split position
    function applyPosition(percentage) {
      // clip-path on the after-image wrapper: inset(top right bottom left)
      // Since "after" sits above "before", clipping it from the left (percentage%)
      // reveals the "before" image on the left.
      afterWrapper.style.clipPath = `inset(0 0 0 ${percentage}%)`;
      resizeBar.style.left = `${percentage}%`;
      handle.style.left = `${percentage}%`;
    }
    
    // Function to update split position from clientX coordinate
    function updateSplit(clientX) {
      const rect = slider.getBoundingClientRect();
      let offsetX = clientX - rect.left;
      
      // Enforce boundaries
      if (offsetX < 0) offsetX = 0;
      if (offsetX > rect.width) offsetX = rect.width;
      
      // Calculate percentage
      currentPercentage = (offsetX / rect.width) * 100;
      applyPosition(currentPercentage);
    }
    
    // RequestAnimationFrame handler to optimize dragging updates
    function onDrag(clientX) {
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
      animationFrameId = requestAnimationFrame(() => {
        updateSplit(clientX);
      });
    }
    
    // Drag Start
    function dragStart(e) {
      isDragging = true;
      slider.classList.add('dragging');
      // Prevent default browser touch/drag behavior
      if (e.cancelable) {
        e.preventDefault();
      }
    }
    
    // Drag End
    function dragEnd() {
      if (!isDragging) return;
      isDragging = false;
      slider.classList.remove('dragging');
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
        animationFrameId = null;
      }
    }
    
    // Drag Move
    function dragMove(e) {
      if (!isDragging) return;
      
      let clientX = 0;
      if (e.type === 'touchmove') {
        clientX = e.touches[0].clientX;
      } else {
        clientX = e.clientX;
      }
      
      onDrag(clientX);
    }
    
    // Event Listeners for Mouse
    handle.addEventListener('mousedown', dragStart);
    resizeBar.addEventListener('mousedown', dragStart);
    
    window.addEventListener('mouseup', dragEnd);
    window.addEventListener('mousemove', dragMove);
    
    // Event Listeners for Touch (with passive false to allow preventDefault)
    handle.addEventListener('touchstart', dragStart, { passive: false });
    resizeBar.addEventListener('touchstart', dragStart, { passive: false });
    
    window.addEventListener('touchend', dragEnd);
    window.addEventListener('touchmove', dragMove, { passive: false });
    
    // Let user click anywhere on slider to jump to that position
    slider.addEventListener('click', (e) => {
      // Don't trigger split update if clicking exactly on handle or resize bar
      if (e.target === handle || handle.contains(e.target) || e.target === resizeBar) return;
      updateSplit(e.clientX);
    });
    
    // Window Resize listener to keep slider percentage stable
    window.addEventListener('resize', () => {
      applyPosition(currentPercentage);
    });
    
    // Set initial position
    applyPosition(currentPercentage);
  });
});

