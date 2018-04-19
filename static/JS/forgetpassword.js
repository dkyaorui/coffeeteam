//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
	if(animating) return false;
	var em = document.getElementById("email").value;
    var na = document.getElementById("name").value;
	document.getElementById("tishi").innerHTML="<font color='margin:0 0px 0px 316px;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</font>";
	if(em == '' && na == '')
	{
		document.getElementById("tishi").innerHTML="<font color='red'>请填写邮箱和用户名</font>";
		document.getElementById("email").style.borderColor='red';
		document.getElementById("name").style.borderColor='red';
		return false;
	}
	else if(em == '' || na == '')
	{
		if(em == '')
		{
			document.getElementById("tishi").innerHTML="<font color='red'>请填写邮箱</font>";
			document.getElementById("email").style.borderColor='red';
			document.getElementById("name").style.borderColor='white';
		}
		else
		{
			document.getElementById("tishi").innerHTML="<font color='red'>请填写用户名</font>";
			var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
			if(!myreg.test(em))
			{
				document.getElementById("email").style.borderColor='red';
				document.getElementById("name").style.borderColor='red';
				myreg.focus();
			}
			else
			{	
				document.getElementById("email").style.borderColor='white';
				document.getElementById("name").style.borderColor='red';
			}
		}
		return false;
	}
    else {
		var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
		if(!myreg.test(em))
		{
			document.getElementById("tishi").innerHTML="<font color='red'>邮箱格式错误！</font>";
			document.getElementById("email").style.borderColor='red';
			document.getElementById("name").style.borderColor='white';
			myreg.focus();
			return false;
        }
		document.getElementById("email").style.borderColor='white';
		document.getElementById("name").style.borderColor='white';
    }
});

$(".nextstep").click(function(){
	if(animating) return false;
	var pw1 = document.getElementById("id_password1").value;
    var pw2 = document.getElementById("id_password2").value;
	if(pw1 == '' || pw1 == '' || pw1.length < 6 || pw2.length < 6)
	{
		document.getElementById("same").innerHTML="<font color='red'>密码至少6位</font>";
		document.getElementById("id_password1").style.borderColor='red';
        document.getElementById("id_password2").style.borderColor='red';
		return false;
	}
    else if(pw1 == pw2) {
        document.getElementById("same").innerHTML="<font color='yellow'>两次密码相同</font>";
		document.getElementById("id_password1").style.borderColor='white';
        document.getElementById("id_password2").style.borderColor='white';
    }
    else {
		document.getElementById("same").innerHTML="<font color='red'>两次密码不相同</font>";
		document.getElementById("id_password1").style.borderColor='red';
        document.getElementById("id_password2").style.borderColor='red';
		return false;
    }
	animating = true;
	current_fs = $(this).parent();
	next_fs = $(this).parent().next().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	
	//show the next fieldset
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'transform': 'scale('+scale+')'});
			next_fs.css({'left': left, 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".login").click(function(){
	window.location.href="/blog/to_login";
})