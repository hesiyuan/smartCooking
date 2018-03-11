console.log('annyang block')
    if (annyang) {
      // Let's define our first command. First the text we expect, and then the function it should call

          var commands = {
            // annyang will capture anything after a splat (*) and pass it to the function.
            // e.g. saying "Show me Batman and Robin" is the same as calling showFlickr('Batman and Robin');
            'show me *tag': showFlickr,
            // A named variable is a one word variable, that can fit anywhere in your command.
            // e.g. saying "calculate October stats" will call calculateStats('October');
            'go forward': function() {
               console.log('go forward');
            },

            // By defining a part of the following command as optional, annyang will respond to both:
            // "say hello to my little friend" as well as "say hello friend"
            'play the video': function() {
                console.log('play the video');
                player.playVideo();
            },

            'show tps report': function() {
                console.log('show tps report');
            }

          };

          var showFlickr = function(tag) {
            console.log(tag);
          }
          
      // Add our commands to annyang
      annyang.addCommands(commands);
      // Start listening. You can call this here, or attach this call to an event, button, etc.
      annyang.start();
    }