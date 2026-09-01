import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export default function RollingCoinHero3D({ className = '' }) {
  const mountRef = useRef(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    let animationFrameId;
    let width = container.clientWidth || window.innerWidth || 600;
    let height = container.clientHeight || window.innerHeight || 600;

    // ── 1. Scene Setup ──────────────────────────────────────────────────────────
    const scene = new THREE.Scene();

    // ── 2. Camera Setup ────────────────────────────────────────────────────────
    const camera = new THREE.PerspectiveCamera(34, width / height, 0.1, 50);
    const defaultCamPos = new THREE.Vector3(4.5, 4.8, 5.4);
    camera.position.copy(defaultCamPos);
    camera.lookAt(0, 0.25, 0);

    // ── 3. High-Performance WebGL Renderer (Lag-Free) ─────────────────────────
    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({
        antialias: true,
        alpha: true,
        powerPreference: 'high-performance',
        precision: 'mediump',
      });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
      renderer.setClearColor(0x000000, 0); // 100% transparent background
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.2;
      container.appendChild(renderer.domElement);
    } catch (e) {
      console.warn('[RollingCoinHero3D] WebGL initialization failed:', e);
      return;
    }

    // ── 4. Fast Cinematic Lighting (Zero Shadow Map Overhead) ─────────────────
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x1e1e2f, 1.5);
    scene.add(hemiLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 2.6);
    keyLight.position.set(6, 12, 5);
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0x60a5fa, 1.4);
    rimLight.position.set(-6, 6, -5);
    scene.add(rimLight);

    // Rotating Neon Violet Spotlight & Point Light
    const neonSpotLight = new THREE.SpotLight(0xe879f9, 7.0, 14, Math.PI / 3, 0.4, 1.0);
    scene.add(neonSpotLight);

    const neonPointLight = new THREE.PointLight(0xc084fc, 5.0, 7.0, 1.2);
    scene.add(neonPointLight);

    const cyanPointLight = new THREE.PointLight(0x38bdf8, 3.0, 6.0, 1.3);
    scene.add(cyanPointLight);

    // ── 5. Optimized Premium Materials ─────────────────────────────────────────
    // Glassy Translucent Acrylic Track Material (Smooth, Fast, High Clearcoat Specular)
    const frostedGlassMaterial = new THREE.MeshPhysicalMaterial({
      color: new THREE.Color(0xdce7f5),
      roughness: 0.1,
      metalness: 0.05,
      clearcoat: 1.0,
      clearcoatRoughness: 0.08,
      transparent: true,
      opacity: 0.65,
      side: THREE.DoubleSide,
    });

    const frostedWedgeMaterial = new THREE.MeshPhysicalMaterial({
      color: new THREE.Color(0xe0e7ff),
      roughness: 0.12,
      metalness: 0.02,
      clearcoat: 0.9,
      clearcoatRoughness: 0.1,
      transparent: true,
      opacity: 0.55,
      side: THREE.DoubleSide,
    });

    // 24K Highly Reflective Gold Coin Material
    const goldCoinMaterial = new THREE.MeshStandardMaterial({
      color: new THREE.Color(0xffb703),
      roughness: 0.14,
      metalness: 0.96,
    });

    const goldTrimMaterial = new THREE.MeshStandardMaterial({
      color: new THREE.Color(0xffe57f),
      roughness: 0.18,
      metalness: 0.92,
    });

    // ── 6. Geometries & Meshes ─────────────────────────────────────────────────
    const rootGroup = new THREE.Group();
    scene.add(rootGroup);

    // ── A. Transparent Floor Grid ──
    const gridHelper = new THREE.GridHelper(20, 28, 0x52525b, 0x27272a);
    gridHelper.position.y = 0.001;
    rootGroup.add(gridHelper);

    // ── B. Frosted Glass Curved Track ──
    const trackInnerR = 1.7;
    const trackOuterR = 2.45;
    const trackMidR = (trackInnerR + trackOuterR) / 2; // 2.075
    const trackHeight = 0.52;
    const angleStart = -Math.PI * 0.82;
    const angleEnd = Math.PI * 0.82;
    const arcSegments = 48;

    const trackShape = new THREE.Shape();
    // Outer arc
    for (let i = 0; i <= arcSegments; i++) {
      const theta = angleStart + (angleEnd - angleStart) * (i / arcSegments);
      const x = Math.cos(theta) * trackOuterR;
      const y = Math.sin(theta) * trackOuterR;
      if (i === 0) trackShape.moveTo(x, y);
      else trackShape.lineTo(x, y);
    }
    // Inner arc
    for (let i = arcSegments; i >= 0; i--) {
      const theta = angleStart + (angleEnd - angleStart) * (i / arcSegments);
      const x = Math.cos(theta) * trackInnerR;
      const y = Math.sin(theta) * trackInnerR;
      trackShape.lineTo(x, y);
    }
    trackShape.closePath();

    const extrudeSettings = {
      depth: trackHeight,
      bevelEnabled: true,
      bevelSegments: 2,
      steps: 1,
      bevelSize: 0.04,
      bevelThickness: 0.04,
    };

    const trackGeo = new THREE.ExtrudeGeometry(trackShape, extrudeSettings);
    trackGeo.rotateX(Math.PI / 2);
    trackGeo.computeVertexNormals();

    const trackMesh = new THREE.Mesh(trackGeo, frostedGlassMaterial);
    trackMesh.position.y = trackHeight + 0.04;
    rootGroup.add(trackMesh);

    // ── C. Inner Central Wedge Platform ──
    const wedgeShape = new THREE.Shape();
    const wedgeR = 1.35;
    const wedgeSegments = 24;
    wedgeShape.moveTo(0, 0);
    for (let i = 0; i <= wedgeSegments; i++) {
      const theta = (Math.PI * 0.36) * (i / wedgeSegments);
      wedgeShape.lineTo(Math.cos(theta) * wedgeR, Math.sin(theta) * wedgeR);
    }
    wedgeShape.closePath();

    const wedgeGeo = new THREE.ExtrudeGeometry(wedgeShape, {
      depth: trackHeight * 0.88,
      bevelEnabled: true,
      bevelSegments: 2,
      steps: 1,
      bevelSize: 0.03,
      bevelThickness: 0.03,
    });
    wedgeGeo.rotateX(Math.PI / 2);
    wedgeGeo.computeVertexNormals();

    const wedgeMesh = new THREE.Mesh(wedgeGeo, frostedWedgeMaterial);
    wedgeMesh.position.set(0, trackHeight * 0.88 + 0.03, 0);
    wedgeMesh.rotation.y = -0.15;
    rootGroup.add(wedgeMesh);

    // ── D. Minimalist Pedestal Blocks ──
    const step1Geo = new THREE.BoxGeometry(0.65, 0.26, 0.42);
    const step1 = new THREE.Mesh(step1Geo, frostedGlassMaterial);
    step1.position.set(-1.82, 0.13, 1.42);
    step1.rotation.y = 0.5;
    rootGroup.add(step1);

    const step2Geo = new THREE.BoxGeometry(0.5, 0.16, 0.38);
    const step2 = new THREE.Mesh(step2Geo, frostedGlassMaterial);
    step2.position.set(-2.15, 0.08, 1.08);
    step2.rotation.y = 0.4;
    rootGroup.add(step2);

    // ── E. Perfectly Oriented Upright Rolling 24K Golden Coin ──
    // coinGroup handles positioning along track curve and tangential orientation
    const coinGroup = new THREE.Group();
    rootGroup.add(coinGroup);

    // coinSpinner handles the actual rolling spin around its axle
    const coinSpinner = new THREE.Group();
    coinGroup.add(coinSpinner);

    const coinRadius = 0.32;
    const coinThickness = 0.075;

    // Cylinder with its circular caps pointing along local X axis (so it stands upright on its rim)
    const coinGeo = new THREE.CylinderGeometry(coinRadius, coinRadius, coinThickness, 36);
    coinGeo.rotateZ(Math.PI / 2); // Rotate cylinder so faces are at X = ±coinThickness/2
    const coinBody = new THREE.Mesh(coinGeo, goldCoinMaterial);
    coinSpinner.add(coinBody);

    // Outer Raised Rim on both faces (oriented along X)
    const rimGeo = new THREE.TorusGeometry(coinRadius * 0.88, 0.015, 12, 36);
    rimGeo.rotateY(Math.PI / 2);

    const rimFront = new THREE.Mesh(rimGeo, goldTrimMaterial);
    rimFront.position.x = coinThickness / 2 + 0.001;
    coinSpinner.add(rimFront);

    const rimBack = new THREE.Mesh(rimGeo, goldTrimMaterial);
    rimBack.position.x = -coinThickness / 2 - 0.001;
    coinSpinner.add(rimBack);

    // Center Emblem Rings on both faces
    const starGeo = new THREE.RingGeometry(0.04, 0.13, 6);
    starGeo.rotateY(Math.PI / 2);

    const emblemFront = new THREE.Mesh(starGeo, goldTrimMaterial);
    emblemFront.position.x = coinThickness / 2 + 0.002;
    coinSpinner.add(emblemFront);

    const emblemBack = new THREE.Mesh(starGeo, goldTrimMaterial);
    emblemBack.position.x = -coinThickness / 2 - 0.002;
    coinSpinner.add(emblemBack);

    // ── F. Rotating Neon Laser Sweep Beam ──
    const laserBeamGeo = new THREE.CylinderGeometry(0.014, 0.014, 3.0, 12);
    const laserBeamMat = new THREE.MeshBasicMaterial({
      color: 0xe879f9,
      transparent: true,
      opacity: 0.88,
    });
    const laserBeam = new THREE.Mesh(laserBeamGeo, laserBeamMat);
    laserBeam.rotation.z = Math.PI / 2;
    laserBeam.position.set(1.5, trackHeight + 0.02, 0);

    const laserPivot = new THREE.Group();
    laserPivot.add(laserBeam);
    rootGroup.add(laserPivot);

    // ── G. Lightweight Floating Dust Motes ──
    const particleCount = 30;
    const particleGeo = new THREE.BufferGeometry();
    const particlePos = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i += 3) {
      particlePos[i] = (Math.random() - 0.5) * 7;
      particlePos[i + 1] = Math.random() * 3.5 + 0.2;
      particlePos[i + 2] = (Math.random() - 0.5) * 7;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0xc084fc,
      size: 0.045,
      transparent: true,
      opacity: 0.55,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    rootGroup.add(particles);

    // ── 7. Interactive Parallax Controller ────────────────────────────────────
    const mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };
    const handleMouseMove = (e) => {
      const normX = (e.clientX / window.innerWidth) * 2 - 1;
      const normY = -(e.clientY / window.innerHeight) * 2 + 1;
      mouse.targetX = normX;
      mouse.targetY = normY;
    };

    window.addEventListener('mousemove', handleMouseMove, { passive: true });

    // ── 8. Physics & Rolling Kinematics Animation Loop ────────────────────────
    const startTime = performance.now();
    let accumulatedRollAngle = 0;
    let prevTheta = 0;

    // Track surface height is at y = trackHeight + 0.08
    // Coin bottom rim rests exactly on top surface of the track:
    const coinCenterY = trackHeight + 0.08 + coinRadius;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = (performance.now() - startTime) / 1000;

      // Smooth camera mouse parallax lerp
      mouse.x += (mouse.targetX - mouse.x) * 0.05;
      mouse.y += (mouse.targetY - mouse.y) * 0.05;

      camera.position.x = defaultCamPos.x + mouse.x * 0.75;
      camera.position.y = defaultCamPos.y + mouse.y * 0.5;
      camera.position.z = defaultCamPos.z - mouse.y * 0.35;
      camera.lookAt(0, 0.25, 0);

      // ── A. Precise Rolling Coin Kinematics ──
      const cycleDuration = 6.8; // seconds for back-and-forth oscillation
      const cycleProgress = (elapsedTime % cycleDuration) / cycleDuration;
      // Smooth sinusoidal movement along the arc with soft turning at boundaries
      const easeArc = 0.5 - 0.5 * Math.cos(cycleProgress * Math.PI * 2);
      const arcMargin = 0.22;
      const currentTheta = (angleStart + arcMargin) + (angleEnd - angleStart - 2 * arcMargin) * easeArc;

      // Position coin center on track
      const coinX = Math.cos(currentTheta) * trackMidR;
      const coinZ = Math.sin(currentTheta) * trackMidR;
      coinGroup.position.set(coinX, coinCenterY, coinZ);

      // Orient coin group so local X is radial and local Z is tangent forward along track
      coinGroup.rotation.y = -currentTheta;

      // Accurate roll distance calculation (s = r_track * d_theta)
      if (prevTheta !== 0) {
        const deltaTheta = currentTheta - prevTheta;
        const deltaDist = trackMidR * deltaTheta;
        const deltaRoll = deltaDist / coinRadius;
        accumulatedRollAngle += deltaRoll;
      }
      prevTheta = currentTheta;

      // Roll the upright coin around its horizontal axle (local X-axis)
      coinSpinner.rotation.x = accumulatedRollAngle;

      // Subtle dynamic lean into the curve (centripetal lean)
      const rollVelocity = Math.sin(cycleProgress * Math.PI * 2);
      coinSpinner.rotation.z = rollVelocity * 0.06;

      // ── B. Neon Sweep & Lights ──
      const sweepAngle = elapsedTime * 0.9;
      laserPivot.rotation.y = sweepAngle;

      neonSpotLight.position.set(
        Math.cos(sweepAngle) * 3.2,
        1.6,
        Math.sin(sweepAngle) * 3.2
      );
      neonSpotLight.target = trackMesh;

      neonPointLight.position.set(
        Math.cos(sweepAngle) * 2.0,
        0.55 + Math.sin(elapsedTime * 2.0) * 0.15,
        Math.sin(sweepAngle) * 2.0
      );

      cyanPointLight.position.set(
        Math.cos(-sweepAngle * 0.7) * 2.8,
        1.1,
        Math.sin(-sweepAngle * 0.7) * 2.8
      );

      // Drift dust particles
      const positions = particleGeo.attributes.position.array;
      for (let i = 1; i < particleCount * 3; i += 3) {
        positions[i] += 0.003;
        if (positions[i] > 3.8) positions[i] = 0.2;
      }
      particleGeo.attributes.position.needsUpdate = true;

      // Render scene
      renderer.render(scene, camera);
    };

    animate();

    // ── 9. Resize Handler ────────────────────────────────────────────────────
    const handleResize = () => {
      if (!container) return;
      width = container.clientWidth || window.innerWidth;
      height = container.clientHeight || window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    };

    window.addEventListener('resize', handleResize);

    // ── 10. Memory Cleanup on Unmount ────────────────────────────────────────
    return () => {
      if (animationFrameId) cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);

      [
        trackGeo,
        wedgeGeo,
        step1Geo,
        step2Geo,
        coinGeo,
        rimGeo,
        starGeo,
        laserBeamGeo,
        particleGeo,
      ].forEach((g) => g?.dispose?.());

      [
        frostedGlassMaterial,
        frostedWedgeMaterial,
        goldCoinMaterial,
        goldTrimMaterial,
        laserBeamMat,
        particleMat,
      ].forEach((m) => m?.dispose?.());

      if (renderer) {
        renderer.dispose();
        if (renderer.domElement && container.contains(renderer.domElement)) {
          container.removeChild(renderer.domElement);
        }
      }
    };
  }, []);

  return (
    <div className={`relative w-full h-full flex items-center justify-center overflow-hidden ${className}`}>
      <div
        ref={mountRef}
        className="w-full h-full select-none"
        style={{ touchAction: 'none' }}
      />
    </div>
  );
}
