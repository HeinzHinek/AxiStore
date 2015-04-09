jQuery(document).ready(function($) {

	var threecards = false;
	var cardcounter = 0;

	function startCard() {
		var mydelay = 0;
		$("#cardholder a").each(function(){
			mydelay = mydelay + 70;
			$(this).delay(mydelay).fadeIn();
		});
	}

	startCard();

	$( "#mix" ).click(function() {
		$("#cardholder a").hide();
		startCard();
	});

	$("#cardholder a" ).on( "mouseenter", function() {
        _this = $(this);
        if ( !_this.hasClass('selected') ) {
            _this.addClass('hovercard');
        }
    }).on( "mouseleave", function() {
        _this = $(this);
        if ( !_this.hasClass('selected') ) {
            _this.removeClass('hovercard');
        }
    });

    $('#cardholder a').click(function(event) {

		event.preventDefault();
		var helptext = $('#myhelp').val();

		var currenturl = $('#helpurl').val();

		var cardcount = $('input[name=cardcount]:checked').val();
		if ( cardcount == 'three' ) {

			threecards = true;
			_this = $(this);

			if ( _this.hasClass('selected') ) {
				_this.removeClass('selected');
				cardcounter--;
			} else {
				cardcounter++;
				_this.addClass('selected');
			}
		} else {
			threecards = false;
		}

		if (!threecards) {
			if ( helptext != '' ) {
				location.href = currenturl + "?myhelp=" + helptext;
			} else {
				location.href = currenturl;
			}
		} else {
			if ( cardcounter == 3 ) {
				if ( helptext != '' ) {
					location.href = currenturl + "?numcards=3&myhelp=" + helptext;
				} else {
					location.href = currenturl + "?numcards=3";
				}
			}
		}
	});

});