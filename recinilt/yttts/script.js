const API_KEY = 'AIzaSyATljp0o2LnBXL2IMrX9sNie6eUHOuBCKE'; // Buraya kendi YouTube Data API anahtarınızı ekleyin.

function getVideoId(url) {
    const regex = /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

function parseSRT(data) {
    const regex = /(\d+)\s+\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\s+([\s\S]*?)(?=\n\n|$)/g;
    let match;
    const subtitles = [];

    while (match = regex.exec(data)) {
        subtitles.push({
            id: match[1],
            text: match[2].trim()
        });
    }

    return subtitles;
}

function speakSubtitle(subtitles, index) {
    if (index < subtitles.length) {
        const utterance = new SpeechSynthesisUtterance(subtitles[index].text);
        utterance.onend = () => {
            speakSubtitle(subtitles, index + 1);
        };
        window.speechSynthesis.speak(utterance);
    }
}

function startVideoAndTTS() {
    const videoUrl = document.getElementById('videoLink').value;
    const videoId = getVideoId(videoUrl);

    if (!videoId) {
        alert('Lütfen geçerli bir YouTube linki girin.');
        return;
    }

    // YouTube videoyu iframe içerisinde başlat
    const iframe = document.getElementById('youtubeVideo');
    iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;

    // Altyazıları al ve TTS ile seslendir
    fetchSubtitlesAndSpeak(videoId);
}

function fetchSubtitlesAndSpeak(videoId) {
    fetch(`https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${videoId}&key=${API_KEY}`)
        .then(response => response.json())
        .then(data => {
            if (data.items && data.items.length > 0) {
                const firstSubtitleId = data.items[0].id;
                return fetch(`https://www.googleapis.com/youtube/v3/captions/${firstSubtitleId}?key=${API_KEY}&tfmt=srt`);
            } else {
                throw new Error('No subtitles found for this video.');
            }
        })
        .then(response => response.text())
        .then(srtData => {
            const subtitles = parseSRT(srtData);
            speakSubtitle(subtitles, 0);
        })
        .catch(error => {
            console.error('An error occurred:', error);
            alert('Bir hata oluştu. Lütfen tekrar deneyin.');
        });
}
