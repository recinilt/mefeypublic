//xmlparse

// var myurl5 = document.getElementById("yturl").value;
// function yturl(params) {
//     myurl5 = document.getElementById("yturl").value;
//     if (myurl5 ) {
//         myurl4=myurl5;
//     }
// }
// + "&enablejsapi=1"

///////////////////// tts speech synthezer
   
var mytts = (function(){
    var mytext = "Merhabalar Merhabalar";
    const msg = new SpeechSynthesisUtterance();
    msg.volume = 1; // 0 to 1
    msg.rate = 1.8; // 0.1 to 10
    msg.pitch = 1; // 0 to 2
    msg.text  = mytext;
    
    
    const voice = {
        "name": "Yelda",
        "lang": "tr-TR"
      }; //speaks[35]; //47
    console.log(`Voice: ${voice.name} and Lang: ${voice.lang}`);
    msg.voiceURI = voice.name;
    msg.lang = voice.lang;
    
      var totts = function(tosay,volume0to1,rate0to10,pitch0to2){
          msg.text = tosay;
          if (volume0to1){msg.volume=volume0to1};
          if(rate0to10){msg.rate=rate0to10};
          if(pitch0to2){msg.pitch=pitch0to2};
        speechSynthesis.speak(msg);
      }
      return {
          totts
      };
    
    })();
    
    mytts.totts("merhabalar.");
  
            // function oku() {
            //     var text = document.getElementById("domtext").value;
            // console.log(text);
            // mytts.totts(text);
            // }
 
            
//////////////////////////////////////////

var myurl6 = "https://www.youtube.com/watch?v=kir-S1VoNgE&t=12s";
var myurl4 = "https://video.google.com/timedtext?lang=tr&v=yizckrcFsz8";
var vivid = "kir-S1VoNgE&t";
var myalert = document.getElementById("myalert");
function myurlparse(yturl) {
    myalert.innerHTML = "";
    var yturl = document.getElementById("yturl").value;
    var ytwindex = yturl.indexOf("watch?v=");
    var ytyindex = yturl.indexOf("youtu.be/");
    if (ytwindex > -1) {
        vivid = yturl.substr(ytwindex, 19).substr(8, 11);
        myurl4 = "https://video.google.com/timedtext?lang=tr&v=" + vivid;
        console.log(myurl4 + " " + vivid);
        //player.videoId=vivid;
        player.loadVideoById(vivid);
        myxhttp(myurl4);
        //ytapimyurl(vivid);
        return myurl4, vivid;
    } else if (ytyindex > -1) {
        vivid = yturl.substr(ytyindex, 20).substr(8, 11);
        myurl4 = "https://video.google.com/timedtext?lang=tr&v=" + vivid;
        console.log(myurl4 + " " + vivid);
        //player.videoId=vivid;
        player.loadVideoById(vivid);
        myxhttp(myurl4);
        //ytapimyurl(vivid);
        return myurl4, vivid;

    } else {
        console.log("adres geçersiz");
        myalert.innerHTML ="Tekrar Deneyiniz. Geçersiz Youtube Adresi Girildi.";
        //document.getElementById("yturl").innerHTML="Tekrar Deneyiniz. Geçersiz Youtube Adresi Girildi.";
    }

}

function mybadge(params) {
    document.getElementById("yturl").value="https://www.youtube.com/watch?v=64A8U2YC0b8";
    myurlparse();
}
// function ytapimyurl(vivid) {

//     player = new YT.Player('player', {
//         height: '390',
//         width: '640',
//         videoId: vivid,
//         events: {
//             'onReady': onPlayerReady,     //,
//             'onStateChange': onPlayerStateChange
//         }
        
//     });
// }

//myurlparse(myurl6)


function myxhttp(myurl4) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            myFunction(this);
        }
    };
    xhttp.open("GET", myurl4, true);
    xhttp.send();

}

myxhttp(myurl4);

var sentences;
var times;
var timesentencesobj = {};
var regexToSpace = /([&].{1,12}[;])|[!-@\[-`\{-~][a-zA-Z][!-@\[-`\{-~]?[!-@\[-`\{-~]|(["-&])|([\(-\+])|([-])|([/@])|([<->])|([\[-`])|([\{-~])/gmui;
var regexToComma = /([!\?:\n;])/gmui;

function sentenceparse(str) {
    console.log("sentenceparse begin");
    let i = 0;
    let sl = sentences.length;
    //console.log(sentences);
    for (i = 0; i < sl; i++) {
        sentences[i] = sentences[i].replace(regexToSpace, " ");
        sentences[i] = sentences[i].replace(regexToComma, ",");

    }
    return sentences;
}

function myFunction(xml) {

    var i, xmlDoc, l, sentencenodes;
    xmlDoc = xml.responseXML;
    //txt = "";
    times = [];
    sentences = [];

    sentencenodes = xmlDoc.getElementsByTagName("text");
    l = sentencenodes.length;
    for (i = 0; i < l; i++) {
        times.push(Number(sentencenodes[i].getAttributeNode("start").nodeValue).toFixed(0));
        sentences.push(sentencenodes[i].childNodes[0].nodeValue);
        //txt += x[i].getAttributeNode("start").nodeValue + "<br>";
    }
    sentenceparse(sentences);
    console.log(sentences);

    console.log(times);
    return times, sentences;
}

////////////////////////
//controller
var myinterval;
function startinterv(params) {
    myinterval = setInterval(myTimer, 1000);
}

var ytsec = 0;
var secindex = 0;
responsiveVoice.enableEstimationTimeout = false;
function myTimer() {
    ytsec = player.getCurrentTime().toFixed(0);
    console.log("times.includes(ytsec): " + times.includes(ytsec));
    //secindex = times.indexOf(Number(ytsec));
    if (times.includes(ytsec)) {
        secindex = times.indexOf(String(ytsec));
        console.log("secindex: " + secindex);
        console.log("sentences[secindex]: " + sentences[secindex]);


        //responsiveVoice.speak(sentences[secindex], "Turkish Female", { rate: 1.4 });
        mytts.totts(sentences[secindex])
    }
    console.log("ytsec: " + ytsec);
    //console.log("secindex: "+secindex);
}

function stopinterv(params) {
    clearInterval(myinterval);
}


/////////////////////////
//ytapi
// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('player', {
        height: '390',
        width: '100%',
        videoId: 'yizckrcFsz8',
        events: {
            'onReady': onPlayerReady,     //,
            'onStateChange': onPlayerStateChange
        }
        
    });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    //event.target.playVideo();
    console.log("player ready");
}
/*
// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
//var done = false;
// function onPlayerStateChange(event) {
//   if (event.data == YT.PlayerState.PLAYING) {
//     //setTimeout(stopVideo, 6000);
//     //done = true;
 
//   }
// }
// function stopVideo() {
//   player.stopVideo();
// }
 
 
///////////////////////////
 
      ////////////////////
/////////////////////
//import {responsiveVoice} from "https://code.responsivevoice.org/responsivevoice.js";
//let str=localStorage.getItem("mooji.srt");
*/
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING) {
        //setTimeout(stopVideo, 6000);
        //done = true;
        console.log("playing");
        startinterv();


    }
    if (event.data == YT.PlayerState.ENDED || event.data == YT.PlayerState.PAUSED || event.data == YT.PlayerState.BUFFERING) {
        console.log("paused");
        stopinterv();
    }
}
//   function stopVideo() {
//     player.stopVideo();
//   }

function curr() {
    console.log(player.getCurrentTime());
}
