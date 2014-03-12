function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


var topRopeLabel;
var topRopeParent;
var topRopeOptions;

var boulderLabel;
var boulderParent;
var boulderOptions;

$(function () {

	topRopeLabel = $("[label='Top Rope']");
	topRopeParent = topRopeLabel.parent();
	topRopeOptions = $("[label='Top Rope']").children();

	boulderLabel = $("[label='Bouldering']");
	boulderParent = boulderLabel.parent();
	boulderOptions = $("[label='Bouldering']").children();

	$("[label='Top Rope']").detach();
	$("[label='Top Rope']").children().detach();

	$('#route-date-set').datepicker ()

	$('#route-color').simplecolorpicker({
		picker: true
	});
	$('#route-color2').simplecolorpicker({
		picker: true
	});

});

$("#id_type_1").click(function() {
	$("[label='Top Rope']").detach();
	$("[label='Top Rope']").children().detach();

	boulderParent.append(boulderLabel);
	boulderLabel.append(boulderOptions);
});

$("#id_type_0").click(function() {
	$("[label='Bouldering']").detach();
	$("[label='Bouldering']").children().detach();

	topRopeParent.append(topRopeLabel);
	topRopeLabel.append(topRopeOptions);
});

$("#route-rate").raty();

$("#route-send").click(function(){
	$(this).toggleClass("active")
	if($(this).hasClass("active")){
		$.post("/"+GYM+"/routes/"+ROUTE+"/send/");
	}else{
		$.post("/"+GYM+"/routes/"+ROUTE+"/unsend/");
	}
})

$("#route-favorite").click(function(){
	$(this).toggleClass("active")
	if($(this).hasClass("active")){
		$.post("/"+GYM+"/routes/"+ROUTE+"/favorite/");
	}else{
		$.post("/"+GYM+"/routes/"+ROUTE+"/unfavorite/");
	}
})
