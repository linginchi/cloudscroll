(function() {
  const bg = document.getElementById('cover-bg');
  const cover = document.getElementById('cover-page');
  if (!bg || !cover) return;

  // Ink-wash landscape with a warm sun. No raft, no figures.
  // Refined palette: muted warm tones harmonized with the 淡雅紙本書房 scheme.
  bg.innerHTML = `
    <!-- ===== Shared ink-wash filter defs ===== -->
    <svg width="0" height="0" style="position:absolute;" aria-hidden="true">
      <defs>
        <filter id="inkWash" x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="2" seed="7" result="noise"/>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="3" xChannelSelector="R" yChannelSelector="G"/>
          <feGaussianBlur stdDeviation="0.6"/>
        </filter>
        <filter id="inkWashSoft" x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="3" result="noise"/>
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="2" xChannelSelector="R" yChannelSelector="G"/>
          <feGaussianBlur stdDeviation="1.1"/>
        </filter>
      </defs>
    </svg>

    <!-- Layer 1: Warm sky gradient (muted, softer transition into paper white) -->
    <svg class="bg-layer layer-sky" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:0;left:0;width:100%;height:62%;opacity:0.75;">
      <defs>
        <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#f5ede0"/>
          <stop offset="40%" stop-color="#efe0c8"/>
          <stop offset="70%" stop-color="#e8d4ab"/>
          <stop offset="100%" stop-color="#e8d4ab" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="480" height="510" fill="url(#skyGrad)"/>
    </svg>

    <!-- Layer 2: Subdued warm sun (melting into paper, gentle glow) -->
    <svg class="bg-layer layer-sun" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:15%;left:0;width:100%;height:38%;opacity:0.9;">
      <defs>
        <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#fff6e8" stop-opacity="0.8"/>
          <stop offset="22%" stop-color="#f0d8a0" stop-opacity="0.55"/>
          <stop offset="50%" stop-color="#dfb878" stop-opacity="0.22"/>
          <stop offset="100%" stop-color="#d4a868" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <g filter="url(#inkWashSoft)">
        <circle cx="335" cy="130" r="140" fill="url(#sunGlow)"/>
        <circle cx="335" cy="130" r="60" fill="#f0d8a0" opacity="0.3"/>
        <circle cx="335" cy="130" r="34" fill="#fbecc8" opacity="0.8"/>
        <circle cx="335" cy="130" r="20" fill="#fdf4e0" opacity="0.85"/>
      </g>
    </svg>

    <!-- Layer 3: Thin warm clouds drifting (breathing) -->
    <svg class="bg-layer layer-clouds" viewBox="0 0 480 250" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:9%;left:0;width:100%;height:28%;opacity:0.45;">
      <g filter="url(#inkWashSoft)" fill="#ddc8a0">
        <ellipse class="cloud cloud-1" cx="80" cy="60" rx="78" ry="14" opacity="0.35"/>
        <ellipse class="cloud cloud-1" cx="120" cy="55" rx="52" ry="10" opacity="0.3"/>
        <ellipse class="cloud cloud-2" cx="320" cy="92" rx="66" ry="12" opacity="0.32"/>
        <ellipse class="cloud cloud-2" cx="360" cy="86" rx="44" ry="9" opacity="0.28"/>
        <ellipse class="cloud cloud-3" cx="205" cy="42" rx="48" ry="8" opacity="0.26"/>
      </g>
    </svg>

    <!-- Layer 4: Far mountains (misty blue-grey wash, fading into distance) -->
    <svg class="bg-layer layer-mountains-far" viewBox="0 0 480 450" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:24%;left:0;width:100%;height:36%;opacity:0.48;">
      <g filter="url(#inkWashSoft)">
        <path d="M-40,360 Q20,210 80,300 Q140,170 200,280 Q260,150 320,260 Q380,135 440,250 Q500,190 540,320 L540,450 L-40,450 Z"
              fill="#889894" opacity="0.48"/>
      </g>
    </svg>

    <!-- Layer 5: Mid mountains (ink-green-blue, layered strokes suggesting brush texture) -->
    <svg class="bg-layer layer-mountains-mid" viewBox="0 0 480 450" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:23%;left:0;width:100%;height:40%;opacity:0.7;">
      <g filter="url(#inkWash)">
        <path d="M-50,320 Q10,170 80,280 Q150,110 220,240 Q290,95 360,230 Q410,130 470,270 Q530,190 560,320 L560,450 L-50,450 Z"
              fill="#5e7568" opacity="0.4"/>
        <path d="M-20,300 Q60,180 140,270 Q210,160 280,250 Q350,150 420,260 L420,450 L-20,450 Z"
              fill="#4d6258" opacity="0.28"/>
        <g fill="#8a9c88" opacity="0.26">
          <circle cx="150" cy="160" r="4"/>
          <circle cx="158" cy="155" r="3"/>
          <circle cx="166" cy="162" r="3.5"/>
          <circle cx="290" cy="150" r="4"/>
          <circle cx="298" cy="145" r="3"/>
          <circle cx="306" cy="152" r="3"/>
          <circle cx="410" cy="175" r="3.5"/>
          <circle cx="418" cy="170" r="3"/>
          <circle cx="80" cy="215" r="4"/>
          <circle cx="88" cy="210" r="3"/>
          <circle cx="370" cy="170" r="3"/>
        </g>
      </g>
    </svg>

    <!-- Layer 6: Near mountains (deeper ink tones, more texture and presence) -->
    <svg class="bg-layer layer-mountains-near" viewBox="0 0 480 450" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:22%;left:0;width:100%;height:38%;opacity:0.75;">
      <g filter="url(#inkWash)">
        <path d="M-30,340 Q40,205 120,300 Q180,185 260,270 Q330,155 400,260 Q460,195 510,310 L510,450 L-30,450 Z"
              fill="#3d4e44" opacity="0.55"/>
        <path d="M0,330 Q70,220 150,300 Q220,200 300,290 L300,450 L0,450 Z"
              fill="#334238" opacity="0.3"/>
        <g fill="#8a9c88" opacity="0.28">
          <circle cx="180" cy="230" r="3.5"/>
          <circle cx="188" cy="225" r="3"/>
          <circle cx="196" cy="232" r="3"/>
          <circle cx="330" cy="205" r="3.5"/>
          <circle cx="338" cy="200" r="3"/>
          <circle cx="346" cy="207" r="3"/>
          <circle cx="200" cy="240" r="3"/>
          <circle cx="350" cy="215" r="3"/>
        </g>
      </g>
    </svg>

    <!-- Layer 7: Stream (soft ink reflections beneath the scene) -->
    <svg class="bg-layer layer-stream" viewBox="0 0 480 300" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:4%;left:0;width:100%;height:26%;opacity:0.55;">
      <defs>
        <linearGradient id="streamGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#e8d0a0" stop-opacity="0.2"/>
          <stop offset="50%" stop-color="#d0b890" stop-opacity="0.08"/>
          <stop offset="100%" stop-color="#9aa894" stop-opacity="0.12"/>
        </linearGradient>
      </defs>
      <rect x="0" y="30" width="480" height="200" fill="url(#streamGrad)"/>
      <g stroke="#5a4e40" fill="none" opacity="0.18">
        <path d="M-20,120 Q100,104 200,128 Q300,152 420,120 Q460,112 520,128" stroke-width="0.8"/>
        <path d="M-20,140 Q120,126 240,148 Q320,166 440,140 Q480,134 520,148" stroke-width="0.6"/>
        <path d="M-20,165 Q100,155 220,173 Q320,190 420,165 Q460,158 520,170" stroke-width="0.6"/>
        <path d="M-20,188 Q100,180 200,195 Q300,210 420,188 Q460,182 520,193" stroke-width="0.5"/>
      </g>
    </svg>

    <!-- Layer 8: Gentle warmth overlay (unifies the scene with paper-toned glow) -->
    <svg class="bg-layer layer-sunset-glow" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:0;left:0;width:100%;height:55%;opacity:0.2;">
      <defs>
        <radialGradient id="sunsetGlow" cx="70%" cy="22%" r="65%">
          <stop offset="0%" stop-color="#f0d8a0" stop-opacity="0.45"/>
          <stop offset="50%" stop-color="#dfb878" stop-opacity="0.12"/>
          <stop offset="100%" stop-color="transparent" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect x="0" y="0" width="480" height="850" fill="url(#sunsetGlow)"/>
    </svg>

    <!-- Layer 9: Geese in V formation (ink-dark, flying across the paper sky) -->
    <svg class="bg-layer layer-geese" viewBox="0 0 480 200" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:21%;left:0;width:100%;height:16%;opacity:0.45;">
      <g class="geese-group">
        <!-- Goose 1 (front, larger) -->
        <g class="goose goose-1" transform="translate(40,50)">
          <line class="goose-body" x1="0" y1="0" x2="8" y2="0" stroke="#2c2416" stroke-width="1.2" stroke-linecap="round"/>
          <line class="wing-left" x1="4" y1="0" x2="-4" y2="-6" stroke="#2c2416" stroke-width="1.2" stroke-linecap="round"/>
          <line class="wing-right" x1="4" y1="0" x2="-4" y2="6" stroke="#2c2416" stroke-width="1.2" stroke-linecap="round"/>
        </g>
        <!-- Goose 2 (middle) -->
        <g class="goose goose-2" transform="translate(64,44)">
          <line class="goose-body" x1="0" y1="0" x2="7" y2="0" stroke="#2c2416" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-left" x1="3.5" y1="0" x2="-3.5" y2="-5" stroke="#2c2416" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-right" x1="3.5" y1="0" x2="-3.5" y2="5" stroke="#2c2416" stroke-width="1" stroke-linecap="round"/>
        </g>
        <!-- Goose 3 -->
        <g class="goose goose-3" transform="translate(80,50)">
          <line class="goose-body" x1="0" y1="0" x2="8" y2="0" stroke="#2c2416" stroke-width="1.2" stroke-linecap="round"/>
          <line class="wing-left" x1="4" y1="0" x2="-4" y2="-6" stroke="#2c2416" stroke-width="1.2" stroke-linecap="round"/>
          <line class="wing-right" x1="4" y1="0" x2="-4" y2="6" stroke="#2c2416" stroke-width="1.2" stroke-linecap="round"/>
        </g>
        <!-- Goose 4 (tail) -->
        <g class="goose goose-4" transform="translate(96,56)">
          <line class="goose-body" x1="0" y1="0" x2="7" y2="0" stroke="#2c2416" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-left" x1="3.5" y1="0" x2="-3.5" y2="-5" stroke="#2c2416" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-right" x1="3.5" y1="0" x2="-3.5" y2="5" stroke="#2c2416" stroke-width="1" stroke-linecap="round"/>
        </g>
        <!-- Goose 5 (second V, smaller) -->
        <g class="goose goose-5" transform="translate(130,68)">
          <line class="goose-body" x1="0" y1="0" x2="6" y2="0" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-left" x1="3" y1="0" x2="-3" y2="-4" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-right" x1="3" y1="0" x2="-3" y2="4" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
        </g>
        <!-- Goose 6 -->
        <g class="goose goose-6" transform="translate(142,65)">
          <line class="goose-body" x1="0" y1="0" x2="6" y2="0" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-left" x1="3" y1="0" x2="-3" y2="-4" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-right" x1="3" y1="0" x2="-3" y2="4" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
        </g>
        <!-- Goose 7 -->
        <g class="goose goose-7" transform="translate(152,71)">
          <line class="goose-body" x1="0" y1="0" x2="6" y2="0" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-left" x1="3" y1="0" x2="-3" y2="-4" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-right" x1="3" y1="0" x2="-3" y2="4" stroke="#3a3028" stroke-width="0.8" stroke-linecap="round"/>
        </g>
      </g>
    </svg>
  `;

  bg.setAttribute('aria-hidden', 'true');

  var enterBtn = document.getElementById('cover-enter-btn');
  if (enterBtn) {
    enterBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      sessionStorage.setItem('transition', 'cover-to-shelf');
      window.location.href = 'shelf.html';
    });
  }
})();
