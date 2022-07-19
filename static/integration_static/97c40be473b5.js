;$(document).ready(function(){currentVideo=$('.playlist-item.active');nextVideo=currentVideo.next('li');prevVideo=currentVideo.prev('li');var tmpHtml=currentVideo.attr('data')+'/'+$('.video-count').html()
$('.video-count').html(tmpHtml)
if(nextVideo.length){$('.forward').html('<a href="'+nextVideo.children('a').attr('href')+'"><i class="fa fa-1 fa-fast-forward"></i></a>');}else{$('.forward').html('<i class="fa fa-1 fa-fast-forward"></i>');}
if(prevVideo.length){$('.backward').html('<a href="'+prevVideo.children('a').attr('href')+'"><i class="fa fa-1 fa-fast-backward"></i></a>');}else{$('.backward').html('<i class="fa fa-1 fa-fast-backward"></i>');}
$(".fancybox").fancybox({maxWidth:500,maxHeight:485,fitToView:true,autoSize:false,closeClick:false,openEffect:"none",closeEffect:"none",modal:true,});$(".video-show-more").click(function(e){e.preventDefault();$(".video-info").slideToggle("slow");$(this).text($(this).text()=='Show video info'?"Hide video info":"Show video info");});});;document.addEventListener('DOMContentLoaded',(event)=>{function logData(e){videotime=String(e.target.currentTime);if(e.type=='play'){play=Math.round(e.target.currentTime);if(play==pause){act_pp='Play';}
else{act_pp='Seek';videotime=String(pause)+'-'+String(play);}}
if(e.type=='pause'){pause=Math.round(e.target.currentTime);act_pp='Pause';}
if(e.target.id=="st_video_html5_api")
{let data={timestamp:new Date().toLocaleTimeString(),action:act_pp,url:e.target.currentSrc,videotime:videotime}
log_data.push(data)}}
function clickListener(e)
{var clickedElement=e.target,tags=document.getElementsByTagName(clickedElement.tagName);for(var i=0;i<tags.length;++i)
{if(tags[i]==clickedElement)
{let video=document.getElementById("st_video_html5_api")
var href=clickedElement.parentElement.getAttribute("href")
var href1=clickedElement.getAttribute('href')
var act=String(clickedElement.innerText).trim()
if(href){if(href.match('watch'))
{act='Change';}}
if(href1){if(href1.match('watch'))
{act='Change';href=href1;}
if(href1=='#tutorials'){act='TutorialList';href=href1;}
if(href1=='#forums'){act='ForumsQuestionList';href=href1;}
else if(href1.match('forums'))
{act='ForumsQuestion';href=href1;}}
if(act.match('Slides')){act='Slides';href='Slides';}
if(act.match('files')||act.match('Codefiles')){act='Codefiles';href='Codefiles';}
if(href){log_data.push({timestamp:new Date().toLocaleTimeString(),action:act,url:href,videotime:video.currentTime,});}}}}
var log_data=[]
let pause=0
let play=0
if(0){let video=document.getElementById("st_video_html5_api")
let act_pp=''
let videotime=''
video.addEventListener('play',logData)
video.addEventListener('pause',logData)
var arrayWithElements=new Array();document.onclick=clickListener;}
function myfun(e){$.ajax({method:"POST",url:"/saveVideoData/",data:{video_log:log_data},csrfmiddlewaretoken:'xlcA3Qr3ASL7DmS8MGIyPMktJiFyQ2qzLyYZFh4vLfLXzmjt6AThNUZaOJaFI4Qy',}).done(function(msg){console.log("Data Saved: "+msg);});}
window.onbeforeunload=function(e){if(0){e.preventDefault();myfun(e);}};});var player,tag=document.createElement('script'),firstScriptTag=document.getElementsByTagName('script')[0];var flag=false;tag.src="https://www.youtube.com/iframe_api";firstScriptTag.parentNode.insertBefore(tag,firstScriptTag);function onPlaybackQualityChange(event){console.log(event);}
Number.prototype.between=function(min,max){return this>=min&&this<=max;};var ik_player;function onYouTubeIframeAPIReady(){ik_player=new YT.Player('player');ik_player.addEventListener("onReady","onReady");ik_player.addEventListener("onStateChange","onStateChange");}
function formatTime(time){time=Math.round(time);var minutes=Math.floor(time/60),seconds=time-minutes*60;seconds=seconds<10?'0'+seconds:seconds;return minutes+"."+seconds;}
function onReady(event){function logDuration(){window.setTimeout(logDuration,1000);var cur_time=formatTime(ik_player.getCurrentTime()).toString();var duration=formatTime(ik_player.getDuration()).toString();if(parseFloat(cur_time)==parseFloat(duration.toString())){$('.ScrollStyle').find('.question').css("background-color","white");}else{trigger(cur_time,duration);}
return cur_time}
logDuration();$("#text").click(function(e){ik_player.pauseVideo()
setForum(logDuration())});}
function trigger(cur_time,duration){min_range='01-02'
sec_range='10-20'
id='4099'
min_split=min_range.split("-")
sec_split=sec_range.split("-")
lower=min_split[0]+"."+sec_split[0];upper=min_split[1]+"."+sec_split[1];var div=document.getElementById('4099');if((parseFloat(cur_time)).between(parseFloat(lower.toString()),parseFloat(upper.toString())))
{bgColor=$("#"+'4099').css('background-color')
if($("#"+'4099').css("background-color")=="rgb(205, 205, 205)"){}else{var el=document.getElementById('forums_Q');el.scrollTop=0;}
$("#"+'4099').prependTo("#forum_Q");div.style.backgroundColor="#cdcdcd";}else{div.style.backgroundColor="#ffffff";}
min_range='02-03'
sec_range='10-20'
id='1979'
min_split=min_range.split("-")
sec_split=sec_range.split("-")
lower=min_split[0]+"."+sec_split[0];upper=min_split[1]+"."+sec_split[1];var div=document.getElementById('1979');if((parseFloat(cur_time)).between(parseFloat(lower.toString()),parseFloat(upper.toString())))
{bgColor=$("#"+'1979').css('background-color')
if($("#"+'1979').css("background-color")=="rgb(205, 205, 205)"){}else{var el=document.getElementById('forums_Q');el.scrollTop=0;}
$("#"+'1979').prependTo("#forum_Q");div.style.backgroundColor="#cdcdcd";}else{div.style.backgroundColor="#ffffff";}
min_range='0-1'
sec_range='0-10'
id='373'
min_split=min_range.split("-")
sec_split=sec_range.split("-")
lower=min_split[0]+"."+sec_split[0];upper=min_split[1]+"."+sec_split[1];var div=document.getElementById('373');if((parseFloat(cur_time)).between(parseFloat(lower.toString()),parseFloat(upper.toString())))
{bgColor=$("#"+'373').css('background-color')
if($("#"+'373').css("background-color")=="rgb(205, 205, 205)"){}else{var el=document.getElementById('forums_Q');el.scrollTop=0;}
$("#"+'373').prependTo("#forum_Q");div.style.backgroundColor="#cdcdcd";}else{div.style.backgroundColor="#ffffff";}}
var trackedPlayer=videojs('st_video');var previousTime=0;var currentTime=0;trackedPlayer.on('timeupdate',function(){previousTime=currentTime;currentTime=trackedPlayer.currentTime();var cur_time=formatTime(currentTime).toString();trigger(cur_time);$("#text").click(function(e){trackedPlayer.pause()
setForum(cur_time)});});function setForum(cur_time)
{var time_split=cur_time.split(".")
var minute=parseFloat(time_split[0]);var min_range=minute+"-"+(minute+parseFloat(1))
if(parseInt(time_split[1]).between(parseInt(0),parseInt(9))){sec_range="0-10"}else if(parseFloat(time_split[1]).between(parseFloat(10),parseFloat(19))){sec_range="10-20"}else if(parseFloat(time_split[1]).between(parseFloat(20),parseFloat(29))){sec_range="20-30"}else if(parseFloat(time_split[1]).between(parseFloat(30),parseFloat(39))){sec_range="30-40"}else if(parseFloat(time_split[1]).between(parseFloat(40),parseFloat(49))){sec_range="40-50"}else{sec_range="50-60"}
var url="https://forums.spoken-tutorial.org/new-question/?category=Advance C&tutorial=Command line arguments in C&minute_range="+min_range+"&second_range="+sec_range;$("#text").attr("href",url);}