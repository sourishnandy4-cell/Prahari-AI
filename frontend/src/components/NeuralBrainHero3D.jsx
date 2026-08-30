import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function NeuralBrainHero3D({ phase = 0, className = '' }) {
  const mountRef = useRef(null);
  const phaseRef = useRef(phase);
  phaseRef.current = phase;

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    let animationFrameId;
    let width = container.clientWidth || window.innerWidth || 1000;
    let height = container.clientHeight || window.innerHeight || 700;

    // ── 1. Scene & Camera Setup ─────────────────────────────────────────────
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, width / height, 0.1, 100);
    const defaultCamPos = new THREE.Vector3(0, 0.25, 5.8);
    camera.position.copy(defaultCamPos);
    camera.lookAt(0, 0, 0);

    // ── 2. High-Performance WebGL Renderer ──────────────────────────────────
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance',
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(0x000000, 0); // 100% Seamless Transparent
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.45;
    container.appendChild(renderer.domElement);

    const brainGroup = new THREE.Group();
    scene.add(brainGroup);

    // ── 3. Texture Atlas for Glowing Matrix Digits & Neural Nodes ───────────
    const createMatrixTextureAtlas = () => {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 512;
      const ctx = canvas.getContext('2d');

      // 4x4 Grid of Glyphs (0..9, Matrix characters, glowing dots)
      const glyphs = [
        '0', '1', '7', '8',
        '9', '4', 'λ', '§',
        'Ø', 'X', '✦', '▲',
        '•', '●', '☼', '※'
      ];

      ctx.clearRect(0, 0, 512, 512);
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      for (let i = 0; i < 16; i++) {
        const gx = (i % 4) * 128 + 64;
        const gy = Math.floor(i / 4) * 128 + 64;

        // Glowing backdrop aura
        const rad = ctx.createRadialGradient(gx, gy, 0, gx, gy, 56);
        rad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        rad.addColorStop(0.3, 'rgba(215, 240, 255, 0.85)');
        rad.addColorStop(0.65, 'rgba(125, 211, 252, 0.35)');
        rad.addColorStop(1, 'rgba(0, 0, 0, 0)');

        if (i >= 12) {
          // Circular particle nodes
          ctx.fillStyle = rad;
          ctx.beginPath();
          ctx.arc(gx, gy, 54, 0, Math.PI * 2);
          ctx.fill();
        } else {
          // Matrix numeric & symbol glyphs with intense glow
          ctx.font = 'bold 54px monospace';
          ctx.shadowColor = '#38bdf8';
          ctx.shadowBlur = 18;
          ctx.fillStyle = '#ffffff';
          ctx.fillText(glyphs[i], gx, gy);

          ctx.shadowBlur = 4;
          ctx.fillStyle = '#f8fafc';
          ctx.fillText(glyphs[i], gx, gy);
        }
      }

      const texture = new THREE.CanvasTexture(canvas);
      texture.needsUpdate = true;
      return texture;
    };

    const particleTexture = createMatrixTextureAtlas();

    // ── 4. High-Density Brain Anatomy & Particle Field (8,500 Points) ───────
    const DENSE_POINTS = 8500;
    const positions = new Float32Array(DENSE_POINTS * 3);
    const basePositions = new Float32Array(DENSE_POINTS * 3);
    const velocities = new Float32Array(DENSE_POINTS * 3);
    const colors = new Float32Array(DENSE_POINTS * 3);
    const sizes = new Float32Array(DENSE_POINTS);
    const randomPhases = new Float32Array(DENSE_POINTS);

    const cWhite = new THREE.Color(0xffffff);
    const cSilver = new THREE.Color(0xe4e4e7);
    const cSky = new THREE.Color(0x7dd3fc);
    const cCyanGlow = new THREE.Color(0x38bdf8);

    for (let i = 0; i < DENSE_POINTS; i++) {
      const hemi = i % 2 === 0 ? 1 : -1;

      // Golden ratio spherical sampling
      const phi = Math.acos(1 - 2 * (i / DENSE_POINTS));
      const theta = Math.sqrt(DENSE_POINTS * Math.PI) * phi;

      const rx = 1.38;
      const ry = 1.16;
      const rz = 1.66;

      let x = Math.sin(phi) * Math.cos(theta) * rx;
      let y = Math.cos(phi) * ry;
      let z = Math.sin(phi) * Math.sin(theta) * rz;

      // Hemispheric separation with longitudinal fissure
      x = hemi * (Math.abs(x) * 0.86 + 0.16);

      // Anatomical Lobes:
      // Frontal Lobe (prominent rounded anterior)
      if (z > 0) {
        x *= 1.0 + 0.12 * (z / rz);
        y *= 1.0 + 0.08 * (z / rz);
      } else {
        // Occipital Lobe (slopes posterior-inferior)
        y -= 0.18 * Math.pow(Math.abs(z) / rz, 1.8);
        x *= 1.0 - 0.16 * Math.pow(Math.abs(z) / rz, 1.3);
      }

      // Temporal Lobe (lateral bulge mid-anterior)
      if (y < 0.28 && y > -0.55 && z > -0.38 && z < 0.85) {
        x *= 1.18;
      }

      // Cerebellum (posterior-inferior cauliflower lobe)
      const isCerebellum = (z < -0.32 && y < -0.36);
      if (isCerebellum) {
        x *= 0.82;
        y -= 0.26;
        z -= 0.14;
      }

      // High-Frequency Cortical Folding (Gyri & Sulci ridges)
      const f1 = 9.2;
      const f2 = 18.5;
      const folds =
        Math.sin(x * f1) * Math.cos(y * f1) * Math.sin(z * f1) * 0.12 +
        Math.sin(x * f2 + z * f2) * 0.05 +
        Math.cos(y * f2 + x * f2) * 0.04;

      // Medial Fissure Cleft
      const fissure = Math.exp(-Math.pow(x / 0.34, 2)) * 0.24;
      const rMod = 1.0 + folds - fissure;

      x *= rMod;
      y *= rMod;
      z *= rMod;

      // Volumetric cortex depth (35% internal density)
      if (Math.random() < 0.35) {
        const depth = 0.55 + Math.random() * 0.42;
        x *= depth;
        y *= depth;
        z *= depth;
      }

      const idx = i * 3;
      positions[idx] = x;
      positions[idx + 1] = y;
      positions[idx + 2] = z;

      basePositions[idx] = x;
      basePositions[idx + 1] = y;
      basePositions[idx + 2] = z;

      // 3D Dispersion Velocity Vectors (Radial blast + curl vortex)
      const dist = Math.sqrt(x * x + y * y + z * z) || 1;
      const speed = 1.4 + Math.random() * 3.4;
      velocities[idx] = (x / dist) * speed + (Math.random() - 0.5) * 1.6;
      velocities[idx + 1] = (y / dist) * speed + (Math.random() - 0.5) * 1.6;
      velocities[idx + 2] = (z / dist) * speed + (Math.random() - 0.5) * 1.6;

      // Color distribution (Bright pure silver-white core with cyan synaptic highlights)
      const rand = Math.random();
      let col = cWhite;
      if (rand < 0.22) col = cCyanGlow;
      else if (rand < 0.45) col = cSky;
      else if (rand < 0.8) col = cSilver;

      colors[idx] = col.r;
      colors[idx + 1] = col.g;
      colors[idx + 2] = col.b;

      sizes[i] = 0.048 + Math.random() * 0.045;
      randomPhases[i] = Math.random() * Math.PI * 2;
    }

    const brainGeometry = new THREE.BufferGeometry();
    brainGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    brainGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const brainMaterial = new THREE.PointsMaterial({
      size: 0.075,
      map: particleTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.95,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const brainPoints = new THREE.Points(brainGeometry, brainMaterial);
    brainGroup.add(brainPoints);

    // ── 5. Synaptic Neural Network Connections (Axon Lines) ─────────────────
    const lineIndices = [];
    const CONNECT_DIST_SQ = 0.22 * 0.22;
    const MAX_CONN = 2;

    for (let i = 0; i < Math.min(DENSE_POINTS, 1600); i += 2) {
      let count = 0;
      const ix = basePositions[i * 3];
      const iy = basePositions[i * 3 + 1];
      const iz = basePositions[i * 3 + 2];

      for (let j = i + 1; j < Math.min(DENSE_POINTS, 1600); j++) {
        if (count >= MAX_CONN) break;
        const jx = basePositions[j * 3];
        const jy = basePositions[j * 3 + 1];
        const jz = basePositions[j * 3 + 2];

        const dx = ix - jx;
        const dy = iy - jy;
        const dz = iz - jz;
        const dSq = dx * dx + dy * dy + dz * dz;

        if (dSq < CONNECT_DIST_SQ) {
          lineIndices.push(i, j);
          count++;
        }
      }
    }

    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(new Float32Array(positions), 3));
    lineGeometry.setIndex(lineIndices);

    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0xbae6fd,
      transparent: true,
      opacity: 0.32,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const lineSystem = new THREE.LineSegments(lineGeometry, lineMaterial);
    brainGroup.add(lineSystem);

    // ── 6. Luminous Inner Neural Core & Volumetric Glow ─────────────────────
    const innerLight = new THREE.PointLight(0x38bdf8, 4.0, 7.5, 1.3);
    brainGroup.add(innerLight);

    const coreGeo = new THREE.SphereGeometry(0.7, 24, 24);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x0284c7,
      transparent: true,
      opacity: 0.16,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const coreGlowMesh = new THREE.Mesh(coreGeo, coreMat);
    brainGroup.add(coreGlowMesh);

    // ── 7. Infinite Cosmic Stardust Field (Zero Bounding Borders) ───────────
    const DUST_COUNT = 220;
    const dustGeo = new THREE.BufferGeometry();
    const dustPos = new Float32Array(DUST_COUNT * 3);
    for (let i = 0; i < DUST_COUNT * 3; i += 3) {
      dustPos[i] = (Math.random() - 0.5) * 12.0;
      dustPos[i + 1] = (Math.random() - 0.5) * 8.0;
      dustPos[i + 2] = (Math.random() - 0.5) * 8.0;
    }
    dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));

    const dustMat = new THREE.PointsMaterial({
      size: 0.05,
      map: particleTexture,
      color: 0xffffff,
      transparent: true,
      opacity: 0.5,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    const dustPoints = new THREE.Points(dustGeo, dustMat);
    scene.add(dustPoints);

    // ── 8. Dynamic Parallax & Timeline Interpolation ────────────────────────
    const mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };
    const handleMouseMove = (e) => {
      const normX = (e.clientX / window.innerWidth) * 2 - 1;
      const normY = -(e.clientY / window.innerHeight) * 2 + 1;
      mouse.targetX = normX;
      mouse.targetY = normY;
    };
    window.addEventListener('mousemove', handleMouseMove, { passive: true });

    let clock = new THREE.Clock();
    let currentDispersion = 0;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsed = clock.getElapsedTime();
      const curPhase = phaseRef.current;

      // Mouse Parallax Lerp
      mouse.x += (mouse.targetX - mouse.x) * 0.05;
      mouse.y += (mouse.targetY - mouse.y) * 0.05;

      camera.position.x = defaultCamPos.x + mouse.x * 0.75;
      camera.position.y = defaultCamPos.y + mouse.y * 0.45;
      camera.lookAt(0, 0, 0);

      // Organic 3D Brain Rotation
      brainGroup.rotation.y = elapsed * 0.24 + mouse.x * 0.22;
      brainGroup.rotation.x = Math.sin(elapsed * 0.4) * 0.08 - mouse.y * 0.18;
      brainGroup.rotation.z = Math.cos(elapsed * 0.3) * 0.05;

      // Phase-Driven Dispersion Factor
      // Phase 0: 0.0 (Compact intact anatomical human brain)
      // Phase 1: 1.0 (Full infinite dispersion into cybernetic nebula)
      // Phase 2: 0.82 (Cosmic stardust halo framing Prahari reveal)
      let targetDispersion = 0;
      if (curPhase === 1) targetDispersion = 1.0;
      else if (curPhase === 2) targetDispersion = 0.82;

      currentDispersion += (targetDispersion - currentDispersion) * 0.038;

      // Update Particle Positions & Firing Impulses
      const posArr = brainGeometry.attributes.position.array;
      const colArr = brainGeometry.attributes.color.array;
      const linePosArr = lineGeometry.attributes.position.array;

      for (let i = 0; i < DENSE_POINTS; i++) {
        const idx = i * 3;
        const bx = basePositions[idx];
        const by = basePositions[idx + 1];
        const bz = basePositions[idx + 2];

        const vx = velocities[idx];
        const vy = velocities[idx + 1];
        const vz = velocities[idx + 2];

        // Cortical Breathing Micro-Oscillation
        const pulse = 1.0 + Math.sin(elapsed * 2.5 + randomPhases[i]) * 0.028;

        // Position morphing
        const px = bx * pulse + vx * currentDispersion * 1.9;
        const py = by * pulse + vy * currentDispersion * 1.9;
        const pz = bz * pulse + vz * currentDispersion * 1.9;

        posArr[idx] = px;
        posArr[idx + 1] = py;
        posArr[idx + 2] = pz;

        linePosArr[idx] = px;
        linePosArr[idx + 1] = py;
        linePosArr[idx + 2] = pz;

        // Synaptic Spark Traversal (Traveling Electrical Waves)
        if (i % 20 === 0) {
          const spark = Math.max(0, Math.sin(elapsed * 6.0 + randomPhases[i]));
          colArr[idx] = 1.0;
          colArr[idx + 1] = 0.88 + spark * 0.12;
          colArr[idx + 2] = 0.65 + spark * 0.35;
        }
      }

      brainGeometry.attributes.position.needsUpdate = true;
      brainGeometry.attributes.color.needsUpdate = true;
      lineGeometry.attributes.position.needsUpdate = true;

      // Dynamic Material Adjustments
      lineMaterial.opacity = Math.max(0.01, 0.32 * (1.0 - currentDispersion * 0.92));
      innerLight.intensity = 3.2 + Math.sin(elapsed * 4.0) * 1.5;
      coreGlowMesh.scale.setScalar(1.0 + Math.sin(elapsed * 2.2) * 0.18);
      coreMat.opacity = Math.max(0.02, 0.16 * (1.0 - currentDispersion * 0.85));

      // Drift Stardust Motes
      const dPos = dustGeo.attributes.position.array;
      for (let i = 1; i < DUST_COUNT * 3; i += 3) {
        dPos[i] += 0.0035;
        if (dPos[i] > 4.2) dPos[i] = -4.2;
      }
      dustGeo.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    // ── 9. Resize Handling ──────────────────────────────────────────────────
    const handleResize = () => {
      if (!container) return;
      width = container.clientWidth || window.innerWidth;
      height = container.clientHeight || window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    };
    window.addEventListener('resize', handleResize);

    // ── 10. Cleanup & Memory Free ───────────────────────────────────────────
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);

      [brainGeometry, lineGeometry, dustGeo, coreGeo].forEach((g) => g?.dispose?.());
      [brainMaterial, lineMaterial, dustMat, coreMat].forEach((m) => m?.dispose?.());
      particleTexture?.dispose?.();

      renderer.dispose();
      if (renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div className={`relative w-full h-full flex items-center justify-center overflow-hidden pointer-events-none ${className}`}>
      <div
        ref={mountRef}
        className="w-full h-full select-none"
        style={{ touchAction: 'none' }}
      />
    </div>
  );
}
