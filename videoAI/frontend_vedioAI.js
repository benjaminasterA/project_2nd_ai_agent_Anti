/**
 * Global Marketing Short-form AI Agent
 * Reactive State Management System with Backend Integration
 * Filename: frontend_vedioAI.js
 * Version: v1.2.0 | Snapshot: SNAPSHOTS.md#v120
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initial State
    const initialState = {
        globalTarget: 'United States',
        countries: ['United States', 'Korea', 'Japan', 'Germany'],
        seoTitle: 'Future of AI Marketing 2026',
        tone: 'Viral',
        keywords: [],
        analytics: {
            views: '125,840',
            engagement: 89,
            seoScore: 92,
            emotionPeak: '00:43'
        },
        currentTime: 43,
        duration: 92
    };

    // 2. Reactive Handler
    const handler = {
        set(target, property, value) {
            target[property] = value;
            renderUI(property, value);
            return true;
        }
    };

    const state = new Proxy(initialState, handler);
    window.appState = state; // For debugging

    // 3. UI Rendering Engine
    function renderUI(property, value) {
        switch (property) {
            case 'globalTarget':
                const dropdown = document.querySelector('#countryToggle');
                const flagMap = {
                    'United States': 'us',
                    'Korea': 'kr',
                    'Japan': 'jp',
                    'Germany': 'de'
                };
                dropdown.querySelector('img').src = `https://flagcdn.com/${flagMap[value]}.svg`;
                dropdown.querySelector('span').textContent = value;
                fetchKeywords(value);
                break;

            case 'seoTitle':
                const input = document.getElementById('seoTitle');
                if (input.value !== value) input.value = value;
                updateCharCount(value.length);
                break;

            case 'tone':
                document.querySelectorAll('.tone-picker button').forEach(btn => {
                    btn.classList.toggle('active', btn.textContent === value);
                });
                break;

            case 'keywords':
                renderKeywords(value);
                break;

            case 'analytics':
                document.getElementById('statViews').textContent = value.views;
                document.getElementById('statEmotionPeak').textContent = value.emotionPeak;

                const engRing = document.getElementById('statEngRing');
                engRing.style.setProperty('--p', value.engagement);
                engRing.querySelector('span').textContent = `${value.engagement}%`;

                const seoRing = document.getElementById('statSeoRing');
                seoRing.style.setProperty('--p', value.seoScore);
                seoRing.querySelector('span').innerHTML = `${value.seoScore}<small>/100</small>`;
                break;
        }
    }

    // 4. Component Renderers
    function renderKeywords(keywords) {
        const container = document.getElementById('keywordListContainer');
        container.innerHTML = keywords.map(kw => `
            <div class="kw-item">
                <i class="ph-fill ph-circle" style="color: ${getConfidenceColor(kw.confidence)}"></i>
                <span class="text">${kw.text}</span>
                <span class="score" style="color: ${getConfidenceColor(kw.confidence)}">${kw.val}%</span>
                <i class="ph-bold ${kw.val > 80 ? 'ph-check-circle' : 'ph-warning'}" style="color: ${getConfidenceColor(kw.confidence)}"></i>
            </div>
        `).join('');
    }

    function getConfidenceColor(level) {
        if (level === 'high') return '#22c55e';
        if (level === 'mid') return '#fbbf24';
        return '#ef4444';
    }

    function updateCharCount(len) {
        const countSpan = document.querySelector('.seo-field .count');
        const fill = document.querySelector('.seo-field .fill');
        countSpan.textContent = `${len} / 100`;
        fill.style.width = `${len}%`;
        fill.style.backgroundColor = len > 60 ? '#ef4444' : '#3b82f6';
    }

    function updateAnalytics(data) {
        document.getElementById('statViews').textContent = data.views;
        document.getElementById('statEmotionPeak').textContent = data.emotionPeak;

        // Circular Rings
        const engRing = document.getElementById('statEngRing');
        engRing.style.setProperty('--p', data.engagement);
        engRing.innerHTML = `<span>${data.engagement}%</span>`;

        const seoRing = document.getElementById('statSeoRing');
        seoRing.style.setProperty('--p', data.seoScore);
        seoRing.innerHTML = `<span>${data.seoScore}<small>/100</small></span>`;
    }

    // 5. Backend Logic
    async function fetchKeywords(country) {
        try {
            const res = await fetch(`/api/keywords?country=${country}`);
            const data = await res.json();
            state.keywords = data.keywords;
        } catch (e) { console.error("Keyword Fetch Failed", e); }
    }

    // 6. Event Listeners
    document.querySelector('.btn-generate').addEventListener('click', async () => {
        const btn = document.querySelector('.btn-generate');
        const originalContent = btn.innerHTML;

        // UI Feedback: Loading
        btn.disabled = true;
        btn.innerHTML = `<i class="ph ph-circle-notch ph-spin"></i> Analyzing...`;

        try {
            const res = await fetch('/api/ai/generate-seo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: state.seoTitle,
                    country: state.globalTarget,
                    tone: state.tone
                })
            });
            const data = await res.json();

            if (data.status === 'success') {
                // Update Multi-State
                state.keywords = data.keywords;
                state.analytics = data.analytics;

                // Visual Pulse Effect
                document.querySelector('.seo-sidebar').style.animation = 'none';
                void document.querySelector('.seo-sidebar').offsetWidth;
                document.querySelector('.seo-sidebar').style.animation = 'pulse-bg 0.5s ease';
            }
        } catch (e) {
            console.error("AI Generation Failed", e);
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalContent;
        }
    });

    document.getElementById('countryToggle').addEventListener('click', () => {
        const currentIndex = state.countries.indexOf(state.globalTarget);
        const nextIndex = (currentIndex + 1) % state.countries.length;
        state.globalTarget = state.countries[nextIndex];
    });

    document.getElementById('seoTitle').addEventListener('input', (e) => {
        state.seoTitle = e.target.value;
        // Immediate visual feedback for character count
        updateCharCount(e.target.value.length);
    });

    // Manual Keyword Addition
    const kwInput = document.getElementById('manualKeywordInput');
    const kwAddBtn = document.getElementById('btnAddKeyword');

    kwAddBtn.addEventListener('click', () => {
        const val = kwInput.value.trim();
        if (val) {
            // Add to reactive state
            state.keywords = [
                { text: val, val: Math.floor(Math.random() * 30) + 70, confidence: 'high' },
                ...state.keywords
            ];
            kwInput.value = '';
            // Pulse effect to show addition
            document.getElementById('keywordListContainer').parentElement.classList.add('pulse');
            setTimeout(() => document.getElementById('keywordListContainer').parentElement.classList.remove('pulse'), 1000);
        }
    });

    kwInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') kwAddBtn.click();
    });

    document.querySelectorAll('.tone-picker button').forEach(btn => {
        btn.addEventListener('click', () => {
            state.tone = btn.textContent;
            // Add pulse effect simulation
            btn.parentElement.classList.add('pulse');
            setTimeout(() => btn.parentElement.classList.remove('pulse'), 1000);
        });
    });

    // 8. Sidebar & Video Upload Implementation
    const navItems = document.querySelectorAll('.nav-item');
    const navUpload = document.getElementById('navVideoUpload');
    const fileInput = document.getElementById('videoFileInput');

    // Sidebar Active State Switching & Section Navigation
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            if (item.id !== 'navVideoUpload') {
                e.preventDefault();
                navItems.forEach(i => i.classList.remove('active'));
                item.classList.add('active');

                // Mapping Sidebar to Sections
                const text = item.textContent.trim();
                if (text === 'Analytics') {
                    document.querySelector('.bottom-stats').scrollIntoView({ behavior: 'smooth' });
                    document.querySelector('.bottom-stats').classList.add('pulse');
                    setTimeout(() => document.querySelector('.bottom-stats').classList.remove('pulse'), 1000);
                } else if (text === 'Timeline') {
                    document.querySelector('.timeline-box').scrollIntoView({ behavior: 'smooth' });
                    document.querySelector('.timeline-box').classList.add('pulse');
                    setTimeout(() => document.querySelector('.timeline-box').classList.remove('pulse'), 1000);
                } else if (text === 'SEO Keywords') {
                    document.querySelector('.seo-sidebar').scrollIntoView({ behavior: 'smooth' });
                    document.querySelector('.seo-sidebar').classList.add('pulse');
                    setTimeout(() => document.querySelector('.seo-sidebar').classList.remove('pulse'), 1000);
                } else if (text === 'Dashboard') {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            }
        });
    });

    navUpload.addEventListener('click', (e) => {
        e.preventDefault();
        fileInput.click();
    });

    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // UI Feedback: Start Upload
        const btnGenerate = document.querySelector('.btn-generate');
        const originalBtnContent = btnGenerate.innerHTML;
        btnGenerate.disabled = true;
        btnGenerate.innerHTML = `<i class="ph ph-cloud-arrow-up ph-spin"></i> Uploading...`;

        const formData = new FormData();
        formData.append('video', file);

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            if (data.status === 'success') {
                // Update Video Player Source
                const videoEl = document.getElementById('mainVideo');
                videoEl.src = `/uploads/${data.filename}`;
                videoEl.load();
                videoEl.play();

                alert(`업로드 및 분석 준비 완료: ${data.message}`);

                // Simulate automatic AI analysis after upload
                btnGenerate.innerHTML = `<i class="ph ph-circle-notch ph-spin"></i> Analyzing Video...`;
                setTimeout(() => {
                    document.querySelector('.btn-generate').click(); // Trigger SEO generation
                }, 1500);
            }
            else {
                alert(`실패: ${data.message}`);
            }
        } catch (err) {
            console.error("Upload Error", err);
            alert("업로드 중 오류가 발생했습니다.");
        } finally {
            btnGenerate.innerHTML = originalBtnContent;
            btnGenerate.disabled = false;
        }
    });

    // 9. Initialization
    renderUI('globalTarget', state.globalTarget);
    renderUI('analytics', state.analytics);
    renderUI('tone', state.tone);
    renderUI('seoTitle', state.seoTitle);
});
