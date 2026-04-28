/*
 * scene.js — Tron Ares 3D world for evolvingagentslabs.github.io
 *
 * A WebGL scene built with Three.js. Four kinetic monoliths float
 * over a neon-grid floor, each emitting its project's signature
 * color. Particles flow between them like data on a bus. The camera
 * slowly orbits while accepting subtle mouse parallax — a lift from
 * ART+COM's Chronos XXI: contemplative motion, reflective surfaces,
 * abstract digital matter that feels physical.
 *
 * No build step. Pure ES modules from a CDN, loaded via importmap
 * declared in index.html.
 *
 * Hover/focus a project card in the HTML overlay (`data-project="..."`)
 * to fire the scene's `focusMonolith()` — the matching monolith brightens
 * and gently pulses while the others dim. The same handler is wired to
 * pointer events on the canvas itself for direct click-through to the
 * project's GitHub repo.
 */

import * as THREE from "three";
import { EffectComposer }     from "three/addons/postprocessing/EffectComposer.js";
import { RenderPass }         from "three/addons/postprocessing/RenderPass.js";
import { UnrealBloomPass }    from "three/addons/postprocessing/UnrealBloomPass.js";
import { OutputPass }         from "three/addons/postprocessing/OutputPass.js";
import { ShaderPass }         from "three/addons/postprocessing/ShaderPass.js";

// ─── Cheap-device guard ─────────────────────────────────────────────
// Skip the WebGL scene on phones without enough GPU. Static fallback
// shows the bg2 layer (CSS gradient + scanlines) which is already in
// styles.css.
const supportsWebGL = (() => {
  try {
    const c = document.createElement("canvas");
    return !!(c.getContext("webgl2") || c.getContext("webgl"));
  } catch { return false; }
})();
const isLowPerf = matchMedia("(max-width: 720px)").matches
               || matchMedia("(prefers-reduced-motion: reduce)").matches
               || !supportsWebGL;

if (isLowPerf) {
  document.documentElement.classList.add("scene-fallback");
} else {
  start();
}

