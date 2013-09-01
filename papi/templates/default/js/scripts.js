$(function() {
	prettyPrint();

	$(".view-source").on("click", function() {
		$(this).closest(".source").find(".source-code").first().toggle();
	});
});