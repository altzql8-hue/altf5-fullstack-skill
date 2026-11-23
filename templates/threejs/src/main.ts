import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import './styles.css';

const mount = document.querySelector<HTMLElement>('#canvas-container');
const toggle = document.querySelector<HTMLButtonElement>('#toggle');
const status = document.querySelector<HTMLElement>('#status');
if (!mount || !toggle || !status) throw new Error('3D mount elements missing');
const host = mount;
const button = toggle;
const message = status;
let paused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let disposed = false;
let renderer: THREE.WebGLRenderer;
try {
  renderer = new THREE.WebGLRenderer({antialias:true, alpha:false, powerPreference:'high-performance'});
} catch {
  host.textContent = 'WebGL is unavailable. Try a WebGL-capable browser or device.';
  button.disabled = true;
  throw new Error('WebGL renderer initialization failed');
}
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x0c1324);
renderer.outputColorSpace = THREE.SRGBColorSpace;
host.appendChild(renderer.domElement);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(55,1,.1,100);
camera.position.set(2.7,2,4.5);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false;
controls.minDistance = 2;
controls.maxDistance = 9;
const geometry = new THREE.BoxGeometry(1.65,1.65,1.65);
const material = new THREE.MeshStandardMaterial({color:0x7aa5ff,metalness:.3,roughness:.28});
const cube = new THREE.Mesh(geometry,material);
scene.add(cube);
scene.add(new THREE.HemisphereLight(0xffffff,0x273257,2));
const light = new THREE.DirectionalLight(0xffffff,2.7);
light.position.set(3,6,5);
scene.add(light);
const resize = () => {
  const width = Math.max(1, host.clientWidth);
  const height = Math.max(1, host.clientHeight);
  camera.aspect = width/height;
  camera.updateProjectionMatrix();
  renderer.setSize(width,height,false);
};
const observer = new ResizeObserver(resize);
observer.observe(host);
resize();
function syncButton(){button.textContent = paused ? 'Resume animation' : 'Pause animation';button.setAttribute('aria-pressed',String(paused));}
syncButton();
button.addEventListener('click', () => {paused=!paused;syncButton();});
const clock = new THREE.Clock();
const animate = () => {
  if (disposed) return;
  const delta = Math.min(clock.getDelta(),.05);
  if (!paused) cube.rotation.y += delta*.65;
  controls.update();
  renderer.render(scene,camera);
};
renderer.setAnimationLoop(animate);
function dispose() {
  if(disposed)return;
  disposed=true;
  renderer.setAnimationLoop(null);
  observer.disconnect();
  controls.dispose();
  geometry.dispose();
  material.dispose();
  renderer.dispose();
  renderer.domElement.remove();
}
window.addEventListener('pagehide',dispose,{once:true});
renderer.domElement.addEventListener('webglcontextlost',(event)=>{event.preventDefault();paused=true;message.textContent='Graphics context lost; reload the page to retry.';renderer.setAnimationLoop(null);button.disabled=true;});
