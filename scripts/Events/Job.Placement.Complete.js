// // Get a reference to the camera.
// var camera = machine.defaultHead.defaultCamera;

// // Move the camera to where the part was placed.
// camera.moveTo(placementLocation);

// // Settle the camera and capture an image.
// var image = camera.settleAndCapture();

// var t = new Date(); // get current time
// var timeStr = t.toISOString(); // e.g. 2011-12-19T15:28:46.493Z

// timeStr = timeStr.replace('T','_');
// timeStr = timeStr.replace(':','-');
// timeStr = timeStr.replace(':','-');
// timeStr = timeStr.slice(0,-5); // remove milli seconds
// // timeStr is now: 2011-12-19_15-28-46

// var fileName = String('/home/nemo/.openpnp/vision/log/placements-' + timeStr + '_' + placement.getId() + '.png')

// print('save placement image to ' + fileName);
// // Write the image to a file based on the placement name.
// var file = new java.io.File(fileName);
// javax.imageio.ImageIO.write(image, "PNG", file);
