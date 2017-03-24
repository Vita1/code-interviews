var database = firebase.database();

function getAllEvents(callback) {
    database.ref('/').once('value').then( function(snapshot){
        var events = Object.values(snapshot.val())[0];
        callback(events);
        });
}