// ────────────────────────────────────────────────────────────────────
function start() {
  const canvas = document.getElementById("bg");
  if (!canvas) return;

  // Renderer ─────────────────────────────────────────────────────────
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  // Scene + fog ──────────────────────────────────────────────────────
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x000000, 0.024);

  // Camera ───────────────────────────────────────────────────────────
  const camera = new THREE.PerspectiveCamera(
    52, window.innerWidth / window.innerHeight, 0.1, 200,
  );
  camera.position.set(0, 7, 26);
  camera.lookAt(0, 3, 0);

  // Floor grid (Tron) ───────────────────────────────────────────────
  // Two grids stacked: a wide subtle one for distance, a tighter
  // bright one for foreground. Both use Ares orange.
  const gridFar = new THREE.GridHelper(160, 80, 0xff2d00, 0xff2d00);
  gridFar.material.transparent = true;
  gridFar.material.opacity = 0.18;
  gridFar.material.depthWrite = false;
  gridFar.position.y = -0.01;
  scene.add(gridFar);

  const gridNear = new THREE.GridHelper(60, 30, 0xff6b1a, 0xff6b1a);
  gridNear.material.transparent = true;
  gridNear.material.opacity = 0.45;
  gridNear.material.depthWrite = false;
  scene.add(gridNear);

  // Subtle reflective floor (mirror-like dark plane to blend with the grid)
  const floorGeom = new THREE.PlaneGeometry(160, 160);
  const floorMat  = new THREE.MeshStandardMaterial({
    color: 0x000000,
    metalness: 0.92,
    roughness: 0.55,
    transparent: true,
    opacity: 0.6,
  });
  const floor = new THREE.Mesh(floorGeom, floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -0.02;
  scene.add(floor);

  // Lighting ────────────────────────────────────────────────────────
  scene.add(new THREE.AmbientLight(0x331100, 0.5));

  const keyLight = new THREE.DirectionalLight(0xff6b1a, 1.4);
  keyLight.position.set(8, 14, 6);
  scene.add(keyLight);

  const cyanRim  = new THREE.DirectionalLight(0x00d4ff, 0.5);
  cyanRim.position.set(-10, 6, -10);
  scene.add(cyanRim);

  // ─── Monoliths ─────────────────────────────────────────────────
  // Four kinetic forms in a row. Each has a signature color and a
  // distinct silhouette mapped to the project's physical metaphor:
  //   skillos       → tall flat slab        (laptop / book)
  //   skillos_mini  → tall thin rounded box (smartphone)
  //   RoClaw        → literal cube           (the cube robot)
  //   llm_os        → wide low slab          (CPU die)
  const COLORS = {
    ARES_RED:   new THREE.Color(0xff2d00),
    ARES_GLOW:  new THREE.Color(0xff6b1a),
    ARES_PALE:  new THREE.Color(0xffd9c2),
    MCP_GREEN:  new THREE.Color(0x00ff7f),
    MCP_GLOW:   new THREE.Color(0x4ade80),
    WHITE:      new THREE.Color(0xffffff),
    PALE:       new THREE.Color(0xe4e4e7),
    CYAN:       new THREE.Color(0x00d4ff),
  };

  const SPACING = 7.5;
  const PROJECTS = [
    {
      slug: "skillos",
      url:  "https://github.com/EvolvingAgentsLabs/skillos",
      color: COLORS.ARES_RED,
      glow:  COLORS.ARES_GLOW,
      build: () => makeSlab(2.4, 4.2, 0.45),  // laptop-shaped slab
      x: -1.5 * SPACING,
    },
    {
      slug: "skillos_mini",
      url:  "https://github.com/EvolvingAgentsLabs/skillos_mini",
      color: COLORS.ARES_GLOW,
      glow:  COLORS.ARES_PALE,
      build: () => makePhone(1.2, 2.6, 0.25),
      x: -0.5 * SPACING,
    },
    {
      slug: "roclaw",
      url:  "https://github.com/EvolvingAgentsLabs/skillos_robot",
      color: COLORS.MCP_GREEN,
      glow:  COLORS.MCP_GLOW,
      build: () => makeCube(2.2),
      x:  0.5 * SPACING,
    },
    {
      slug: "llm_os",
      url:  "https://github.com/EvolvingAgentsLabs/llm_os",
      color: COLORS.WHITE,
      glow:  COLORS.PALE,
      build: () => makeCpu(2.6, 0.6, 2.6),
      x:  1.5 * SPACING,
    },
  ];

  const monoliths = [];
  for (const p of PROJECTS) {
    const group = new THREE.Group();
    group.position.set(p.x, 2, 0);
    group.userData = p;

    const body = p.build();
    const mat = new THREE.MeshStandardMaterial({
      color:     p.color,
      emissive:  p.color,
      emissiveIntensity: 1.15,
      metalness: 0.55,
      roughness: 0.32,
    });
    const mesh = new THREE.Mesh(body, mat);
    group.add(mesh);

    // Wireframe overlay — subtle Tron grid on the surface
    const wire = new THREE.LineSegments(
      new THREE.WireframeGeometry(body),
      new THREE.LineBasicMaterial({
        color: p.glow,
        transparent: true,
        opacity: 0.45,
      }),
    );
    group.add(wire);

    // Pedestal — disc beneath the monolith
    const pedGeom = new THREE.CylinderGeometry(1.2, 1.5, 0.15, 32);
    const pedMat  = new THREE.MeshStandardMaterial({
      color: 0x000000,
      emissive: p.color,
      emissiveIntensity: 0.6,
      metalness: 0.8,
      roughness: 0.2,
    });
    const pedestal = new THREE.Mesh(pedGeom, pedMat);
    pedestal.position.y = -1.95;
    group.add(pedestal);

    // Glow ring beneath the pedestal
    const ringGeom = new THREE.RingGeometry(1.4, 1.55, 48);
    const ringMat  = new THREE.MeshBasicMaterial({
      color: p.glow,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.65,
    });
    const ring = new THREE.Mesh(ringGeom, ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = -1.96;
    group.add(ring);

    // Up-beam — thin column of light
    const beamGeom = new THREE.CylinderGeometry(0.04, 0.04, 80, 12);
    const beamMat  = new THREE.MeshBasicMaterial({
      color: p.glow,
      transparent: true,
      opacity: 0.45,
      depthWrite: false,
    });
    const beam = new THREE.Mesh(beamGeom, beamMat);
    beam.position.y = 38;
    group.add(beam);

    // Point light on the monolith for self-illumination
    const pl = new THREE.PointLight(p.color, 1.6, 12, 1.6);
    pl.position.y = 0.5;
    group.add(pl);

    scene.add(group);
    monoliths.push({ group, mesh, wire, pedestal, ring, beam, light: pl, project: p });
  }

  // ─── Particle bus ──────────────────────────────────────────────
  // Particles flow horizontally across the four monoliths, like
  // data crossing a system bus. Color cycles along the spectrum
  // of the four signature colors so the bus reads as a unifying
  // signal between projects.
  const PARTICLE_COUNT = 600;
  const pGeom = new THREE.BufferGeometry();
  const pPos  = new Float32Array(PARTICLE_COUNT * 3);
  const pCol  = new Float32Array(PARTICLE_COUNT * 3);
  const pSpd  = new Float32Array(PARTICLE_COUNT);

  const palette = [
    COLORS.ARES_RED, COLORS.ARES_GLOW, COLORS.ARES_PALE,
    COLORS.MCP_GREEN, COLORS.MCP_GLOW,
    COLORS.PALE, COLORS.WHITE,
    COLORS.CYAN,
  ];

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    pPos[i*3 + 0] = (Math.random() * 36) - 18;
    pPos[i*3 + 1] = Math.random() * 7.5 + 0.4;
    pPos[i*3 + 2] = (Math.random() * 18) - 9;

    const c = palette[Math.floor(Math.random() * palette.length)];
    pCol[i*3 + 0] = c.r;
    pCol[i*3 + 1] = c.g;
    pCol[i*3 + 2] = c.b;

    pSpd[i] = 0.025 + Math.random() * 0.085;
  }
  pGeom.setAttribute("position", new THREE.BufferAttribute(pPos, 3));
  pGeom.setAttribute("color",    new THREE.BufferAttribute(pCol, 3));

  const pMat = new THREE.PointsMaterial({
    size: 0.10,
    vertexColors: true,
    transparent: true,
    opacity: 0.95,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });
  const particles = new THREE.Points(pGeom, pMat);
  scene.add(particles);

  // Floor "grid scan" — a faint horizontal pulse that sweeps the floor
  const sweepGeom = new THREE.PlaneGeometry(160, 1.2);
  const sweepMat = new THREE.MeshBasicMaterial({
    color: 0x00d4ff,
    transparent: true,
    opacity: 0.20,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  const sweep = new THREE.Mesh(sweepGeom, sweepMat);
  sweep.rotation.x = -Math.PI / 2;
  sweep.position.y = 0.01;
  scene.add(sweep);

  // ─── Post-processing (bloom + scanline shader) ────────────────
  const composer = new EffectComposer(renderer);
  composer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  composer.setSize(window.innerWidth, window.innerHeight);
  composer.addPass(new RenderPass(scene, camera));

  const bloom = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    1.35, // strength
    0.65, // radius
    0.10, // threshold
  );
  composer.addPass(bloom);

  // Scanline / vignette shader — a CRT-ish post effect
  const scanShader = {
    uniforms: {
      tDiffuse:  { value: null },
      uTime:     { value: 0 },
      uScanInt:  { value: 0.06 },
      uVigInt:   { value: 0.55 },
    },
    vertexShader: /* glsl */ `
      varying vec2 vUv;
      void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }
    `,
    fragmentShader: /* glsl */ `
      varying vec2 vUv;
      uniform sampler2D tDiffuse;
      uniform float uTime;
      uniform float uScanInt;
      uniform float uVigInt;
      void main() {
        vec4 c = texture2D(tDiffuse, vUv);
        // scanlines
        float scan = 0.5 + 0.5 * sin((vUv.y * 1400.0) + uTime * 4.0);
        c.rgb *= 1.0 - uScanInt * (1.0 - scan);
        // vignette
        vec2 d = vUv - 0.5;
        float v = 1.0 - dot(d, d) * uVigInt * 2.4;
        c.rgb *= v;
        gl_FragColor = c;
      }
    `,
  };
  const scanPass = new ShaderPass(scanShader);
  composer.addPass(scanPass);
  composer.addPass(new OutputPass());

  // ─── Interaction state ────────────────────────────────────────
  let focused = null;            // currently-emphasized project slug
  const pointer = new THREE.Vector2();   // normalized mouse [-1,1]
  const pointerScreen = new THREE.Vector2(); // raw pixel
  const raycaster = new THREE.Raycaster();
  let scrollT = 0;               // 0..1 across page scroll

  window.addEventListener("pointermove", (e) => {
    pointer.x = (e.clientX / window.innerWidth)  * 2 - 1;
    pointer.y = -(e.clientY / window.innerHeight) * 2 + 1;
    pointerScreen.set(e.clientX, e.clientY);
  });

  // Direct click on a monolith → open repo
  canvas.addEventListener("click", () => {
    raycaster.setFromCamera(pointer, camera);
    const meshes = monoliths.map((m) => m.mesh);
    const hit = raycaster.intersectObjects(meshes, false)[0];
    if (hit) {
      const proj = monoliths.find((m) => m.mesh === hit.object).project;
      window.open(proj.url, "_blank", "noopener");
    }
  });

  // Wire HTML cards → focus events
  document.querySelectorAll("[data-project]").forEach((el) => {
    const slug = el.getAttribute("data-project");
    el.addEventListener("mouseenter", () => focusMonolith(slug));
    el.addEventListener("focus",      () => focusMonolith(slug));
    el.addEventListener("mouseleave", () => focusMonolith(null));
    el.addEventListener("blur",       () => focusMonolith(null));
  });
  function focusMonolith(slug) { focused = slug; }

  // Scroll → keep camera close on the four monoliths until past the
  // projects section, then drift back as the page continues. Bind to
  // scrollY normalized over document height.
  window.addEventListener("scroll", () => {
    const max = (document.body.scrollHeight - window.innerHeight) || 1;
    scrollT = Math.min(1, Math.max(0, window.scrollY / max));
  }, { passive: true });

  // Resize ───────────────────────────────────────────────────────
  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight, false);
    composer.setSize(window.innerWidth, window.innerHeight);
  });

  // ─── Animation loop ───────────────────────────────────────────
  const clock = new THREE.Clock();

  function tick() {
    const t  = clock.getElapsedTime();
    const dt = Math.min(0.05, clock.getDelta()); // clamp jank

    // Camera — slow auto-orbit + mouse parallax + scroll dolly
    const orbitR = 22 + Math.sin(t * 0.07) * 1.5;
    const yaw    = t * 0.08;
    const pitch  = 0.34 + scrollT * 0.18 + pointer.y * -0.05;
    camera.position.set(
      Math.sin(yaw) * orbitR + pointer.x * 1.2,
      4 + pitch * 6.2,
      Math.cos(yaw) * orbitR + pointer.y * 1.2,
    );
    camera.lookAt(0, 3 + pointer.y * 0.4, 0);

    // Monoliths — slow rotation + breathing emission
    for (const m of monoliths) {
      m.group.rotation.y += dt * 0.45;
      m.group.position.y = 2 + Math.sin(t * 0.6 + m.project.x * 0.4) * 0.08;
      const isFocus = focused === m.project.slug;
      const target  = isFocus ? 2.0 : (focused ? 0.7 : 1.15);
      m.mesh.material.emissiveIntensity +=
        (target - m.mesh.material.emissiveIntensity) * 0.08;
      m.light.intensity +=
        ((isFocus ? 3.4 : focused ? 0.9 : 1.6) - m.light.intensity) * 0.08;
      m.ring.material.opacity +=
        ((isFocus ? 0.95 : focused ? 0.35 : 0.65) - m.ring.material.opacity) * 0.08;
    }

    // Particles — sweep along x; respawn at the left when they exit
    const pos = pGeom.attributes.position.array;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      pos[i*3] += pSpd[i];
      if (pos[i*3] > 18) {
        pos[i*3]   = -18;
        pos[i*3+1] = Math.random() * 7.5 + 0.4;
        pos[i*3+2] = (Math.random() * 18) - 9;
      }
    }
    pGeom.attributes.position.needsUpdate = true;
    particles.rotation.y = Math.sin(t * 0.05) * 0.02;

    // Floor sweep — drift forward
    sweep.position.z = ((t * 4) % 60) - 30;
    sweep.material.opacity = 0.16 + Math.sin(t * 1.6) * 0.06;

    // Scanline shader uniform
    scanShader.uniforms.uTime.value = t;

    composer.render();
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);

  // Expose for HTML hover handlers — already wired above, but
  // also make it inspectable for debugging in DevTools.
  window.__AGENTS = { focusMonolith, monoliths, scene, camera, renderer };
}

