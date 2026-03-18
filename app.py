from flask import Flask, send_from_directory
import os

app = Flask(__name__)

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZAKARIA · personal page</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    
    <!-- Preload الفيديو لتحميل أسرع -->
    <link rel="preload" as="video" href="/bg-loop.mp4" type="video/mp4">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Roboto, system-ui, sans-serif;
        }

        body {
            min-height: 100vh;
            background-color: #0b0f10;
            color: #e3e9ef;
            line-height: 1.5;
            position: relative;
            overflow-x: hidden;
        }

        /* صفحة البداية */
        .splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0b0f10;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            cursor: pointer;
            transition: opacity 0.8s ease, visibility 0.8s;
        }

        .splash-screen.hidden {
            opacity: 0;
            visibility: hidden;
        }

        .splash-content {
            text-align: center;
            padding: 2rem;
        }

        .splash-content h1 {
            font-size: 4rem;
            margin-bottom: 1rem;
            color: #3b82c9;
            letter-spacing: 5px;
            animation: pulse 2s infinite;
        }

        .splash-content p {
            font-size: 1.5rem;
            color: #a8b9c6;
            margin-top: 2rem;
            border: 2px solid #3b82c9;
            padding: 1rem 2rem;
            border-radius: 60px;
            display: inline-block;
            animation: glow 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 0.7; }
            50% { opacity: 1; text-shadow: 0 0 20px #3b82c9; }
            100% { opacity: 0.7; }
        }

        @keyframes glow {
            0% { box-shadow: 0 0 10px #3b82c9; }
            50% { box-shadow: 0 0 30px #3b82c9; }
            100% { box-shadow: 0 0 10px #3b82c9; }
        }

        /* خلفية ثابتة تظهر أثناء تحميل الفيديو */
        .video-fallback {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #0b0f10;
            z-index: -2;
        }

        /* الفيديو الخلفي - تم زيادة الشفافية */
        .bg-video {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0;
            transition: opacity 1.5s ease;
            z-index: -1;
        }

        .bg-video.loaded {
            opacity: 0.35;  /* تم التعديل من 0.2 إلى 0.35 */
        }

        .main-content {
            max-width: 700px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
            position: relative;
            backdrop-filter: blur(2px);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            opacity: 0;
            transition: opacity 1s ease;
        }

        .main-content.visible {
            opacity: 1;
        }

        .profile {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 2rem;
        }
        .profile-img {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #3b82c9;
            box-shadow: 0 0 20px rgba(59, 130, 201, 0.3);
            background-color: #1e2629;
        }
        .profile h1 {
            font-size: 2.8rem;
            font-weight: 500;
            letter-spacing: 2px;
            margin-top: 0.5rem;
            margin-bottom: 0.3rem;
            text-shadow: 0 2px 5px rgba(0,0,0,0.5);
            color: #f0f5fa;
        }
        .description {
            color: #a8b9c6;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            word-spacing: 4px;
            background: rgba(20, 30, 35, 0.6);
            padding: 0.3rem 1rem;
            border-radius: 40px;
            backdrop-filter: blur(4px);
            border: 1px solid #2e404b;
        }

        .music-player {
            background: rgba(10, 18, 22, 0.8);
            backdrop-filter: blur(8px);
            border-radius: 80px;
            padding: 0.8rem 1.5rem;
            margin: 2rem 0 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px solid #2b3f4b;
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
            flex-wrap: wrap;
            gap: 15px;
        }

        .track-icons {
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
        }

        .track-icon {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
            transition: 0.2s;
            object-fit: cover;
            background: #1e2f38;
        }

        .track-icon:hover {
            transform: scale(1.1);
            border-color: #3b82c9;
        }

        .track-icon.active {
            border-color: #3b82c9;
            box-shadow: 0 0 15px #3b82c9;
        }

        .player-controls {
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .player-controls button {
            background: transparent;
            border: none;
            color: #b4cfdd;
            font-size: 1.4rem;
            cursor: pointer;
            transition: 0.2s;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }

        .player-controls button:hover {
            color: white;
            background: #1e3a4a;
        }

        #playPauseBtn {
            background: #1e4055;
            color: white;
            width: 50px;
            height: 50px;
        }
        #playPauseBtn:hover {
            background: #2a5a75;
        }

        .tg-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 1.5rem 0 2rem;
        }
        .tg-btn {
            flex: 1;
            background: rgba(18, 32, 40, 0.8);
            backdrop-filter: blur(5px);
            border: 1px solid #2e5f77;
            color: #ddeeff;
            padding: 0.9rem 0.5rem;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 500;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: 0.25s;
            letter-spacing: 0.5px;
        }
        .tg-btn i {
            color: #3b82c9;
            font-size: 1.3rem;
        }
        .tg-btn:hover {
            background: #1d3f50;
            border-color: #4b9fd8;
            color: white;
            transform: scale(1.02);
        }

        .social-links {
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            margin: 1.8rem 0;
        }
        .social-icon {
            background: rgba(15, 25, 30, 0.7);
            backdrop-filter: blur(4px);
            width: 55px;
            height: 55px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            transition: 0.2s;
            border: 1px solid #3d5663;
            color: #cbdbe5;
            text-decoration: none;
        }
        .social-icon:hover {
            transform: translateY(-5px);
            border-color: #5b9bc7;
        }
        .social-icon.fa-telegram:hover {
            background: #0088cc;
            color: white;
        }
        .social-icon.fa-youtube:hover {
            background: #ff0000;
            color: white;
        }
        .social-icon.fa-facebook:hover {
            background: #1877f2;
            color: white;
        }

        .gallery-launcher {
            text-align: center;
            margin: 1.5rem 0 1rem;
        }
        .gallery-icon-btn {
            background: none;
            border: 2px solid #3b82c9;
            color: #cde1f0;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            font-size: 2.2rem;
            cursor: pointer;
            transition: 0.25s;
            background: rgba(10, 20, 28, 0.6);
            backdrop-filter: blur(4px);
        }
        .gallery-icon-btn:hover {
            background: #1b3e57;
            color: white;
            border-color: #72b8f0;
            transform: scale(1.07);
        }
        .gallery-icon-btn i {
            filter: drop-shadow(0 0 5px #3b82c9);
        }

        .gallery-page {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            min-height: 100vh;
            background: rgba(3, 8, 12, 0.97);
            backdrop-filter: blur(12px);
            z-index: 2000;
            padding: 2rem;
            overflow-y: auto;
            transform: translateY(100%);
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
        }
        .gallery-page.active {
            transform: translateY(0);
        }
        .gallery-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            color: #c9dbe8;
            border-bottom: 1px solid #2a4b5c;
            padding-bottom: 1rem;
        }
        .gallery-header h2 {
            font-weight: 400;
            font-size: 2rem;
            letter-spacing: 3px;
        }
        .close-gallery {
            background: transparent;
            border: none;
            color: #b0d0e0;
            font-size: 2.5rem;
            cursor: pointer;
            transition: 0.2s;
            line-height: 1;
        }
        .close-gallery:hover {
            color: #f0f8ff;
        }
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }
        .gallery-item {
            background: #101e26;
            border-radius: 20px;
            overflow: hidden;
            aspect-ratio: 1 / 1;
            border: 1px solid #2d5568;
            transition: 0.2s;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.6);
        }
        .gallery-item:hover {
            transform: scale(1.02);
            border-color: #4b8bb0;
        }
        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .footer-desc {
            margin-top: auto;
            text-align: center;
            color: #889faa;
            font-size: 0.9rem;
            padding-top: 2rem;
            border-top: 1px solid #20323d;
        }

        @media (max-width: 600px) {
            .music-player {
                flex-direction: column;
                align-items: stretch;
                border-radius: 40px;
            }
            .track-icons {
                justify-content: center;
            }
            .player-controls {
                justify-content: center;
            }
            .profile h1 { font-size: 2.2rem; }
            .tg-buttons { flex-direction: column; }
            .splash-content h1 { font-size: 2.5rem; }
            .splash-content p { font-size: 1.2rem; }
        }
    </style>
