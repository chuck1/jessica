
// hello

function edit_open(e) {
	console.log('edit_open');
	console.log(e.target);

	// hide edit_open button
	$(e.target).hide();

	// hide rendered
	//
	
	

	// show edit
	//
	
	var div = $("<div></div>")
	var textarea = $("<textarea></textarea>")
	var button_edit = $("<button>edit</button>")
	var button_cancel = $("<button>cancel</button>")

	button_cancel.click(function() {
		window.location.replace(path);
	});

	div.append(textarea);
	div.append(button_edit);
	div.append(button_cancel);

	$("body").append(div)
}

function on_load() {

	$("button#edit_open").click(edit_open);

}