// ─── Geometry factories ───────────────────────────────────────────
function makeSlab(w, h, d)  { return new THREE.BoxGeometry(w, h, d); }

function makePhone(w, h, d) {
  // Rounded box (approximation via ExtrudeGeometry would be cleaner;
  // BoxGeometry with bevelled scale is enough for distance viewing).
  const shape = new THREE.Shape();
  const r = 0.18;
  shape.moveTo(-w/2 + r, -h/2);
  shape.lineTo( w/2 - r, -h/2);
  shape.quadraticCurveTo(w/2, -h/2, w/2, -h/2 + r);
  shape.lineTo(w/2,  h/2 - r);
  shape.quadraticCurveTo(w/2, h/2, w/2 - r, h/2);
  shape.lineTo(-w/2 + r, h/2);
  shape.quadraticCurveTo(-w/2, h/2, -w/2, h/2 - r);
  shape.lineTo(-w/2, -h/2 + r);
  shape.quadraticCurveTo(-w/2, -h/2, -w/2 + r, -h/2);
  return new THREE.ExtrudeGeometry(shape, {
    depth: d,
    bevelEnabled: true,
    bevelSize: 0.04,
    bevelThickness: 0.04,
    curveSegments: 12,
  });
}

function makeCube(s) {
  // Slightly bevelled cube — feels less plasticky.
  const g = new THREE.BoxGeometry(s, s, s);
  return g;
}

function makeCpu(w, h, d) {
  // Wide low slab with a thinner inner die hint via beveled box.
  const g = new THREE.BoxGeometry(w, h, d);
  return g;
}
