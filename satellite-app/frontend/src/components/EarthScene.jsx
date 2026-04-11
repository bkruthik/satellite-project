import { useEffect, useRef } from "react";
import * as THREE from "three";

export default function EarthScene() {
  const mountRef = useRef(null);

  useEffect(() => {
    // Scene
    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(
      60,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.set(0, 0, 4);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setClearColor(0x000000, 1);
    mountRef.current.appendChild(renderer.domElement);

    // 🌍 Load texture safely
    const loader = new THREE.TextureLoader();
    loader.load(
      "https://raw.githubusercontent.com/creativetimofficial/public-assets/master/earth-night.jpg",
      (texture) => {
        const geometry = new THREE.SphereGeometry(1.5, 64, 64);
        const material = new THREE.MeshStandardMaterial({ map: texture });
        const earth = new THREE.Mesh(geometry, material);
        scene.add(earth);

        // 💡 Lights (THIS FIXES BLACK SCREEN)
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(5, 3, 5);
        scene.add(directionalLight);

        // 🔄 Animate
        const animate = () => {
          earth.rotation.y += 0.0015;
          renderer.render(scene, camera);
          requestAnimationFrame(animate);
        };
        animate();
      },
      undefined,
      (error) => {
        console.error("Texture load error:", error);
      }
    );

    // 🔄 Handle resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener("resize", handleResize);

    // 🧹 Cleanup
    return () => {
      window.removeEventListener("resize", handleResize);
      mountRef.current.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <div
      ref={mountRef}
      style={{ width: "100vw", height: "100vh", background: "black" }}
    />
  );
}