(function(){
	var video = document.getElementById('video');
		vendoUrl = window.URL || window.webkitURL;

	navigator.getUserMedia = 	navigator.getUserUserMedia ||
						 		navigator.webkitGetUserMedia ||
								navigator.mozGetUserMedia ||
						 		navigator.msGetUserMedia;

	navigator.getUserMedia({
		video: true,
		audio: false
	}, function(stream){
		video.src = vendoUrl.createObjectURL(stream);
		// video.srcObject = stream;
		// video.src = window.URL.createObjectURL(stream);
		video.play();
	}, function(error){
		//an error occured
		//error.code
	});
});
// if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     // Not adding `{ audio: true }` since we only want video now
//     navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
//         video.src = window.URL.createObjectURL(stream);
//         video.play();
//     });
// }

// // Elements for taking the snapshot
// var canvas = document.getElementById('canvas');
// var context = canvas.getContext('2d');
// var video = document.getElementById('video');

// // Trigger photo take
// document.getElementById("snap").addEventListener("click", function() {
// 	context.drawImage(video, 0, 0, 640, 480);
// });

// }

// var video = document.getElementById("video")

// if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
//     // Not adding `{ audio: true }` since we only want video now
//     navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
//         video.src = window.URL.createObjectURL(stream);
//         video.play();
//     });
// }

// var canvas = document.getElementById('canvas')
// var canvas = document.getElementById('2d')
// var canvas = document.getElementById('video')

// // Trigger photo take
// document.getElementById("snap").addEventListener("click", function() {
// 	context.drawImage(video, 0, 0, 640, 480);
// });