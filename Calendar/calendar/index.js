
	// require express for setting up server and morgan for server logging
	var express = require('express');
	var morgan = require('morgan');

	// get port number from heroku, or default to 3000
	var port = process.env.PORT || 3000;

	var app = express();

	app.use(morgan('dev'));

	// set /public as path for static GET requests
	app.use(express.static(__dirname+'/public'));

	// add more routing rules here to complete your server

	// start server and listen 
	app.listen(port, function() {
		console.log("Server listening on port " + port);
	}); 

