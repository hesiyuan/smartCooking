
$(document).ready(function(){ // jQuery
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];
    var seekedPosition;
    var lastMode = 3;

    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });
    //receive details from server
    socket.on('newnumber', function(msg) { // event handler with event newnumber
        console.log("Receive number" + msg.number);
        //maintain a list of ten numbers
        // if (numbers_received.length >= 10){
        //     numbers_received.shift()
        // }            
        // numbers_received.push(msg.number);
        // numbers_string = '';
        // for (var i = 0; i < numbers_received.length; i++){
        //     numbers_string = numbers_string + '<p>' + numbers_received[i].toString() + '</p>';
        // }
        // $('#log').html(numbers_string);
    });

    socket.on('gesture_mode', function(msg) {
        var mode = msg.mode;
        console.log("gesture_mode: " + mode);

        if(mode == 4) { // pause mode
                
            // if(lastmode == 1 || lastmode == 2){
            //     // seekedPosition must be set from lastmode
            // }else if(lastMode == 3) {

            //     seekedPosition = player.getCurrentTime();
            // }else { // lastMode == 4
            //     //
            //     seekedPosition = player.getCurrentTime();
            // }

            player.pauseVideo();
            lastMode = 4;

        }else if(mode == 1) {
            // go left one second
            
            if(lastMode == 1 || lastMode == 2){

                seekedPosition -- ;
            }else{
                seekedPosition = player.getCurrentTime();
            }


            player.seekTo(seekedPosition, false);
            lastMode = 1;

        }else if(mode == 2) {
            //go right one second

            if(lastMode == 1 || lastMode == 2) {
                seekedPosition++;

            }else {

                seekedPosition = player.getCurrentTime();
            }

            player.seekTo(seekedPosition, false);
            lastMode = 2;

        }else if(mode == 3) {

            if(lastMode==1 || lastMode == 2) {
                player.seekTo(seekedPosition, true);
            }else if(lastMode == 3) {



            }else { // lastmode == 4
                player.seekTo(player.getCurrentTime(), true);

            }

            player.playVideo();
            lastMode = 3;
            
        }
       

    });

    $("p").click(function(){ // works
        $(this).hide();
    });

});
