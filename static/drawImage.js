var imageWidth = 80, imageHeight = 7, imageData = [''], pixelSize = 10, imageSettings, mouseDown = false;

// Send the image as a POST to the server for handling
function sendImage(){
	// Create form for sending POST
	var form = document.createElement("form");
	form.setAttribute('method',"POST");
	form.setAttribute('action',"image");
	form.setAttribute('display',"none");
	
	// Create input for size and image
	var width = document.createElement("input");
	width.setAttribute('name', "width");
	width.setAttribute('value', imageWidth);
	width.setAttribute('type', "hidden");
	var height = document.createElement("input");
	height.setAttribute('name', "height");
	height.setAttribute('value', imageHeight);
	height.setAttribute('type', "hidden");
	var image = document.createElement("input");
	image.setAttribute('name', "image");
	image.setAttribute('value', imageData);
	image.setAttribute('type', "hidden");
	var space = document.createElement("input");
	space.setAttribute('name', "space");
	space.setAttribute('value', imageSettings.elements.namedItem("space").value);
	space.setAttribute('type', "hidden");
	var key = document.createElement("input");
	key.setAttribute('name', "key");
	key.setAttribute('value', imageSettings.elements.namedItem("key").value);
	key.setAttribute('type', "hidden");
	
	// Add all inputs to the form and send
	form.appendChild(width);
	form.appendChild(height);
	form.appendChild(image);
	form.appendChild(space);
	form.appendChild(key);
	document.body.appendChild(form);
	form.submit();
}

// Create stage with layer, pixels, and array of pixels (Used to send the data)
function createImageBoard(){
	
	// Get the width and height if it is set (Default to width 80 and height 7)
	imageWidth = getParameterByName("width"), imageHeight = getParameterByName("height");
	imageSettings.elements.namedItem("color").value = getParameterByName("color");
	if(getParameterByName("key")!==null && getParameterByName("key")!=='')
		imageSettings.elements.namedItem("key").value = getParameterByName("key");
	if(getParameterByName("space")!==null && getParameterByName("space")!=='')
		imageSettings.elements.namedItem("space").value = getParameterByName("space");
	if(imageWidth!==null && imageWidth!==''){
		imageSettings.elements.namedItem("width").value = imageWidth;
		if(isNaN(imageWidth) || imageWidth>255 || imageWidth<1){
			alert('Error! Height and Width must be integers within their respective ranges!');
			return;
		}
	}
	else
		imageWidth = 80;
	if(imageHeight!==null && imageHeight!==''){
		imageSettings.elements.namedItem("height").value = imageHeight;
		if(isNaN(imageHeight) || imageHeight>255 || imageHeight<1){
			alert('Error! Height and Width must be integers within their respective ranges!');
			return;
		}
	}
	else
		imageHeight = 7;
	
	// Create layer and stage
	var imageStage = new Konva.Stage({ container: 'image-canvas', width: imageWidth*pixelSize+pixelSize*2, height: imageHeight*pixelSize+pixelSize*2 }), imageLayer = new Konva.Layer({x: pixelSize, y: pixelSize});

	// Create and add background layer
	var backgroundLayer = new Konva.Layer(), background = new Konva.Rect({
																  width: imageWidth*pixelSize+pixelSize*2,
																  height: imageHeight*pixelSize+pixelSize*2,
																  fill: 'black',
																  stroke: 'grey',
																  strokeWidth: pixelSize
																});
	backgroundLayer.add(background);
	imageStage.add(backgroundLayer);
	
	// Create all pixels in the array and in the layer
	for(var y=0;y<imageHeight;y++){
		imageData[y] = '';
		for(var x=0;x<imageWidth;x++){
			imageData[y] +='0';
			imageLayer.add(createPixel(x,y));
		}
	}
	
	// Add the layer to the stage
	imageStage.add(imageLayer);
}

// Gets the current color of the pixel given
function getPixelColor(x,y){
	switch(imageData[y][x]){
		case '0':
			return "#333333";
		case '1':
			return "#FF0000";
		case '2':
			return "#00FF00";
		case '3':
			return "#FFC200";
		case '4':
			return "#FFFF00";
		case '5':
			return "#C20000";
		case '6':
			return "#C20000";
		case '7':
			return "#A52A2A";
		case '8':
			return "#FFA500";
	}
	return '';
}

// Replaces a character at the given index with the given character (source: http://stackoverflow.com/questions/1431094/how-do-i-replace-a-character-at-a-particular-index-in-javascript)
String.prototype.replaceAt=function(index, character) {
    return this.substr(0, index) + character + this.substr(index+character.length);
}

// Creates a pixel object for display
function createPixel(x,y){
	// Create the pixel as a circle
	var pixel = new Konva.Circle({
				  x: x*pixelSize+pixelSize/2,
				  y: y*pixelSize+pixelSize/2,
				  radius: pixelSize/4,
				  fill: getPixelColor(x,y),
				  stroke: getPixelColor(x,y),
				  strokeWidth: 4
				});
	
	// Bind events to the pixel so that it changes color based on the color in the settings form
	pixel.on('mousedown touchstart', function() {
		var x = (this.x()-pixelSize/2)/pixelSize, y = (this.y()-pixelSize/2)/pixelSize;
		imageData[y] = imageData[y].replaceAt(x, imageSettings.elements.namedItem("color").value);
		this.fill(getPixelColor(x,y));
		this.stroke(getPixelColor(x,y));
		this.getParent().draw();
		mouseDown = true;
	});
	pixel.on('mouseenter touchmove', function() {
		if(mouseDown){
			var x = (this.x()-pixelSize/2)/pixelSize, y = (this.y()-pixelSize/2)/pixelSize;
			imageData[y] = imageData[y].replaceAt(x, imageSettings.elements.namedItem("color").value);
			this.fill(getPixelColor(x,y));
			this.stroke(getPixelColor(x,y));
			this.getParent().draw();
		}
	});
	
	// Return the newly created pixel
	return pixel;
}

// Gets the parameter that was passed to this url (source: http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript)
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    url = url.toLowerCase(); // This is just to avoid case sensitiveness  
    name = name.replace(/[\[\]]/g, "\\$&").toLowerCase();// This is just to avoid case sensitiveness for query parameter name
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

// Load the image board
window.onload = function(){
	imageSettings = document.getElementById("drawForm");
	createImageBoard();
};

// Set mouse to down for detecting draging
window.onmouseup = function(){
	mouseDown = false;
};
window.onmousedown = function(){
	mouseDown = true;
};