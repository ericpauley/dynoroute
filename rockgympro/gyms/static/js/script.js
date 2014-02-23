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