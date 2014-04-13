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

slots = {}

function daClick(){
    $("[name='type']").each(function(){
        var name = $.trim($(this).parent().text());
        $("[label='"+name+"']").detach()
    })
    var name = $.trim($(this).parent().text());
    $("#id_grade").append(slots[name])
}

$(function () {

    $("[name='type']").each(function(){
        var name = $.trim($(this).parent().text());
        slots[name] = $("[label='"+name+"']");
        $("[label='"+name+"']").detach()
    })

    $("[name='type']").click(daClick)

    $("[name='type']:checked").click()

	$('#route-date-set').datepicker ()

	$('[data-widget=color-widget]').simplecolorpicker({
		picker: true
	});

});

$("#route-rate").raty({
	size: 24,
	width: false,
    readOnly: function(){
        return $(this).is("[readonly]")
    }
});

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

$("#gym-follow").click(function(){
	$(this).toggleClass("active")
	if($(this).hasClass("active")){
		$.post("/"+GYM+"/follow/");
		$(this).text("Following");
		$(this).prepend('<i class="fa fa-check"></i>&nbsp;');
	}else{
		$.post("/"+GYM+"/unfollow/");
		$(this).text("Follow Gym");
		$(this).prepend('<i class="fa fa-plus"></i>&nbsp;');
	}
})

app = angular.module("dynoroute", [])

app.config(function($httpProvider){
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
})

app.controller("FlagController", function FlagController($scope, $http){
    $scope.message = ""

    $scope.submit = function(){
        $http.post("/"+GYM+"/routes/"+ROUTE+"/flag/", {
            message: $scope.message
        }).success(function(){
            $scope.message = ""
            $("#flagModal").modal('hide')
            $.howl ({
                type: $(".howler").data ('type')
                , title: ''
                , content: 'Route flagged. Thanks for your feedback.'
                , sticky: $(".howler").data ('sticky')
                , lifetime: 7500
                , iconCls: $(".howler").data ('icon')
            });
        })
    }
})

app.controller("RoutesController", function RoutesController($scope, $http){
    $scope.checked = 0;
    $scope.dismissible = 0;
    $scope.tearable = 0;

    $scope.check = function(event){
        if(event){
            $scope.checked-= 1
        }else{
            $scope.checked+= 1
        }
    }

    $scope.dismiss = function(event){
        if(event){
            $scope.dismissible-= 1
        }else{
            $scope.dismissible+= 1
        }
    }

    $scope.tear = function(event){
        if(event){
            $scope.tearable-= 1
        }else{
            $scope.tearable+= 1
        }
    }
})

$(".nopropagate").click(function(event){
    event.stopPropagation()
})
