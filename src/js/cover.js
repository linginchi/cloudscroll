(function() {
  const bg = document.getElementById('cover-bg');
  const cover = document.getElementById('cover-page');
  if (!bg || !cover) return;

  bg.innerHTML = `
    <!-- Layer 1: Far mountains (distant, faint) -->
    <svg class="bg-layer layer-mountains-far" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:20%;left:0;width:100%;height:50%;opacity:0.15;">
      <path d="M-20,400 Q60,180 140,300 Q220,120 300,280 Q380,100 500,320 L500,450 L-20,450 Z"
            fill="#8b7355"/>
    </svg>

    <!-- Layer 2: Mid mountains (Wuyi style peaks) -->
    <svg class="bg-layer layer-mountains-mid" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:20%;left:0;width:100%;height:45%;opacity:0.22;">
      <path d="M-30,380 Q30,160 100,300 Q180,80 250,260 Q320,100 410,280 Q460,140 530,340 L530,500 L-30,500 Z"
            fill="#7a6b52"/>
      <!-- Add a few sharper Wuyi peaks -->
      <path d="M160,270 L180,120 L200,270" fill="#7a6b52" opacity="0.6"/>
      <path d="M340,260 L360,100 L380,260" fill="#7a6b52" opacity="0.5"/>
    </svg>

    <!-- Layer 3: Near shore / stream hint -->
    <svg class="bg-layer layer-stream" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:20%;left:0;width:100%;height:35%;opacity:0.25;">
      <path d="M-20,380 Q120,340 200,370 Q300,400 420,360 Q460,350 500,370"
            stroke="#a09080" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M-20,370 Q120,330 200,360 Q300,390 420,350 Q460,340 500,360"
            stroke="#a09080" stroke-width="1" fill="none" stroke-linecap="round" opacity="0.5"/>
    </svg>

    <!-- Layer 4: Bamboo raft + fisherman silhouette -->
    <svg class="bg-layer layer-raft" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;bottom:22%;left:0;width:100%;height:15%;opacity:0.35;">
      <rect x="220" y="90" width="80" height="6" rx="3" fill="#3d2b1f"/>
      <line x1="285" y1="90" x2="285" y2="30" stroke="#3d2b1f" stroke-width="1.5"/>
      <circle cx="285" cy="20" r="4" fill="#3d2b1f"/>
      <line x1="285" y1="65" x2="265" y2="55" stroke="#3d2b1f" stroke-width="1"/>
      <circle cx="240" cy="55" r="4" fill="#3d2b1f"/>
      <circle cx="255" cy="58" r="4" fill="#3d2b1f"/>
    </svg>

    <!-- Layer 5: Setting sun glow -->
    <svg class="bg-layer layer-sun" viewBox="0 0 480 850" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:5%;right:10%;width:80px;height:80px;opacity:0.4;">
      <defs>
        <radialGradient id="sunGlow">
          <stop offset="0%" stop-color="#d4b896"/>
          <stop offset="100%" stop-color="transparent"/>
        </radialGradient>
      </defs>
      <circle cx="40" cy="40" r="40" fill="url(#sunGlow)"/>
    </svg>

    <!-- Layer 6: Clouds (animated via CSS) -->
    <svg class="bg-layer layer-clouds" viewBox="0 0 480 200" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:12%;left:0;width:100%;height:25%;opacity:0.18;">
      <ellipse class="cloud cloud-1" cx="100" cy="50" rx="60" ry="20" fill="#a09080"/>
      <ellipse class="cloud cloud-2" cx="300" cy="80" rx="50" ry="15" fill="#a09080"/>
      <ellipse class="cloud cloud-3" cx="200" cy="30" rx="40" ry="12" fill="#a09080" opacity="0.6"/>
    </svg>

    <!-- Layer 7: Geese flying north (animated via CSS) -->
    <svg class="bg-layer layer-geese" viewBox="0 0 480 200" preserveAspectRatio="xMidYMid slice"
         style="position:absolute;top:18%;left:0;width:100%;height:20%;opacity:0.25;">
      <g class="geese-group">
        <path d="M60,50 L55,45 M60,50 L65,45" stroke="#3d2b1f" stroke-width="1" fill="none"/>
        <path d="M80,55 L75,50 M80,55 L85,50" stroke="#3d2b1f" stroke-width="1" fill="none"/>
        <path d="M70,60 L65,55 M70,60 L75,55" stroke="#3d2b1f" stroke-width="1" fill="none"/>
        <path d="M90,65 L85,60 M90,65 L95,60" stroke="#3d2b1f" stroke-width="1" fill="none"/>
      </g>
    </svg>
  `;

  bg.setAttribute('aria-hidden', 'true');

  cover.addEventListener('click', function() {
    sessionStorage.setItem('transition', 'cover-to-shelf');
    window.location.href = 'shelf.html';
  });
})();
