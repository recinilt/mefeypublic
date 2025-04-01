$(document).ready(function() {
    console.log( "document ready!" );




var myexp = /([a-z0-9_-]*)@sivers.org/igm;
var str ="My email is derek@sivers.org but no spam, reci@sivers.org ok?";
var matches = myexp.exec(str);
var rez="the whole thing is " + matches[0] + " and username is " + matches[1];
console.log(matches);
console.log(rez);

$("#mydiv").html("<h2>" + matches+"</h2>");
$("#mydiv2").html(rez);

var matches2 = str.match(myexp);
console.log(matches2);
$("#mydiv3").html(matches2);





});

