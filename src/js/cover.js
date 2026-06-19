(function() {
  const bg = document.getElementById('cover-bg');
  const cover = document.getElementById('cover-page');
  if (!bg || !cover) return;

  // Ink-wash landscape with a warm sun. No raft, no figures.
  // Soft low-saturation palette with a warm orange-yellow sun as the focal warmth.
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

    <!-- Layer 1: Warm sky gradient (soft, with warm horizon) -->
    <svg class="bg-layer layer-sky" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:0;left:0;width:100%;height:62%;opacity:0.7;">
      <defs>
        <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#f5ede0"/>
          <stop offset="45%" stop-color="#f3e2c8"/>
          <stop offset="75%" stop-color="#eed0a8"/>
          <stop offset="100%" stop-color="#eed0a8" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="480" height="510" fill="url(#skyGrad)"/>
    </svg>

    <!-- Layer 2: Warm sun (enhanced — warm, visible, soft orange-yellow) -->
    <svg class="bg-layer layer-sun" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:15%;left:0;width:100%;height:38%;opacity:1;">
      <defs>
        <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#fff2cc" stop-opacity="0.85"/>
          <stop offset="22%" stop-color="#ffd98a" stop-opacity="0.7"/>
          <stop offset="50%" stop-color="#f5b860" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#e8a050" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <g filter="url(#inkWashSoft)">
        <!-- outer warm glow -->
        <circle cx="335" cy="130" r="140" fill="url(#sunGlow)"/>
        <!-- mid glow -->
        <circle cx="335" cy="130" r="60" fill="#ffd98a" opacity="0.4"/>
        <!-- sun core — warm, clearly visible -->
        <circle cx="335" cy="130" r="34" fill="#ffe8a8" opacity="0.85"/>
        <circle cx="335" cy="130" r="22" fill="#fff0c0" opacity="0.9"/>
      </g>
    </svg>

    <!-- Layer 3: Thin warm clouds catching sunlight (breathing) -->
    <svg class="bg-layer layer-clouds" viewBox="0 0 480 250" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:9%;left:0;width:100%;height:28%;opacity:0.5;">
      <g filter="url(#inkWashSoft)" fill="#e8c898">
        <ellipse class="cloud cloud-1" cx="80" cy="60" rx="78" ry="14" opacity="0.4"/>
        <ellipse class="cloud cloud-1" cx="120" cy="55" rx="52" ry="10" opacity="0.35"/>
        <ellipse class="cloud cloud-2" cx="320" cy="92" rx="66" ry="12" opacity="0.38"/>
        <ellipse class="cloud cloud-2" cx="360" cy="86" rx="44" ry="9" opacity="0.32"/>
        <ellipse class="cloud cloud-3" cx="205" cy="42" rx="48" ry="8" opacity="0.3"/>
      </g>
    </svg>

    <!-- Layer 4: Far mountains (pale blue-grey wash, fading into mist) -->
    <svg class="bg-layer layer-mountains-far" viewBox="0 0 480 450" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:24%;left:0;width:100%;height:36%;opacity:0.5;">
      <g filter="url(#inkWashSoft)">
        <path d="M-40,360 Q20,210 80,300 Q140,170 200,280 Q260,150 320,260 Q380,135 440,250 Q500,190 540,320 L540,450 L-40,450 Z"
              fill="#8a9a98" opacity="0.5"/>
      </g>
    </svg>

    <!-- Layer 5: Mid mountains (ink-blue-green, layered strokes for texture) -->
    <svg class="bg-layer layer-mountains-mid" viewBox="0 0 480 450" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:23%;left:0;width:100%;height:40%;opacity:0.75;">
      <g filter="url(#inkWash)">
        <path d="M-50,320 Q10,170 80,280 Q150,110 220,240 Q290,95 360,230 Q410,130 470,270 Q530,190 560,320 L560,450 L-50,450 Z"
              fill="#6a8078" opacity="0.45"/>
        <path d="M-20,300 Q60,180 140,270 Q210,160 280,250 Q350,150 420,260 L420,450 L-20,450 Z"
              fill="#5a7068" opacity="0.32"/>
        <g fill="#9ab098" opacity="0.28">
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

    <!-- Layer 6: Near mountains (deep ink-green-grey, more texture) -->
    <svg class="bg-layer layer-mountains-near" viewBox="0 0 480 450" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:22%;left:0;width:100%;height:38%;opacity:0.8;">
      <g filter="url(#inkWash)">
        <path d="M-30,340 Q40,205 120,300 Q180,185 260,270 Q330,155 400,260 Q460,195 510,310 L510,450 L-30,450 Z"
              fill="#4a5a52" opacity="0.6"/>
        <path d="M0,330 Q70,220 150,300 Q220,200 300,290 L300,450 L0,450 Z"
              fill="#3e4e46" opacity="0.32"/>
        <g fill="#9ab098" opacity="0.32">
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

    <!-- Layer 7: Stream (mostly white with faint warm reflection + ink ripples) -->
    <svg class="bg-layer layer-stream" viewBox="0 0 480 300" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:4%;left:0;width:100%;height:26%;opacity:0.65;">
      <defs>
        <linearGradient id="streamGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#f0c898" stop-opacity="0.25"/>
          <stop offset="50%" stop-color="#d8c0a0" stop-opacity="0.1"/>
          <stop offset="100%" stop-color="#a8b098" stop-opacity="0.14"/>
        </linearGradient>
      </defs>
      <rect x="0" y="30" width="480" height="200" fill="url(#streamGrad)"/>
      <g stroke="#6a5a4a" fill="none" opacity="0.22">
        <path d="M-20,120 Q100,104 200,128 Q300,152 420,120 Q460,112 520,128" stroke-width="0.8"/>
        <path d="M-20,140 Q120,126 240,148 Q320,166 440,140 Q480,134 520,148" stroke-width="0.6"/>
        <path d="M-20,165 Q100,155 220,173 Q320,190 420,165 Q460,158 520,170" stroke-width="0.6"/>
        <path d="M-20,188 Q100,180 200,195 Q300,210 420,188 Q460,182 520,193" stroke-width="0.5"/>
      </g>
    </svg>

    <!-- Layer 8: Warm sunset glow overlay (binds the warmth across the scene) -->
    <svg class="bg-layer layer-sunset-glow" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:0;left:0;width:100%;height:55%;opacity:0.25;">
      <defs>
        <radialGradient id="sunsetGlow" cx="70%" cy="22%" r="65%">
          <stop offset="0%" stop-color="#ffd98a" stop-opacity="0.6"/>
          <stop offset="50%" stop-color="#f5b860" stop-opacity="0.18"/>
          <stop offset="100%" stop-color="transparent" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect x="0" y="0" width="480" height="850" fill="url(#sunsetGlow)"/>
    </svg>

    <!-- Layer 9: Geese flying right (animated wings + left-to-right drift) -->
    <svg class="bg-layer layer-geese" viewBox="0 0 480 200" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:21%;left:0;width:100%;height:16%;opacity:0.5;">
      <g class="geese-group">
        <!-- Goose 1 (front, larger) -->
        <g class="goose goose-1" transform="translate(40,50)">
          <!-- body -->
          <line class="goose-body" x1="0" y1="0" x2="8" y2="0" stroke="#3d2b1f" stroke-width="1.2" stroke-linecap="round"/>
          <!-- left wing -->
          <line class="wing-left" x1="4" y1="0" x2="-4" y2="-6" stroke="#3d2b1f" stroke-width="1.2" stroke-linecap="round"/>
          <!-- right wing -->
          <line class="wing-right" x1="4" y1="0" x2="-4" y2="6" stroke="#3d2b1f" stroke-width="1.2" stroke-linecap="round"/>
        </g>
        <!-- Goose 2 (middle) -->
        <g class="goose goose-2" transform="translate(64,44)">
          <line class="goose-body" x1="0" y1="0" x2="7" y2="0" stroke="#3d2b1f" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-left" x1="3.5" y1="0" x2="-3.5" y2="-5" stroke="#3d2b1f" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-right" x1="3.5" y1="0" x2="-3.5" y2="5" stroke="#3d2b1f" stroke-width="1" stroke-linecap="round"/>
        </g>
        <!-- Goose 3 -->
        <g class="goose goose-3" transform="translate(80,50)">
          <line class="goose-body" x1="0" y1="0" x2="8" y2="0" stroke="#3d2b1f" stroke-width="1.2" stroke-linecap="round"/>
          <line class="wing-left" x1="4" y1="0" x2="-4" y2="-6" stroke="#3d2b1f" stroke-width="1.2" stroke-linecap="round"/>
          <line class="wing-right" x1="4" y1="0" x2="-4" y2="6" stroke="#3d2b1f" stroke-width="1.2" stroke-linecap="round"/>
        </g>
        <!-- Goose 4 (tail) -->
        <g class="goose goose-4" transform="translate(96,56)">
          <line class="goose-body" x1="0" y1="0" x2="7" y2="0" stroke="#3d2b1f" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-left" x1="3.5" y1="0" x2="-3.5" y2="-5" stroke="#3d2b1f" stroke-width="1" stroke-linecap="round"/>
          <line class="wing-right" x1="3.5" y1="0" x2="-3.5" y2="5" stroke="#3d2b1f" stroke-width="1" stroke-linecap="round"/>
        </g>
        <!-- Goose 5 (second V, smaller) -->
        <g class="goose goose-5" transform="translate(130,68)">
          <line class="goose-body" x1="0" y1="0" x2="6" y2="0" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-left" x1="3" y1="0" x2="-3" y2="-4" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-right" x1="3" y1="0" x2="-3" y2="4" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
        </g>
        <!-- Goose 6 -->
        <g class="goose goose-6" transform="translate(142,65)">
          <line class="goose-body" x1="0" y1="0" x2="6" y2="0" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-left" x1="3" y1="0" x2="-3" y2="-4" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-right" x1="3" y1="0" x2="-3" y2="4" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
        </g>
        <!-- Goose 7 -->
        <g class="goose goose-7" transform="translate(152,71)">
          <line class="goose-body" x1="0" y1="0" x2="6" y2="0" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-left" x1="3" y1="0" x2="-3" y2="-4" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
          <line class="wing-right" x1="3" y1="0" x2="-3" y2="4" stroke="#3d2b1f" stroke-width="0.8" stroke-linecap="round"/>
        </g>
      </g>
    </svg>
  `;

  bg.setAttribute('aria-hidden', 'true');

  cover.addEventListener('click', function() {
    sessionStorage.setItem('transition', 'cover-to-shelf');
    window.location.href = 'shelf.html';
  });
})();
