let model;
let video;

async function setupHandpose() {
  video = document.createElement('video');
  video.width = 640;
  video.height = 480;
  
  document.body.appendChild(video);

  // Load the HandPose model
  model = await handpose.load();
  console.log("HandPose model loaded");

  // Setup the webcam feed
  const stream = await navigator.mediaDevices.getUserMedia({
    video: true,
  });
  video.srcObject = stream;
  video.play();

  video.addEventListener('loadeddata', () => {
    detectHand();
  });
}

async function detectHand() {
  const predictions = await model.estimateHands(video);
  
  if (predictions.length > 0) {
    const landmarks = predictions[0].landmarks;
    handleGestures(landmarks);
  }

  requestAnimationFrame(detectHand);
}

function handleGestures(landmarks) {
  // Get the Y coordinates of the index finger (point 8) and middle finger (point 12)
  const indexY = landmarks[8][1];
  const middleY = landmarks[12][1];
  
  // Check for two-finger scroll
  if (Math.abs(indexY - middleY) < 20) {
    if (indexY < 200) {
      window.scrollBy(0, -10); // Scroll up
    } else if (indexY > 280) {
      window.scrollBy(0, 10); // Scroll down
    }
  }
  
  // Check for one-finger click (using the tip of the index finger)
  const indexTip = landmarks[8];
  const x = indexTip[0];
  const y = indexTip[1];
  
  if (indexTip[2] < 0.1) { // Assuming the finger is close to the screen
    const element = document.elementFromPoint(x, y);
    if (element && element.classList.contains('content')) {
      element.style.backgroundColor = 'yellow'; // Highlight the clicked element
      setTimeout(() => {
        element.style.backgroundColor = ''; // Remove highlight after some time
      }, 500);
    }
  }
}

setupHandpose();
