/**
 * Global Marketing Short-form AI Agent
 * Reactive State Management System
 */

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. State Definition (중앙 집중식 상태 관리) ---
    const initialState = {
        globalTarget: {
            name: 'United States',
            flag: 'https://flagcdn.com/us.svg',
            index: 0
        },
        seo: {
            title: 'Future of AI Marketing 2026',
            tone: 'Viral',
            keywords: [
                { text: "AI Marketing Automation", confidence: "high", val: 92 },
                { text: "Future of AI", confidence: "mid", val: 72 },
                { text: "Real-Time Analytics", confidence: "high", val: 85 },
                { text: "Global SaaS Trends", confidence: "mid", val: 78 },
                { text: "AI for Business", confidence: "low", val: 41 }
            ]
        },
        timeline: {
            progress: 45, // percentage
            currentTime: '00:43'
        }
    };

    const countries = [
        { name: 'United States', flag: 'https://flagcdn.com/us.svg' },
        { name: 'Korea', flag: 'https://flagcdn.com/kr.svg' },
        { name: 'Japan', flag: 'https://flagcdn.com/jp.svg' },
        { name: 'Germany', flag: 'https://flagcdn.com/de.svg' }
    ];

    // --- 2. Reactive Handler (Proxy를 통한 자동 업데이트) ---
    const handler = {
        set(target, property, value) {
            target[property] = value;
            // 상태가 변경될 때마다 UI 업데이트 함수 호출
            renderUI(property, value);
            return true;
        }
    };

    // Nested Proxy for deep observation
    const state = new Proxy({
        ...initialState,
        globalTarget: new Proxy(initialState.globalTarget, handler),
        seo: new Proxy(initialState.seo, handler),
        timeline: new Proxy(initialState.timeline, handler)
    }, handler);


    // --- 3. UI Renderers (컴포넌트별 렌더링 로직) ---
    function renderUI(property, value) {
        console.log(`[State Update] ${property} has changed.`);

        if (property === 'globalTarget') {
            const countryToggle = document.getElementById('countryToggle');
            countryToggle.querySelector('.country-name').textContent = value.name;
            countryToggle.querySelector('img').src = value.flag;

            // 국가 변경 시 키워드 자동 업데이트 (Mock logic)
            updateKeywordsByCountry(value.name);
        }

        if (property === 'seo') {
            const seoTitleInput = document.getElementById('seoTitle');
            seoTitleInput.value = value.title;

            // Validate Title Length
            updateTitleValidation(value.title);

            // Update Tone Buttons
            const toneButtons = document.querySelectorAll('.tone-btn');
            toneButtons.forEach(btn => {
                btn.classList.toggle('active', btn.textContent === value.tone);
            });
        }

        if (property === 'timeline') {
            const timelinePlayhead = document.querySelector('.timeline-playhead-line');
            const videoProgress = document.querySelector('.current-progress');
            const videoPlayhead = document.querySelector('.playhead');

            const percent = value.progress;
            timelinePlayhead.style.left = `${percent}%`;
            timelinePlayhead.querySelector('.playhead-time').textContent = value.currentTime;

            videoProgress.style.width = `${percent}%`;
            videoPlayhead.style.left = `${percent}%`;
        }
    }

    // --- 4. Logic Functions (핵심 비즈니스 로직) ---

    function updateTitleValidation(title) {
        const len = title.length;
        const ytCountFill = document.querySelector('.indicator.youtube .fill');
        const ytCountText = document.querySelector('.indicator.youtube .count');

        const ytPercent = Math.min((len / 100) * 100, 100);
        ytCountFill.style.width = `${ytPercent}%`;
        ytCountText.textContent = `${len} / 100`;

        const isWarning = len > 60;
        ytCountFill.style.backgroundColor = isWarning ? 'var(--danger)' : 'var(--primary)';
        ytCountText.style.color = isWarning ? 'var(--danger)' : 'var(--text-muted)';
    }

    function updateKeywordsByCountry(country) {
        const keywordItems = document.querySelectorAll('.keyword-item');
        const baseTexts = ["AI Marketing", "Next Gen", "Hyper Automation", "SaaS Growth", "Business Intelligence"];

        keywordItems.forEach((item, index) => {
            item.style.opacity = '0';
            setTimeout(() => {
                item.querySelector('.text').textContent = `${baseTexts[index]} [${country}]`;
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, index * 80);
        });
    }

    function formatPercentToTime(percent) {
        const totalSeconds = 92; // 01:32
        const currentSeconds = Math.floor((percent / 100) * totalSeconds);
        const mins = Math.floor(currentSeconds / 60);
        const secs = currentSeconds % 60;
        return `0${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }


    // --- 5. Event Listeners (User Interaction -> State Update) ---

    // Country Toggle
    const countryToggleBtn = document.getElementById('countryToggle');
    countryToggleBtn.addEventListener('click', () => {
        const nextIdx = (state.globalTarget.index + 1) % countries.length;
        const nextCountry = countries[nextIdx];

        // Update State -> Triggers UI Render
        state.globalTarget = {
            ...nextCountry,
            index: nextIdx
        };

        // Visual feedback
        countryToggleBtn.style.transform = 'scale(0.95)';
        setTimeout(() => countryToggleBtn.style.transform = 'scale(1)', 150);
    });

    // SEO Title Input
    const seoTitleInput = document.getElementById('seoTitle');
    seoTitleInput.addEventListener('input', (e) => {
        // Update State -> Triggers UI Validation & Sync
        state.seo = {
            ...state.seo,
            title: e.target.value
        };
    });

    // Tone Buttons
    const toneButtons = document.querySelectorAll('.tone-btn');
    toneButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update State -> Triggers UI rendering for 'active' class
            state.seo = {
                ...state.seo,
                tone: btn.textContent
            };

            btn.style.animation = 'none';
            btn.offsetHeight;
            btn.style.animation = 'pulse 0.4s ease';
        });
    });

    // Timeline Interaction
    const trackCanvas = document.querySelector('.track-canvas');
    trackCanvas.addEventListener('mousemove', (e) => {
        const rect = trackCanvas.getBoundingClientRect();
        let x = e.clientX - rect.left;
        x = Math.max(0, Math.min(x, rect.width));

        const percent = (x / rect.width) * 100;

        // Update State -> Triggers Timeline/Video Sync
        state.timeline = {
            progress: percent,
            currentTime: formatPercentToTime(percent)
        };
    });

    // --- 6. Initialization ---
    // Initial Render
    renderUI('globalTarget', state.globalTarget);
    renderUI('seo', state.seo);
    renderUI('timeline', state.timeline);


    // CSS Keyframes injection
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .keyword-item {
            transition: opacity 0.3s ease, transform 0.3s ease;
            transform: translateY(10px);
        }
    `;
    document.head.appendChild(style);

    console.log('Reactive AI Video SEO Agent initialized with State Management.');

    // Global access for testing/debugging
    window.appState = state;
});
