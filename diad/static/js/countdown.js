/******************************************************************************************************************************
COMMING SOON PAGE
*******************************************************************************************************************************/
(function($) {
    /**
    * Set your date here  (YEAR, MONTH (0 for January/11 for December), DAY, HOUR, MINUTE, SECOND)
    * according to the GMT+0 Timezone
    **/
    var launch = new Date(2015, 04, 27, 00, 00);
    /**
    * The script
    **/
    var message = $('#message');
    var days = $('#days');
    var hours = $('#hours');
    var minutes = $('#minutes');
    var seconds = $('#seconds');

    var daysM = $('#daysM');
    var hoursM = $('#hoursM');
    var minutesM = $('#minutesM');
    var secondsM = $('#secondsM');
    
    setDate();
    function setDate(){
        var now = new Date();
        if( launch < now ){
            days.html('<h1>0</H1><p>Dias</p>');
            hours.html('<h1>0</h1><p>Horas</p>');
            minutes.html('<h1>0</h1><p>Minutos</p>');
            seconds.html('<h1>0</h1><p>Segundos</p>');
            //message.html('OUR SITE IS NOT READY YET...');
            message.html('0 Días 0 Horas 0 Minutos 0 Segundos<br>');
        }
        else{
            var s = -now.getTimezoneOffset()*60 + (launch.getTime() - now.getTime())/1000;
            var d = Math.floor(s/86400);
            days.html('<h1>'+d+'</h1><p>Día'+(d>1?'s':''),'</p>');
            s -= d*86400;

            var h = Math.floor(s/3600);
            hours.html('<h1>'+h+'</h1><p>Hora'+(h>1?'s':''),'</p>');
            s -= h*3600;

            var m = Math.floor(s/60);
            minutes.html('<h1>'+m+'</h1><p>Minuto'+(m>1?'s':''),'</p>');

            s = Math.floor(s-m*60);
            seconds.html('<h1>'+s+'</h1><p>Segundo'+(m>1?'s':'')+'</p>');

            message.html(d+' Día'+(d>1?'s ':' ')+h+' Hora'+(h>1?'s ':' ')+m+' Minuto'+(m>1?'s ':' ')+s+' Segundo'+(m>1?'s':'')+'<br>');

            setTimeout(setDate, 1000);

        }
    }
})(jQuery);
