
$(document).ready(function(){ // jQuery
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];
    var seekedPosition;
    var lastMode;

    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });
    //receive details from server
    socket.on('newnumber', function(msg) { // event handler with event newnumber
        console.log("Receive number" + msg.number);
        //maintain a list of ten numbers
        if (numbers_received.length >= 10){
            numbers_received.shift()
        }            
        numbers_received.push(msg.number);
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
            numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        }
        $('#log').html(numbers_string);
    });

    socket.on('gesture_mode', function(msg) {
        var mode = msg.mode;
        console.log("gesture_mode: " + mode);

        if(mode == 4) {
            //this is not a good practice, but player is a global variable
            //player.seekTo(10,false);
            player.pauseVideo();
            lastMode = 4;

        }else if(mode == 1) {
            // go left one second
            //player.getCurrentTime()
            if(lastMode!=1) {
                seekedPosition = player.getCurrentTime();
            }else{
                seekedPosition--;
            }
            player.seekTo(seekedPosition - 1, false);
            lastMode = 1;

        }else if(mode == 2) {
            //go right one second

            if(lastMode!=2) {
                seekedPosition = player.getCurrentTime();
            }else{
                seekedPosition++;
            }
            player.seekTo(seekedPosition + 1, false);
            lastMode = 2;

        }else if(mode == 3) {
            if(lastMode==1 || lastMode == 2) {
                player.seekTo(seekedPosition, true);
            }
                        
            player.playVideo();
            lastMode = 3;
            
        }
       

    });

    $("p").click(function(){ // works
        $(this).hide();
    });

});
