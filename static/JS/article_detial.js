

$(function(){
	$("#praise").click(function(){
			var praise_img = $("#praise-img");
			var text_box = $("#add-num");
			var praise_txt = $("#praise-txt");
			var num=parseInt(praise_txt.text());
			if(praise_img.attr("src") == ("/static/images/yizan.png")){
				//$(this).html("<img src='{% static 'images/zan.png' %}' id='praise-img' class='animation' />");
				send_msg(0);
				document.getElementById("praise-img").src="/static/images/zan.png";
                praise_img.removeClass("animation");
				praise_txt.removeClass("hover");
				text_box.show().html("<em class='add-animation'>-1</em>");
				$(".add-animation").removeClass("hover");
				num -=1;
				praise_txt.text(num);
			}else{
				//$(this).html("<img src='javascript:doSth();' id='praise-img' class='animation' />");
				send_msg(1);
				document.getElementById("praise-img").src="/static/images/yizan.png";
				praise_img.addClass("animation");
				praise_txt.addClass("hover");
				text_box.show().html("<em class='add-animation'>+1</em>");
				$(".add-animation").addClass("hover");
				num += 1;
				praise_txt.text(num);
			}
		});
	});



$(function(){
	$("#star").click(function(){
			var star_img = $("#star-img");
			if(star_img.attr("src") == ("/static/images/yellowstar.png")){
				send_msg_c(0);
				document.getElementById("star-img").src="/static/images/star.png";
				star_img.removeClass("animation");
				$(".add-animation").removeClass("hover");
			}else{
				send_msg_c(1);
				document.getElementById("star-img").src="/static/images/yellowstar.png";
				star_img.addClass("animation");
				$(".add-animation").addClass("hover");
			}
		});
	});

function send_msg(data){
	var xmlhttp;
	if(window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}else{
	    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    var q=location.search.substr(1);
    var qs=q.split('&');
    var argStr='';
    if(qs){
        for(var i=0;i<qs.length;i++){
            argStr+=qs[i].substring(0,qs[i].indexOf('='))+'='+qs[i].substring(qs[i].indexOf('=')+1)+'&';
        }
    }
	xmlhttp.open("POST","/blog/favorChange/",true);
	xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	xmlhttp.send('id='+argStr+"&data="+data);
	xmlhttp.onreadystatechange = function(){
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
		}
	}
}

function send_msg_c(data){
	var xmlhttp;
	if(window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}

		var q=location.search.substr(1);
    var qs=q.split('&');
    var argStr='';
    if(qs){
        for(var i=0;i<qs.length;i++){
            argStr+=qs[i].substring(0,qs[i].indexOf('='))+'='+qs[i].substring(qs[i].indexOf('=')+1)+'&';
        }
    }
    xmlhttp.open("POST","/blog/collectChange/",true);
		xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
		xmlhttp.send("data="+data+"&id="+argStr);
		xmlhttp.onreadystatechange=function(){
		if(xmlhttp.readyState == 4 && xmlhttp.status==200){
		}
	}
}

