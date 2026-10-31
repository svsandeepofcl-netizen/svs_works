/**
 * Jungle Viper - Realistic Snake Hunt
 * Features:
 * - Realistic snake morphology (tapered head, amber slit eyes, flickering tongue, scale shading)
 * - Authentic jungle floor backdrop with ambient floating fireflies
 * - Dynamic size growth on fruit consumption
 * - Accurate self-collision and wall-collision detection
 * - Relaxed, balanced movement speed (135ms default)
 * - User Profile Management:
 *   * First-time name prompt
 *   * Returning user acknowledgment
 *   * End-of-game choice: "Continue as Current User" vs "New User / Switch"
 *   * Top 5 Leaderboard attributed to active Hunter Name
 * - Synthesized Web Audio API sound effects
 */

(() => {
    // --- Canvas & Grid Setup ---
    const canvas = document.getElementById("game-canvas");
    const ctx = canvas.getContext("2d");

    const GRID_SIZE = 20; // 20px per cell
    const GRID_COLS = canvas.width / GRID_SIZE; // 32
    const GRID_ROWS = canvas.height / GRID_SIZE; // 32

    // --- DOM Elements ---
    const currentScoreEl = document.getElementById("current-score");
    const snakeLengthEl = document.getElementById("snake-length");
    const topScoreBadgeEl = document.getElementById("top-score-badge");
    const topScoresListEl = document.getElementById("top-scores-list");
    const speedSelectEl = document.getElementById("speed-select");
    const muteBtnEl = document.getElementById("mute-btn");
    const muteIconEl = document.getElementById("mute-icon");

    // Header Profile
    const activeHunterDisplay = document.getElementById("active-hunter-display");
    const headerSwitchBtn = document.getElementById("header-switch-btn");

    // Overlays
    const startOverlay = document.getElementById("start-overlay");
    const gameOverOverlay = document.getElementById("game-over-overlay");
    const pauseOverlay = document.getElementById("pause-overlay");
    const nameModalOverlay = document.getElementById("name-modal-overlay");

    // Start Overlay elements
    const startModalTitle = document.getElementById("start-modal-title");
    const namePromptSection = document.getElementById("name-prompt-section");
    const hunterNameInput = document.getElementById("hunter-name-input");
    const returningPlayerSection = document.getElementById("returning-player-section");
    const returningHunterName = document.getElementById("returning-hunter-name");
    const startBtn = document.getElementById("start-btn");
    const switchUserBtn = document.getElementById("switch-user-btn");

    // Game Over Overlay elements
    const deathReasonEl = document.getElementById("death-reason");
    const finalScoreValueEl = document.getElementById("final-score-value");
    const gameOverHunterLabel = document.getElementById("game-over-hunter-label");
    const top5BadgeAnnouncement = document.getElementById("top5-badge-announcement");
    const top5HunterAck = document.getElementById("top5-hunter-ack");
    const continueUserBtn = document.getElementById("continue-user-btn");
    const gameOverNewUserBtn = document.getElementById("game-over-new-user-btn");

    // Name Change Modal elements
    const modalNameInput = document.getElementById("modal-name-input");
    const modalSaveNameBtn = document.getElementById("modal-save-name-btn");
    const modalCancelBtn = document.getElementById("modal-cancel-btn");

    const resumeBtn = document.getElementById("resume-btn");

    // --- User Profile State ---
    const HUNTER_KEY = "jungle_viper_active_hunter";
    let activeHunter = localStorage.getItem(HUNTER_KEY) || "";

    function setActiveHunter(name) {
        const trimmed = (name || "").trim() || "Explorer";
        activeHunter = trimmed;
        localStorage.setItem(HUNTER_KEY, trimmed);
        activeHunterDisplay.textContent = trimmed;
        returningHunterName.textContent = trimmed;
        continueUserBtn.textContent = `CONTINUE AS ${trimmed.toUpperCase()} (R)`;
    }

    // --- Audio Synthesizer (Web Audio API) ---
    class SoundSynth {
        constructor() {
            this.ctx = null;
            this.muted = false;
        }

        init() {
            if (!this.ctx) {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                if (AudioCtx) this.ctx = new AudioCtx();
            }
            if (this.ctx && this.ctx.state === "suspended") {
                this.ctx.resume();
            }
        }

        playChomp() {
            if (this.muted) return;
            this.init();
            if (!this.ctx) return;

            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = "sine";
            osc.frequency.setValueAtTime(220, now);
            osc.frequency.exponentialRampToValueAtTime(580, now + 0.08);

            gain.gain.setValueAtTime(0.28, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now);
            osc.stop(now + 0.12);
        }

        playCrash() {
            if (this.muted) return;
            this.init();
            if (!this.ctx) return;

            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(140, now);
            osc.frequency.exponentialRampToValueAtTime(40, now + 0.35);

            gain.gain.setValueAtTime(0.4, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now);
            osc.stop(now + 0.4);
        }

        playFanfare() {
            if (this.muted) return;
            this.init();
            if (!this.ctx) return;

            const notes = [261.63, 329.63, 392.00, 523.25];
            notes.forEach((freq, i) => {
                const now = this.ctx.currentTime + (i * 0.09);
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();

                osc.type = "triangle";
                osc.frequency.setValueAtTime(freq, now);

                gain.gain.setValueAtTime(0.25, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);

                osc.connect(gain);
                gain.connect(this.ctx.destination);

                osc.start(now);
                osc.stop(now + 0.22);
            });
        }
    }

    const sound = new SoundSynth();

    // --- Jungle Texture Loader ---
    const bgImage = new Image();
    let bgLoaded = false;
    bgImage.src = "assets/jungle_bg.jpg";
    bgImage.onload = () => { bgLoaded = true; };

    // --- Ambient Fireflies & Spores ---
    const fireflies = [];
    for (let i = 0; i < 24; i++) {
        fireflies.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2 + 1,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            alpha: Math.random() * 0.7 + 0.2,
            pulseSpeed: Math.random() * 0.03 + 0.01
        });
    }

    // --- Particle Burst on Fruit Eat ---
    const particles = [];
    function spawnParticles(x, y, color) {
        for (let i = 0; i < 16; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 3.5 + 1;
            particles.push({
                x,
                y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                radius: Math.random() * 3 + 1.5,
                color,
                life: 1.0,
                decay: Math.random() * 0.04 + 0.02
            });
        }
    }

    // --- Game State ---
    let snake = [];
    let direction = { x: 1, y: 0 };
    let nextDirection = { x: 1, y: 0 };
    let food = { x: 15, y: 15, type: 0 };
    let score = 0;
    let isRunning = false;
    let isPaused = false;
    let gameLoopTimeout = null;
    let tongueTimer = 0;

    // Slower, comfortable default: 135ms
    let stepInterval = parseInt(speedSelectEl.value, 10) || 135;

    const FRUIT_TYPES = [
        { name: "Dragon Berry", color: "#f43f5e", glow: "#fb7185", leaf: "#4ade80", points: 10 },
        { name: "Golden Mango", color: "#f59e0b", glow: "#fde047", leaf: "#86efac", points: 15 },
        { name: "Jungle Fig", color: "#a855f7", glow: "#c084fc", leaf: "#34d399", points: 20 }
    ];

    // --- Top 5 Leaderboard Storage ---
    const LEADERBOARD_KEY = "jungle_viper_top5_scores";
    const DEFAULT_LEADERBOARD = [
        { name: "Anaconda King", score: 250, date: "Champion" },
        { name: "Green Mamba", score: 180, date: "Elite" },
        { name: "Emerald Viper", score: 120, date: "Hunter" },
        { name: "Cobra Scout", score: 70, date: "Scout" },
        { name: "Rainforest Novice", score: 30, date: "Novice" }
    ];

    function getTopScores() {
        try {
            const stored = localStorage.getItem(LEADERBOARD_KEY);
            if (stored) {
                const parsed = JSON.parse(stored);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    return parsed.slice(0, 5);
                }
            }
        } catch (e) {
            console.warn("Storage access restricted:", e);
        }
        return [...DEFAULT_LEADERBOARD];
    }

    function saveTopScores(scores) {
        try {
            scores.sort((a, b) => b.score - a.score);
            const top5 = scores.slice(0, 5);
            localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(top5));
            return top5;
        } catch (e) {
            console.warn("Could not save to localStorage:", e);
            return scores.slice(0, 5);
        }
    }

    function renderLeaderboard() {
        const scores = getTopScores();
        topScoresListEl.innerHTML = "";

        const medals = ["🥇", "🥈", "🥉", "4th", "5th"];

        scores.forEach((item, index) => {
            const li = document.createElement("li");
            li.className = `leader-item rank-${index + 1}`;
            li.innerHTML = `
                <div class="leader-left">
                    <span class="rank-badge">${medals[index]}</span>
                    <span class="hunter-name">${escapeHTML(item.name)}</span>
                </div>
                <span class="hunter-score">${item.score} pts</span>
            `;
            topScoresListEl.appendChild(li);
        });

        const highest = scores.length > 0 ? scores[0].score : 0;
        topScoreBadgeEl.textContent = highest;
    }

    function escapeHTML(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    function isScoreEligibleForTop5(currentScore) {
        if (currentScore <= 0) return false;
        const scores = getTopScores();
        if (scores.length < 5) return true;
        return currentScore > scores[scores.length - 1].score;
    }

    // --- Setup Start Overlay for First-Time vs Returning Player ---
    function setupStartOverlayUI() {
        if (!activeHunter) {
            // First time user
            startModalTitle.textContent = "WELCOME TO THE JUNGLE";
            namePromptSection.classList.remove("hidden");
            returningPlayerSection.classList.add("hidden");
            switchUserBtn.classList.add("hidden");
            startBtn.textContent = "START EXPEDITION (ENTER)";
            setTimeout(() => hunterNameInput.focus(), 250);
        } else {
            // Returning user
            startModalTitle.textContent = "READY TO HUNT?";
            namePromptSection.classList.add("hidden");
            returningPlayerSection.classList.remove("hidden");
            returningHunterName.textContent = activeHunter;
            switchUserBtn.classList.remove("hidden");
            startBtn.textContent = `HUNT AS ${activeHunter.toUpperCase()} (ENTER)`;
        }
    }

    // --- Reset Game State ---
    function resetGame() {
        const startX = 10;
        const startY = 16;
        snake = [
            { x: startX, y: startY },
            { x: startX - 1, y: startY },
            { x: startX - 2, y: startY }
        ];

        direction = { x: 1, y: 0 };
        nextDirection = { x: 1, y: 0 };
        score = 0;
        currentScoreEl.textContent = "0";
        snakeLengthEl.textContent = snake.length;

        spawnFood();
    }

    function spawnFood() {
        let valid = false;
        let newX, newY;

        while (!valid) {
            newX = Math.floor(Math.random() * (GRID_COLS - 4)) + 2;
            newY = Math.floor(Math.random() * (GRID_ROWS - 4)) + 2;
            valid = !snake.some(seg => seg.x === newX && seg.y === newY);
        }

        const rand = Math.random();
        let typeIndex = 0;
        if (rand > 0.85) typeIndex = 2; // Jungle Fig
        else if (rand > 0.6) typeIndex = 1; // Golden Mango

        food = { x: newX, y: newY, type: typeIndex };
    }

    // --- Game Loop ---
    function gameLoop() {
        if (!isRunning || isPaused) return;

        update();
        draw();

        gameLoopTimeout = setTimeout(gameLoop, stepInterval);
    }

    // --- Update Logic ---
    function update() {
        direction = { ...nextDirection };

        const head = {
            x: snake[0].x + direction.x,
            y: snake[0].y + direction.y
        };

        // 1. Boundary collision
        if (head.x < 0 || head.x >= GRID_COLS || head.y < 0 || head.y >= GRID_ROWS) {
            handleGameOver("The viper crashed into dense jungle perimeter vines!");
            return;
        }

        // 2. Self-collision: Touching its own body
        for (let i = 0; i < snake.length; i++) {
            if (head.x === snake[i].x && head.y === snake[i].y) {
                handleGameOver("The viper bit its own body! Self-cannibalism is fatal.");
                return;
            }
        }

        snake.unshift(head);

        // Check if food eaten
        if (head.x === food.x && head.y === food.y) {
            const fruitInfo = FRUIT_TYPES[food.type];
            score += fruitInfo.points;
            currentScoreEl.textContent = score;
            snakeLengthEl.textContent = snake.length;

            sound.playChomp();
            spawnParticles(
                head.x * GRID_SIZE + GRID_SIZE / 2,
                head.y * GRID_SIZE + GRID_SIZE / 2,
                fruitInfo.glow
            );

            spawnFood();
            // Size increases because we don't pop tail!
        } else {
            snake.pop();
        }

        tongueTimer++;
    }

    // --- Game Over ---
    function handleGameOver(reason) {
        isRunning = false;
        clearTimeout(gameLoopTimeout);
        sound.playCrash();

        // Screen shake
        canvas.style.transform = "translate(4px, -4px)";
        setTimeout(() => { canvas.style.transform = "translate(-4px, 4px)"; }, 60);
        setTimeout(() => { canvas.style.transform = "translate(0, 0)"; }, 120);

        deathReasonEl.textContent = reason;
        finalScoreValueEl.textContent = score;
        gameOverHunterLabel.textContent = `${activeHunter}'s Score`;

        // Check if Top 5 Score & Auto-record under active hunter
        if (isScoreEligibleForTop5(score)) {
            sound.playFanfare();
            const scores = getTopScores();
            scores.push({
                name: activeHunter,
                score,
                date: new Date().toLocaleDateString()
            });
            saveTopScores(scores);
            renderLeaderboard();

            top5HunterAck.textContent = `Excellent run, ${activeHunter}! You are in the Top 5.`;
            top5BadgeAnnouncement.classList.remove("hidden");
        } else {
            top5BadgeAnnouncement.classList.add("hidden");
        }

        continueUserBtn.textContent = `CONTINUE AS ${activeHunter.toUpperCase()} (R)`;

        gameOverOverlay.classList.remove("hidden");
        gameOverOverlay.classList.add("active");
    }

    // --- Realistic Drawing Routines ---
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 1. Jungle Background
        if (bgLoaded) {
            ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height);
            const vignette = ctx.createRadialGradient(
                canvas.width / 2, canvas.height / 2, canvas.width * 0.35,
                canvas.width / 2, canvas.height / 2, canvas.width * 0.72
            );
            vignette.addColorStop(0, "rgba(4, 18, 9, 0.25)");
            vignette.addColorStop(1, "rgba(2, 8, 4, 0.75)");
            ctx.fillStyle = vignette;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        } else {
            ctx.fillStyle = "#0a2012";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        // 2. Grid floor lines
        ctx.strokeStyle = "rgba(46, 125, 50, 0.12)";
        ctx.lineWidth = 1;
        for (let x = 0; x <= canvas.width; x += GRID_SIZE) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y <= canvas.height; y += GRID_SIZE) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        // 3. Draw Food
        drawFood();

        // 4. Draw Snake
        drawSnake();

        // 5. Draw Particles
        drawParticles();

        // 6. Draw Ambient Jungle Fireflies
        drawFireflies();
    }

    function drawFood() {
        const fx = food.x * GRID_SIZE + GRID_SIZE / 2;
        const fy = food.y * GRID_SIZE + GRID_SIZE / 2;
        const fruitInfo = FRUIT_TYPES[food.type];

        ctx.save();

        // Outer Fruit Glow
        const glowGrad = ctx.createRadialGradient(fx, fy, 2, fx, fy, GRID_SIZE * 0.9);
        glowGrad.addColorStop(0, fruitInfo.glow);
        glowGrad.addColorStop(1, "transparent");
        ctx.fillStyle = glowGrad;
        ctx.beginPath();
        ctx.arc(fx, fy, GRID_SIZE * 0.85, 0, Math.PI * 2);
        ctx.fill();

        // Fruit Body
        const fruitGrad = ctx.createRadialGradient(fx - 2, fy - 2, 1, fx, fy, GRID_SIZE * 0.42);
        fruitGrad.addColorStop(0, "#ffffff");
        fruitGrad.addColorStop(0.3, fruitInfo.glow);
        fruitGrad.addColorStop(0.85, fruitInfo.color);
        fruitGrad.addColorStop(1, "#1a0b12");

        ctx.fillStyle = fruitGrad;
        ctx.beginPath();
        ctx.arc(fx, fy, GRID_SIZE * 0.4, 0, Math.PI * 2);
        ctx.fill();

        // Leaf
        ctx.fillStyle = fruitInfo.leaf;
        ctx.beginPath();
        ctx.ellipse(fx + 3, fy - GRID_SIZE * 0.4, 4, 2, -Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    function drawSnake() {
        if (snake.length === 0) return;

        ctx.save();

        // Body segments
        for (let i = snake.length - 1; i > 0; i--) {
            const seg = snake[i];
            const prev = snake[i - 1];

            const cx = seg.x * GRID_SIZE + GRID_SIZE / 2;
            const cy = seg.y * GRID_SIZE + GRID_SIZE / 2;

            const progress = i / snake.length;
            const radius = Math.max(GRID_SIZE * 0.34, GRID_SIZE * 0.46 * (1 - progress * 0.35));

            const segGrad = ctx.createRadialGradient(cx - 2, cy - 2, 2, cx, cy, radius);
            segGrad.addColorStop(0, "#6ee7b7");    // Pale emerald highlight
            segGrad.addColorStop(0.35, "#10b981"); // Vibrant jungle green
            segGrad.addColorStop(0.7, "#047857");  // Deep rainforest green
            segGrad.addColorStop(1, "#022c22");    // Shadowed underbelly outline

            ctx.fillStyle = segGrad;
            ctx.beginPath();
            ctx.arc(cx, cy, radius, 0, Math.PI * 2);
            ctx.fill();

            const prevCx = prev.x * GRID_SIZE + GRID_SIZE / 2;
            const prevCy = prev.y * GRID_SIZE + GRID_SIZE / 2;

            ctx.strokeStyle = segGrad;
            ctx.lineWidth = radius * 1.8;
            ctx.lineCap = "round";
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(prevCx, prevCy);
            ctx.stroke();

            // Dorsal scale spine dot
            if (i % 2 === 0) {
                ctx.fillStyle = "rgba(254, 240, 138, 0.35)";
                ctx.beginPath();
                ctx.arc(cx, cy, radius * 0.28, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        // Snake Head
        const head = snake[0];
        const hx = head.x * GRID_SIZE + GRID_SIZE / 2;
        const hy = head.y * GRID_SIZE + GRID_SIZE / 2;
        const angle = Math.atan2(direction.y, direction.x);

        ctx.translate(hx, hy);
        ctx.rotate(angle);

        // Flickering Tongue
        if (tongueTimer % 14 < 7) {
            ctx.save();
            ctx.strokeStyle = "#ef4444";
            ctx.lineWidth = 1.8;
            ctx.beginPath();
            ctx.moveTo(GRID_SIZE * 0.5, 0);
            ctx.lineTo(GRID_SIZE * 0.95, 0);
            ctx.lineTo(GRID_SIZE * 1.15, -4);
            ctx.moveTo(GRID_SIZE * 0.95, 0);
            ctx.lineTo(GRID_SIZE * 1.15, 4);
            ctx.stroke();
            ctx.restore();
        }

        // Head Shape
        const headGrad = ctx.createRadialGradient(2, -1, 2, 0, 0, GRID_SIZE * 0.6);
        headGrad.addColorStop(0, "#86efac");
        headGrad.addColorStop(0.35, "#10b981");
        headGrad.addColorStop(0.8, "#047857");
        headGrad.addColorStop(1, "#022c22");

        ctx.fillStyle = headGrad;
        ctx.beginPath();
        ctx.moveTo(GRID_SIZE * 0.55, 0);
        ctx.quadraticCurveTo(GRID_SIZE * 0.25, GRID_SIZE * 0.48, -GRID_SIZE * 0.35, GRID_SIZE * 0.42);
        ctx.quadraticCurveTo(-GRID_SIZE * 0.48, 0, -GRID_SIZE * 0.35, -GRID_SIZE * 0.42);
        ctx.quadraticCurveTo(GRID_SIZE * 0.25, -GRID_SIZE * 0.48, GRID_SIZE * 0.55, 0);
        ctx.closePath();
        ctx.fill();

        ctx.strokeStyle = "#022c22";
        ctx.lineWidth = 1.2;
        ctx.stroke();

        // Eyes
        const eyeOffset = GRID_SIZE * 0.24;
        const eyeX = GRID_SIZE * 0.12;

        [-eyeOffset, eyeOffset].forEach(eyeY => {
            ctx.fillStyle = "#f59e0b";
            ctx.beginPath();
            ctx.arc(eyeX, eyeY, 3.2, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#000000";
            ctx.beginPath();
            ctx.ellipse(eyeX, eyeY, 0.9, 2.5, 0, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(eyeX + 0.8, eyeY - 0.8, 0.7, 0, Math.PI * 2);
            ctx.fill();
        });

        ctx.restore();
    }

    function drawParticles() {
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.life -= p.decay;

            if (p.life <= 0) {
                particles.splice(i, 1);
                continue;
            }

            ctx.save();
            ctx.globalAlpha = p.life;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }

    function drawFireflies() {
        ctx.save();
        fireflies.forEach(f => {
            f.x += f.vx;
            f.y += f.vy;
            f.alpha += Math.sin(Date.now() * f.pulseSpeed) * 0.02;

            if (f.x < 0) f.x = canvas.width;
            if (f.x > canvas.width) f.x = 0;
            if (f.y < 0) f.y = canvas.height;
            if (f.y > canvas.height) f.y = 0;

            const alpha = Math.max(0.1, Math.min(0.85, f.alpha));
            ctx.fillStyle = `rgba(167, 243, 208, ${alpha})`;
            ctx.beginPath();
            ctx.arc(f.x, f.y, f.radius, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.restore();
    }

    // --- Keyboard Controls ---
    window.addEventListener("keydown", (e) => {
        if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " "].includes(e.key)) {
            e.preventDefault();
        }

        sound.init();

        // Pause toggle
        if (e.key === " " || e.key.toLowerCase() === "p") {
            if (isRunning) togglePause();
            return;
        }

        // Restart (R key when game over or running)
        if (e.key.toLowerCase() === "r") {
            if (!isRunning) {
                startOrRestartGame();
            }
            return;
        }

        // Enter to start from start overlay
        if (e.key === "Enter") {
            if (startOverlay.classList.contains("active")) {
                handleStartButtonClick();
                return;
            }
            if (!nameModalOverlay.classList.contains("hidden")) {
                modalSaveNameBtn.click();
                return;
            }
        }

        // Mute toggle
        if (e.key.toLowerCase() === "m") {
            toggleMute();
            return;
        }

        // Direction mapping (Arrow keys + WASD)
        switch (e.key) {
            case "ArrowUp":
            case "w":
            case "W":
                if (direction.y !== 1) nextDirection = { x: 0, y: -1 };
                break;
            case "ArrowDown":
            case "s":
            case "S":
                if (direction.y !== -1) nextDirection = { x: 0, y: 1 };
                break;
            case "ArrowLeft":
            case "a":
            case "A":
                if (direction.x !== 1) nextDirection = { x: -1, y: 0 };
                break;
            case "ArrowRight":
            case "d":
            case "D":
                if (direction.x !== -1) nextDirection = { x: 1, y: 0 };
                break;
        }
    });

    // --- State Control Actions ---
    function handleStartButtonClick() {
        if (!activeHunter) {
            const entered = hunterNameInput.value.trim();
            setActiveHunter(entered || "Explorer");
        }
        startOrRestartGame();
    }

    function startOrRestartGame() {
        sound.init();
        startOverlay.classList.remove("active");
        startOverlay.classList.add("hidden");
        gameOverOverlay.classList.remove("active");
        gameOverOverlay.classList.add("hidden");
        pauseOverlay.classList.add("hidden");
        nameModalOverlay.classList.add("hidden");

        resetGame();
        isRunning = true;
        isPaused = false;
        clearTimeout(gameLoopTimeout);
        gameLoop();
    }

    function togglePause() {
        if (!isRunning) return;
        isPaused = !isPaused;

        if (isPaused) {
            pauseOverlay.classList.remove("hidden");
            pauseOverlay.classList.add("active");
            clearTimeout(gameLoopTimeout);
        } else {
            pauseOverlay.classList.remove("active");
            pauseOverlay.classList.add("hidden");
            gameLoop();
        }
    }

    function toggleMute() {
        sound.muted = !sound.muted;
        muteIconEl.textContent = sound.muted ? "🔇" : "🔊";
        muteBtnEl.innerHTML = `<span id="mute-icon">${sound.muted ? "🔇" : "🔊"}</span> Sound ${sound.muted ? "OFF" : "ON"}`;
    }

    function openNameModal() {
        nameModalOverlay.classList.remove("hidden");
        nameModalOverlay.classList.add("active");
        modalNameInput.value = "";
        setTimeout(() => modalNameInput.focus(), 200);
    }

    function closeNameModal() {
        nameModalOverlay.classList.remove("active");
        nameModalOverlay.classList.add("hidden");
    }

    // --- Event Listeners ---
    startBtn.addEventListener("click", handleStartButtonClick);

    switchUserBtn.addEventListener("click", () => {
        namePromptSection.classList.remove("hidden");
        returningPlayerSection.classList.add("hidden");
        switchUserBtn.classList.add("hidden");
        hunterNameInput.value = "";
        hunterNameInput.focus();
        startBtn.textContent = "SAVE & START (ENTER)";
    });

    continueUserBtn.addEventListener("click", startOrRestartGame);
    gameOverNewUserBtn.addEventListener("click", openNameModal);
    headerSwitchBtn.addEventListener("click", openNameModal);

    modalSaveNameBtn.addEventListener("click", () => {
        const name = modalNameInput.value.trim();
        if (name) {
            setActiveHunter(name);
        }
        closeNameModal();
        startOrRestartGame();
    });

    modalNameInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            modalSaveNameBtn.click();
        }
    });

    modalCancelBtn.addEventListener("click", closeNameModal);
    resumeBtn.addEventListener("click", togglePause);
    muteBtnEl.addEventListener("click", toggleMute);

    speedSelectEl.addEventListener("change", () => {
        stepInterval = parseInt(speedSelectEl.value, 10) || 135;
    });

    // --- Initial Boot ---
    if (activeHunter) {
        setActiveHunter(activeHunter);
    }
    setupStartOverlayUI();
    renderLeaderboard();
    resetGame();
    draw();

})();
