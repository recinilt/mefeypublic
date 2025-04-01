const API_KEY = 'YOUR_YOUTUBE_API_KEY'; // Buraya kendi API anahtarınızı ekleyin.

function getVideoId(url) {
    const regex = /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

function listSubtitles(videoId) {
    fetch(`https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=${videoId}&key=${API_KEY}`)
        .then(response => response.json())
        .then(data => {
            if (data.items && data.items.length > 0) {
                const select = document.createElement('select');
                data.items.forEach(item => {
                    const option = document.createElement('option');
                    option.value = item.id;
                    option.textContent = item.snippet.language;
                    select.appendChild(option);
                });

                const downloadButton = document.createElement('button');
                downloadButton.textContent = 'Seçilen Altyazıyı İndir';
                downloadButton.onclick = () => {
                    const selectedCaptionId = select.value;
                    downloadCaption(selectedCaptionId);
                };

                document.body.appendChild(select);
                document.body.appendChild(downloadButton);
            } else {
                alert('Bu video için altyazı bulunamadı.');
            }
        })
        .catch(error => {
            console.error('Bir hata oluştu:', error);
            alert('Bir hata oluştu. Lütfen tekrar deneyin.');
        });
}

function downloadCaption(captionId) {
    // Altyazıyı SRT formatında indirmek için tfmt parametresini kullanıyoruz.
    const downloadUrl = `https://www.googleapis.com/youtube/v3/captions/${captionId}?key=${API_KEY}&tfmt=srt`;

    window.open(downloadUrl, '_blank');
}

function downloadSubtitle() {
    const videoUrl = document.getElementById('videoLink').value;
    const videoId = getVideoId(videoUrl);

    if (!videoId) {
        alert('Lütfen geçerli bir YouTube linki girin.');
        return;
    }

    listSubtitles(videoId);
}