</head>
<body>

    <!-- صفحة البداية -->
    <div class="splash-screen" id="splashScreen">
        <div class="splash-content">
            <h1>ZAKARIA</h1>
            <p>CLICK ANYWHERE TO CONTINUE...</p>
        </div>
    </div>

    <!-- خلفية ثابتة -->
    <div class="video-fallback"></div>

    <!-- الفيديو الخلفي -->
    <video class="bg-video" id="bgVideo" autoplay muted loop playsinline preload="auto" fetchpriority="high">
        <source src="/bg-loop.mp4" type="video/mp4">
    </video>

    <div class="main-content" id="mainPage">
        <div class="profile">
            <img src="/imag.jpg" alt="profile" class="profile-img" onerror="this.src='https://via.placeholder.com/130x130?text=ZAKARIA'">
            <h1>ZAKARIA</h1>
            <div class="description">free games · bots · spam · tools</div>
        </div>

        <div class="music-player">
            <div class="track-icons" id="trackIcons"></div>
            <div class="player-controls">
                <button id="prevTrackBtn"><i class="fas fa-step-backward"></i></button>
                <button id="playPauseBtn"><i class="fas fa-play"></i></button>
                <button id="nextTrackBtn"><i class="fas fa-step-forward"></i></button>
            </div>
        </div>

        <div class="tg-buttons">
            <a href="https://t.me/Ziko_Tim" target="_blank" class="tg-btn"><i class="fab fa-telegram"></i> Telegram channel</a>
            <a href="https://t.me/MTX_SX_CHAT_TEAM" target="_blank" class="tg-btn"><i class="fab fa-telegram"></i> Telegram group</a>
        </div>

        <div class="social-links">
            <a href="https://t.me/ZikoB0SS" target="_blank" class="social-icon fab fa-telegram"></a>
            <a href="https://youtube.com/@ziko_boss?si=ympG79N5FiLO0qZI" target="_blank" class="social-icon fab fa-youtube"></a>
            <a href="https://www.facebook.com/profile.php?id=61586247175238" target="_blank" class="social-icon fab fa-facebook-f"></a>
        </div>

        <div class="gallery-launcher">
            <button class="gallery-icon-btn" id="openGalleryBtn"><i class="fas fa-images"></i></button>
        </div>

        <div class="footer-desc">
            <span> @ZikoB0SS </span>
        </div>
    </div>

    <div class="gallery-page" id="galleryPage">
        <div class="gallery-header">
            <h2>PROJECT GALLERY</h2>
            <button class="close-gallery" id="closeGalleryBtn">&times;</button>
        </div>
        <div class="gallery-grid" id="galleryGrid"></div>
        <div style="margin-top: 2rem; text-align: center; color: #3f6279;">ZAKARIA · archive</div>
    </div>

    <script>
        (function() {
            // إظهار الفيديو بعد تحميله
            const video = document.getElementById('bgVideo');
            video.addEventListener('loadeddata', function() {
                video.classList.add('loaded');
            });

            // عناصر الصفحة
            const splashScreen = document.getElementById('splashScreen');
            const mainPage = document.getElementById('mainPage');
            
            // تعريف قائمة المقاطع الصوتية
            const tracks = [
                { src: '/audio/song1.mp3', icon: '/icons/icon1.png' },
                { src: '/audio/song2.mp3', icon: '/icons/icon2.png' },
                { src: '/audio/song3.mp3', icon: '/icons/icon3.png' },
                { src: '/audio/song4.mp3', icon: '/icons/icon4.png' }
            ];

            let currentTrack = 0;
            const audio = new Audio();
            audio.src = tracks[currentTrack].src;
            audio.loop = false;

            // عناصر التحكم بالموسيقى
            const playPauseBtn = document.getElementById('playPauseBtn');
            const prevBtn = document.getElementById('prevTrackBtn');
            const nextBtn = document.getElementById('nextTrackBtn');
            const trackIconsDiv = document.getElementById('trackIcons');

            // إنشاء أيقونات المقاطع
            tracks.forEach((track, index) => {
                const img = document.createElement('img');
                img.src = track.icon;
                img.alt = `track ${index+1}`;
                img.className = 'track-icon';
                if (index === currentTrack) img.classList.add('active');
                
                img.addEventListener('click', () => {
                    if (index !== currentTrack) {
                        currentTrack = index;
                        audio.src = tracks[currentTrack].src;
                        audio.play().catch(() => {});
                        playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                        updateActiveIcon();
                    } else {
                        if (audio.paused) {
                            audio.play().catch(() => {});
                            playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                        } else {
                            audio.pause();
                            playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
                        }
                    }
                });

                trackIconsDiv.appendChild(img);
            });

            function updateActiveIcon() {
                const icons = document.querySelectorAll('.track-icon');
                icons.forEach((icon, idx) => {
                    if (idx === currentTrack) {
                        icon.classList.add('active');
                    } else {
                        icon.classList.remove('active');
                    }
                });
            }

            // أزرار التحكم
            playPauseBtn.addEventListener('click', function() {
                if (audio.paused) {
                    audio.play().catch(e => console.log('playback failed:', e));
                    playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                } else {
                    audio.pause();
                    playPauseBtn.innerHTML = '<i class="fas fa-play"></i>';
                }
            });

            prevBtn.addEventListener('click', function() {
                currentTrack = (currentTrack - 1 + tracks.length) % tracks.length;
                audio.src = tracks[currentTrack].src;
                audio.play().catch(() => {});
                playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                updateActiveIcon();
            });

            nextBtn.addEventListener('click', function() {
                currentTrack = (currentTrack + 1) % tracks.length;
                audio.src = tracks[currentTrack].src;
                audio.play().catch(() => {});
                playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                updateActiveIcon();
            });

            audio.addEventListener('ended', function() {
                currentTrack = (currentTrack + 1) % tracks.length;
                audio.src = tracks[currentTrack].src;
                audio.play().catch(() => {});
                playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
                updateActiveIcon();
            });

            // عند الضغط على صفحة البداية
            splashScreen.addEventListener('click', function() {
                splashScreen.classList.add('hidden');
                mainPage.classList.add('visible');
                audio.play().catch(e => console.log('Playback started after click:', e));
                playPauseBtn.innerHTML = '<i class="fas fa-pause"></i>';
            });

            // معرض الصور
            const galleryPage = document.getElementById('galleryPage');
            const openBtn = document.getElementById('openGalleryBtn');
            const closeBtn = document.getElementById('closeGalleryBtn');
            const galleryGrid = document.getElementById('galleryGrid');

            openBtn.addEventListener('click', function() {
                galleryPage.classList.add('active');
            });

            closeBtn.addEventListener('click', function() {
                galleryPage.classList.remove('active');
            });

            // إنشاء صور المعرض
            const imageCount = 6;
            for (let i = 1; i <= imageCount; i++) {
                const item = document.createElement('div');
                item.className = 'gallery-item';
                const img = document.createElement('img');
                img.src = `/images/image${i}.jpg`;
                img.alt = `project ${i}`;
                img.onerror = function() { 
                    this.src = 'https://via.placeholder.com/300x300?text=ZAKARIA'; 
                };
                item.appendChild(img);
                galleryGrid.appendChild(item);
            }
        })();
    </script>
</body>
</html>'''

@app.route('/')
def index():
    return HTML_CONTENT

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('audio', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

@app.route('/icons/<path:filename>')
def serve_icons(filename):
    return send_from_directory('icons', filename)

@app.route('/<path:filename>')
def serve_root(filename):
    if filename in ['imag.jpg', 'bg-loop.mp4', 'favicon.ico']:
        return send_from_directory('.', filename)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)