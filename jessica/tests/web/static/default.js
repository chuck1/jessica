
// hello

function edit_open(e) {
	console.log('edit_open');
	console.log(e.target);

	// hide edit_open button
	
	$(e.target).hide();

	// show edit
	
	var div = $("<div></div>")
	var textarea = $("<textarea></textarea>")

	textarea.val(raw);
	textarea.attr('rows', '20');
	textarea.attr('cols', '150');

	var button_edit = $("<button>edit</button>")
	var button_cancel = $("<button>cancel</button>")

	button_cancel.click(function() {
		//window.location.replace(url);
		location.reload();
	});

	button_edit.click(function() {

		var xhr = new XMLHttpRequest();
		xhr.open("POST", "/edit", true);
		xhr.setRequestHeader('Content-Type', 'application/json');
		xhr.send(JSON.stringify({
			path: path,
			text: textarea.val()
		}));
		xhr.onload = function() {
			console.log("HELLO")
			console.log(this.responseText);
			var data = JSON.parse(this.responseText);
			console.log(data);

			//window.location.replace(url);
			location.reload();
		}

	});

	div.append(textarea);
	div.append(button_edit);
	div.append(button_cancel);

	$("body").append(div)
}

function on_load() {

	$("button#edit_open").click(edit_open);

}

