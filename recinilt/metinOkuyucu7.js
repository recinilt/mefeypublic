class DocumentReader {
    constructor() {
        this.currentFile = null;
        this.currentPosition = 0;
        this.recentFiles = this.loadRecentFiles();
        this.fontSize = parseInt(localStorage.getItem('fontSize') || '18');
        this.theme = localStorage.getItem('theme') || 'light';

        this.init();
        this.updateRecentFilesList();
        this.applyTheme();
        this.applyFontSize();
    }

    init() {
        const fileInput = document.getElementById('fileInput');

        fileInput.addEventListener('change', (e) => {
            this.handleFileSelect(e);
        });

        fileInput.addEventListener('input', (e) => {
            this.handleFileSelect(e);
        });

        document.getElementById('readerContainer').addEventListener('scroll',
            this.throttle(() => {
                this.saveReadingPosition();
                this.updateProgressBar();
            }, 500)
        );

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && document.getElementById('readerContainer').style.display !== 'none') {
                this.closeReader();
            }
        });
    }

    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }

    async handleFileSelect(event) {
        const files = event.target.files;

        if (files.length === 0) return;

        for (let file of files) {
            try {
                await this.processFile(file);
            } catch (error) {
                console.error('Dosya işlenirken hata:', error);
                alert('Dosya okuma hatası: ' + error.message);
            }
        }

        event.target.value = '';
    }

    async processFile(file) {
        const content = await this.readFileContent(file);
        const fileData = {
            name: file.name,
            content: content,
            lastRead: Date.now(),
            position: 0,
            size: file.size
        };

        this.addToRecentFiles(fileData);
        this.openFile(fileData);
    }

    async readFileContent(file) {
        const extension = file.name.split('.').pop().toLowerCase();

        switch (extension) {
            case 'txt':
                return await this.readTextFile(file);
            case 'pdf':
                return await this.readPDFFile(file);
            case 'doc':
            case 'docx':
                return await this.readWordFile(file);
            default:
                if (file.type && file.type.startsWith('text/')) {
                    return await this.readTextFile(file);
                }
                throw new Error('Desteklenmeyen dosya formatı: ' + extension);
        }
    }

    readTextFile(file) {
        return new Promise((resolve, reject) => {
            const nativeFileReader = new window.FileReader();
            nativeFileReader.onload = (e) => resolve(e.target.result);
            nativeFileReader.onerror = (e) => reject(new Error('Metin dosyası okunamadı'));
            nativeFileReader.readAsText(file, 'UTF-8');
        });
    }

    async readPDFFile(file) {
        try {
            const arrayBuffer = await file.arrayBuffer();
            const pdf = await pdfjsLib.getDocument(arrayBuffer).promise;
            let fullText = '';

            for (let i = 1; i <= pdf.numPages; i++) {
                const page = await pdf.getPage(i);
                const textContent = await page.getTextContent();
                const pageText = textContent.items.map(item => item.str).join(' ');
                fullText += pageText + '\n\n';
            }

            return fullText;
        } catch (error) {
            throw new Error('PDF dosyası okunamadı');
        }
    }

    async readWordFile(file) {
        try {
            const arrayBuffer = await file.arrayBuffer();
            const result = await mammoth.extractRawText({ arrayBuffer: arrayBuffer });
            return result.value;
        } catch (error) {
            throw new Error('Word dosyası okunamadı');
        }
    }

    openFile(fileData) {
        this.currentFile = fileData;
        document.getElementById('currentFileName').textContent = fileData.name;
        document.getElementById('readerContent').textContent = fileData.content;
        document.getElementById('readerContainer').style.display = 'block';

        setTimeout(() => {
            this.scrollToPosition(fileData.position);
            this.updateProgressBar();
        }, 200);
    }

    closeReader() {
        // Önce pozisyonu kaydet
        this.saveReadingPosition();
        // Listeyi güncelle ki yeni yüzde görünsün
        this.updateRecentFilesList();

        document.getElementById('readerContainer').style.display = 'none';
        this.currentFile = null;

    }

    scrollToPosition(position) {
        const container = document.getElementById('readerContainer');
        const content = document.getElementById('readerContent');

        // Eski hesaplama metodunu kullan (çalışıyordu)
        const contentHeight = content.scrollHeight;
        const containerHeight = container.clientHeight;
        const maxScrollTop = Math.max(0, contentHeight - containerHeight);

        const targetScroll = (position / 100) * maxScrollTop;
        container.scrollTop = Math.max(0, targetScroll);

        console.log('Pozisyona git:', {
            position: position,
            contentHeight: contentHeight,
            containerHeight: containerHeight,
            maxScrollTop: maxScrollTop,
            targetScroll: targetScroll,
            actualScroll: container.scrollTop
        });
    }

    saveReadingPosition() {
        if (!this.currentFile) return;

        const container = document.getElementById('readerContainer');
        const content = document.getElementById('readerContent');

        // Daha hassas hesaplama
        const contentHeight = content.scrollHeight;
        const containerHeight = container.clientHeight;
        const currentScrollTop = container.scrollTop;

        // Maksimum scroll değeri
        const maxScrollTop = Math.max(0, contentHeight - containerHeight);

        // Pozisyonu hesapla
        let scrollPercentage = 0;
        if (maxScrollTop > 0) {
            scrollPercentage = (currentScrollTop / maxScrollTop) * 100;
        }

        // 0-100 arasında sınırla
        this.currentFile.position = Math.max(0, Math.min(100, scrollPercentage));

        console.log('Pozisyon kaydediliyor:', {
            currentScrollTop: currentScrollTop,
            maxScrollTop: maxScrollTop,
            calculatedPercentage: scrollPercentage,
            savedPosition: this.currentFile.position
        });

        // Recent files'ta güncelle
        const recentFiles = this.loadRecentFiles();
        const fileIndex = recentFiles.findIndex(f => f.name === this.currentFile.name);
        if (fileIndex !== -1) {
            recentFiles[fileIndex].position = this.currentFile.position;
            recentFiles[fileIndex].lastRead = Date.now();
            localStorage.setItem('recentFiles', JSON.stringify(recentFiles));
            this.recentFiles = recentFiles;
        }
    }

    updateProgressBar() {
        if (!this.currentFile) return;

        const progressBar = document.getElementById('progressBar');
        progressBar.style.width = Math.round(this.currentFile.position) + '%';
    }

    addToRecentFiles(fileData) {
        let recentFiles = this.loadRecentFiles();

        recentFiles = recentFiles.filter(f => f.name !== fileData.name);
        recentFiles.unshift(fileData);
        recentFiles = recentFiles.slice(0, 10);

        localStorage.setItem('recentFiles', JSON.stringify(recentFiles));
        this.recentFiles = recentFiles;
        this.updateRecentFilesList();
    }

    loadRecentFiles() {
        const stored = localStorage.getItem('recentFiles');
        return stored ? JSON.parse(stored) : [];
    }

    updateRecentFilesList() {
        const container = document.getElementById('recentFilesList');

        if (this.recentFiles.length === 0) {
            container.innerHTML = '<div class="empty-state">Henüz hiç dosya açılmamış</div>';
            return;
        }

        container.innerHTML = this.recentFiles.map((file, index) => {
            // Güvenli progress hesaplama
            const progress = file.position ? Math.round(file.position) : 0;

            return `
                <div class="file-item" onclick="documentReader.openRecentFile('${this.escapeHtml(file.name)}')">
                    <div>
                        <div class="file-name">${this.escapeHtml(file.name)}</div>
                        <div class="file-progress">%${progress} okundu • ${this.formatDate(file.lastRead)}</div>
                    </div>
                    <div>
                        <button class="remove-btn" onclick="event.stopPropagation(); documentReader.removeRecentFile(${index})" title="Dosyayı listeden kaldır">
                            🗑️
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return String(text).replace(/[&<>"']/g, m => map[m]);
    }

    openRecentFile(fileName) {
        const file = this.recentFiles.find(f => f.name === fileName);
        if (file) {
            file.lastRead = Date.now();
            this.openFile(file);
        }
    }

    removeRecentFile(fileIndex) {
        if (fileIndex >= 0 && fileIndex < this.recentFiles.length) {
            this.recentFiles.splice(fileIndex, 1);
            localStorage.setItem('recentFiles', JSON.stringify(this.recentFiles));
            this.updateRecentFilesList();
        }
    }

    formatDate(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));

        if (diffDays === 0) return 'Bugün';
        if (diffDays === 1) return 'Dün';
        if (diffDays < 7) return `${diffDays} gün önce`;

        return date.toLocaleDateString('tr-TR');
    }

    changeFontSize(delta) {
        if (!this.currentFile) {
            this.fontSize += delta;
            this.fontSize = Math.max(12, Math.min(32, this.fontSize));
            this.applyFontSize();
            localStorage.setItem('fontSize', this.fontSize.toString());
            return;
        }

        // Mevcut scroll oranını kaydet (font değişikliği için)
        const currentScrollRatio = this.getCurrentScrollRatio();

        console.log('Font değişimi öncesi scroll oranı:', currentScrollRatio);

        // Font boyutunu değiştir
        this.fontSize += delta;
        this.fontSize = Math.max(12, Math.min(32, this.fontSize));
        localStorage.setItem('fontSize', this.fontSize.toString());

        // Font değişikliğini uygula
        this.applyFontSize();

        // Pozisyonu geri yükle
        this.restoreScrollRatio(currentScrollRatio);
    }

    getCurrentScrollRatio() {
        const container = document.getElementById('readerContainer');
        const content = document.getElementById('readerContent');

        const contentHeight = content.scrollHeight;
        const containerHeight = container.clientHeight;
        const maxScrollTop = Math.max(0, contentHeight - containerHeight);

        if (maxScrollTop === 0) return 0;

        return container.scrollTop / maxScrollTop;
    }

    restoreScrollRatio(targetRatio) {
        const container = document.getElementById('readerContainer');
        const content = document.getElementById('readerContent');

        // DOM'un tamamen güncellenmesini bekle
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    const contentHeight = content.scrollHeight;
                    const containerHeight = container.clientHeight;
                    const newMaxScrollTop = Math.max(0, contentHeight - containerHeight);

                    const newScrollTop = targetRatio * newMaxScrollTop;
                    container.scrollTop = Math.max(0, newScrollTop);

                    console.log('Font değişimi sonrası pozisyon geri yüklendi:', {
                        targetRatio,
                        newMaxScrollTop,
                        newScrollTop,
                        actualScrollTop: container.scrollTop
                    });

                    // Normal pozisyon kaydetme sistemini güncelle
                    setTimeout(() => {
                        this.saveReadingPosition();
                        this.updateProgressBar();
                    }, 100);
                });
            });
        });
    }

    applyFontSize() {
        document.getElementById('readerContent').style.fontSize = this.fontSize + 'px';
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme();
        localStorage.setItem('theme', this.theme);
    }

    applyTheme() {
        if (this.theme === 'dark') {
            document.body.classList.add('dark-theme');
            document.querySelector('.theme-toggle').textContent = '☀️ Açık Tema';
        } else {
            document.body.classList.remove('dark-theme');
            document.querySelector('.theme-toggle').textContent = '🌙 Koyu Tema';
        }
    }
}

// Global fonksiyonlar
function changeFontSize(delta) {
    documentReader.changeFontSize(delta);
}

function toggleTheme() {
    documentReader.toggleTheme();
}

function closeReader() {

    documentReader.closeReader();

}

// Uygulamayı başlat
const documentReader = new DocumentReader();

// PDF.js konfigürasyonu
if (typeof pdfjsLib !== 'undefined') {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';
}