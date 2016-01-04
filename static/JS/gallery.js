var pictures = [];
var pictures_len;
var comments;
var comment_form;
var like_form;

a = document.querySelectorAll('.picture');
for (var i = 0; i < a.length; i++) {
	pictures.push(a[i].src.replace("/Mini", ""));
	a[i].setAttribute('onclick', 'big_size(this)');
	a[i].setAttribute('alt', a[i].alt + '_' + a[i].src.split('/').pop().split('.')[0]);
}
pictures_len = pictures.length;
document.getElementById("all_photo").innerHTML = pictures_len;

if (document.cookie && !window.location.hash)
	window.location.hash = document.cookie.split('=')[1].split(';')[0];
if (window.location.hash) history();
document.body.onhashchange = history;
comments = $('#comment_table');
comment_form= $('#comment_form');
like_form= $('#like_form');

function history() {
	var index =	window.location.hash.replace('#', '');
		if (0 < index && index <= pictures_len) {
			var parent = document.getElementById("floor2_img_div");
			if (document.getElementById("big_picture")) {
				var child = document.getElementById("big_picture");
				parent.removeChild(child);
			}
			document.getElementById('floor2_img_div').style.backgroundImage = "url('http://chizha.16mb.com/Images/Gallery/loading.gif')";
			document.body.style.overflow = 'hidden';
			document.getElementById("second_floor").style.display = 'block';
				
			document.getElementById("current_photo").innerHTML = index;
			
			var newImg = document.createElement('img');
			newImg.setAttribute('id', 'big_picture');
			newImg.setAttribute('src', pictures[index - 1]);
			newImg.setAttribute('onload', 'picture_resize(this)');
			newImg.setAttribute('alt', 'big');
			parent.appendChild(newImg);

			getLikesCount(index);
            getComments();
		}
		else {
			window.location.hash = '';
			big_size_exit();
		}
}
function picture_resize(pic) {
	var div_width = document.getElementById("floor2_img_div").offsetWidth;
	if (pic.naturalWidth < div_width) pic.width = pic.naturalWidth;
	else pic.width = div_width;
	
	document.getElementById('floor2_img_div').style.backgroundImage = 'none';
	
	var x, current = parseInt(document.getElementById("current_photo").innerHTML);
	
	var load_next = document.createElement('img');
	if (current + 1 > pictures_len) x = 0;
	else x = current;
	load_next.setAttribute('src', pictures[x]);
	
	var load_prev = document.createElement('img');
	if (current - 2 < 0) x = pictures_len - 1;
	else x = current - 2;
	load_prev.setAttribute('src', pictures[x]);
}
function big_size(pic) {
	var path_to_big = pic.src.replace("/Mini", "");
	for (var i = 0; i < pictures_len; i++)
		if (pictures[i] == path_to_big) {		
			window.location.hash = i + 1;			
			break;
		}
}
function nextOrPrev(direction) {	
	var x, current = parseInt(document.getElementById("current_photo").innerHTML);
	if (direction == 'next') {
		if (current + 1 > pictures_len) x = 0;
		else x = current;
	}
	else {
		if (current - 2 < 0) x = pictures_len - 1;
		else x = current - 2;
	}
	window.location.hash = x + 1;
}
function big_size_exit() {
	document.getElementById("second_floor").style.display = 'none';
	document.body.style.overflowY = 'auto';
	window.location.hash = '';
}
if('onhelp' in window) {
	window.onhelp = function (e) {
		e = e || window.event;
		if (e.stopPropagation)
			e.stopPropagation();
		else
			e.cancelBubble = true;
		return false;
	}
}
document.onkeydown = function(e) {
    e = e || window.event;
	var flag = 0;
	if (e.keyCode == 112 || e.keyCode == 27 || e.keyCode == 37 || e.keyCode == 39) {
		flag = 1;
		if(e.stopPropagation)
			e.stopPropagation();
		else
			e.cancelBubble = true;
	}
	if (e.keyCode == 112) { //F1
		if (document.getElementById("help").style.display != 'none')
			document.getElementById("help").style.display = 'none';
		else
			document.getElementById("help").style.display = 'block';
	}
	if (document.getElementById("second_floor").style.display != 'none' &&
		document.getElementById("help").style.display == 'none') {
		if (e.keyCode == 27) { //Esc			
			big_size_exit();			
		}
		else if (e.keyCode == 37) { //left
			nextOrPrev('prev');
		}
		else if (e.keyCode == 39) { //right
			nextOrPrev('next');
		}
	}
	if (flag)
		return false;
};

function imageToCookie() {
	if (document.cookie)
		document.cookie = "image=";
	document.cookie = "image=" + window.location.hash.replace('#', '');
	//console.log(document.cookie);
}


function getComments() {
	$.ajax({
		type: 'GET',
		url: '/home/gallery/get_comments/',
		data: {
			id: window.location.hash.replace('#', '')
		},
		success: function(data) {
             if (typeof data === 'string'){
                 window.location.href = data;
             }
             else {
                 comments.empty().hide();
                 for (var counter in data) {
                     comments.append(data[counter]);
                 }
				 comments.show()
             }
		},
		error: function(data) {
			alert('Stop hacking!');
		}
	});
}
var ifEdit = false, editId = -1;
comment_form.submit(function() {
	$.ajax({
		type: 'POST',
		url: '/home/gallery/send_comment/',
		data: {
			text: $('#text_com').val(),
			id: window.location.hash.replace('#', ''),
			ifEdit: ifEdit,
			editId: editId,
			csrfmiddlewaretoken: $.cookie('csrftoken')
		},
		success: function(data) {
			$('#text_com').val('');
			if (typeof data === 'string') {
				if (data !== 'stop') {
					if (data === 'editOK') {
						getComments();
					}
					else
						window.location.href = data;
				}
			} else {
				getComments();
			}
		},
		error: function(data) {
			alert('Stop hacking!');
		}
	});
	if (ifEdit) {
		ifEdit = false;
		editId = -1;
	}
	return false;
});
function deleteComment(id) {
    $.ajax({
		type: 'POST',
		url: '/home/gallery/delete_comment/' + id,
		data: {
			csrfmiddlewaretoken: $.cookie('csrftoken')
		},
		success: function(data) {
			if (typeof data === 'string'){
				if (data !== 'OK') {
					window.location.href = data;
				}
				getComments();
			}
		},
		error: function (data) {
			alert('Stop hacking!');
		}
    });
}
function editComment (id) {
	ifEdit = true;
	editId = id;
	document.getElementById('text_com').innerHTML = document.getElementById('comment_' + id).innerHTML;
}
like_form.submit(function() {
	$.ajax({
		type: 'POST',
		url: '/home/gallery/send_like/',
		data: {
			id: window.location.hash.replace('#', ''),
			csrfmiddlewaretoken: $.cookie('csrftoken')
		},
		success: function(data) {
			if (parseInt(data) != data){
				window.location.href = data;
			}
			else {
				document.getElementById('likes_count').innerHTML = data;
			}
		},
		error: function (data) {
			alert('Stop hacking!');
		}
	});
	return false;
});

function getLikesCount (id) {
	$.ajax({
		type: 'GET',
		url: '/home/gallery/get_likes_count/',
		data: {
			id: window.location.hash.replace('#', '')
		},
		success: function(data) {
			if (parseInt(data) != data){
				window.location.href = data;
			}
			else {
				document.getElementById('likes_count').innerHTML = data;
			}
		},
		error: function (data) {
			alert('Stop hacking!');
		}
	});
}