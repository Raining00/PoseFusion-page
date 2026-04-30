// state manager
let sliderPosition = 50;
let isDragging = false;

// mouse move event
sliderHandle.addEventListener('mousedown', function(e) {
  e.preventDefault();
  isDragging = true;
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
  sliderHandle.classList.add('active');
});

// Position calculation and update
function handleMouseMove(e) {
  if (!isDragging || !container) return;
  const containerRect = container.getBoundingClientRect();
  const position = ((e.clientX - containerRect.left) / containerRect.width) * 100;
  updateSliderPosition(Math.max(0, Math.min(100, position)));
}

// Update state
function updateSliderPosition(pos) {
  // update the slide's position
  sliderTrack.style.transform = `translate(-50%, 0%) translateX(calc(${pos}%))`;
  // update the clip of images
  leftImage.style.clipPath = `inset(0 ${100 - pos}% 0 0)`;
  rightImage.style.clipPath = `inset(0 0 0 ${pos}%)`;
  // update the transparent of lable
  leftLabel.style.opacity = pos > 95 ? 0 : 1;
}
