var images = [
    'uma1.jpg', 
    'uma2.jpg', 
    'uma3.jpg', 
];
var num = 0;
function next() {
    var slider = document.getElementById('slider');
    num++;
    if(num >= images.length) {
        num = 0;
    }
    slider.src = images[num];
}

setInterval(next,5000)