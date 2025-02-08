if (Hls.isSupported()) {
    var video = document.getElementById('videoElement');
    var hls = new Hls();
    hls.loadSource('http://localhost:5000/livestream/stream/video.m3u8');
    hls.attachMedia(video);
} else {
    console.error('HLS n\'est pas supporté par ce navigateur.');
}