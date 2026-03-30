/**
 * Terra 3D Viewer - Common Viewer Logic
 *
 * Shared Three.js viewer functionality for OBJ and PLY formats
 * Designed to be embedded in standalone HTML files
 *
 * @version 2.0.0
 * @requires Three.js r167+
 */

// This will be imported as an ES module
// Usage: import { TerraViewer } from './viewer-common.js';

export class TerraViewer {
    constructor(config = {}) {
        // Configuration
        this.config = {
            containerId: config.containerId || 'canvas-container',
            showGrid: config.showGrid !== false,
            showAxes: config.showAxes || false,
            enableShadows: config.enableShadows !== false,
            backgroundColor: config.backgroundColor || 0x1a1a1a,
            cameraPosition: config.cameraPosition || [5, 5, 5],
            autoRotate: config.autoRotate || false,
            ...config
        };

        // State
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.model = null;
        this.lights = {};
        this.helpers = {};
        this.isLoading = false;
        this.loadingProgress = 0;
        this.currentPreset = 'default';

        // Performance tracking
        this.stats = {
            vertices: 0,
            faces: 0,
            loadTime: 0
        };
    }

    /**
     * Initialize the viewer
     */
    async init(THREE, OrbitControls) {
        this.THREE = THREE;

        // Setup scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(this.config.backgroundColor);

        // Setup camera
        const container = document.getElementById(this.config.containerId);
        const aspect = container.clientWidth / container.clientHeight;
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.set(...this.config.cameraPosition);

        // Setup renderer
        this.renderer = new THREE.WebGLRenderer({
            antialias: true,
            alpha: true,
            preserveDrawingBuffer: true // Required for screenshots
        });
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        if (this.config.enableShadows) {
            this.renderer.shadowMap.enabled = true;
            this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        }

        container.appendChild(this.renderer.domElement);

        // Setup controls
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        this.controls.screenSpacePanning = false;
        this.controls.minDistance = 1;
        this.controls.maxDistance = 100;
        this.controls.autoRotate = this.config.autoRotate;
        this.controls.autoRotateSpeed = 2.0;

        // Setup lighting
        this.setupLighting();

        // Setup helpers
        if (this.config.showGrid) {
            this.helpers.grid = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
            this.scene.add(this.helpers.grid);
        }

        if (this.config.showAxes) {
            this.helpers.axes = new THREE.AxesHelper(5);
            this.scene.add(this.helpers.axes);
        }

        // Event listeners
        window.addEventListener('resize', () => this.onWindowResize(), false);

        // Start animation loop
        this.animate();

        return this;
    }

    /**
     * Setup lighting system
     */
    setupLighting() {
        const THREE = this.THREE;

        // Ambient light (base illumination)
        this.lights.ambient = new THREE.AmbientLight(0xffffff, 0.4);
        this.scene.add(this.lights.ambient);

        // Main directional light (sun)
        this.lights.directional = new THREE.DirectionalLight(0xffffff, 0.8);
        this.lights.directional.position.set(10, 15, 10);
        this.lights.directional.castShadow = this.config.enableShadows;

        if (this.config.enableShadows) {
            this.lights.directional.shadow.camera.top = 20;
            this.lights.directional.shadow.camera.bottom = -20;
            this.lights.directional.shadow.camera.left = -20;
            this.lights.directional.shadow.camera.right = 20;
            this.lights.directional.shadow.mapSize.width = 2048;
            this.lights.directional.shadow.mapSize.height = 2048;
        }

        this.scene.add(this.lights.directional);

        // Fill light (opposite side)
        this.lights.fill = new THREE.DirectionalLight(0x4488ff, 0.3);
        this.lights.fill.position.set(-10, 5, -10);
        this.scene.add(this.lights.fill);

        // Hemisphere light (sky/ground color gradient)
        this.lights.hemisphere = new THREE.HemisphereLight(0xffffff, 0x444444, 0.3);
        this.lights.hemisphere.position.set(0, 20, 0);
        this.scene.add(this.lights.hemisphere);
    }

    /**
     * Apply lighting preset
     */
    applyLightingPreset(preset) {
        this.currentPreset = preset;

        switch(preset) {
            case 'realistic':
                this.lights.ambient.intensity = 0.4;
                this.lights.directional.intensity = 0.8;
                this.lights.fill.intensity = 0.3;
                this.lights.hemisphere.intensity = 0.3;
                break;

            case 'bright':
                this.lights.ambient.intensity = 0.7;
                this.lights.directional.intensity = 0.6;
                this.lights.fill.intensity = 0.4;
                this.lights.hemisphere.intensity = 0.5;
                break;

            case 'dramatic':
                this.lights.ambient.intensity = 0.2;
                this.lights.directional.intensity = 1.2;
                this.lights.fill.intensity = 0.1;
                this.lights.hemisphere.intensity = 0.2;
                break;

            case 'flat':
                this.lights.ambient.intensity = 1.0;
                this.lights.directional.intensity = 0.2;
                this.lights.fill.intensity = 0.2;
                this.lights.hemisphere.intensity = 0.1;
                break;

            default: // 'default'
                this.lights.ambient.intensity = 0.4;
                this.lights.directional.intensity = 0.8;
                this.lights.fill.intensity = 0.3;
                this.lights.hemisphere.intensity = 0.3;
        }
    }

    /**
     * Load model from embedded data
     */
    async loadModel(loader, modelData, onProgress = null) {
        this.isLoading = true;
        this.loadingProgress = 0;
        const startTime = performance.now();

        try {
            // Simulate progress for parsing
            const progressInterval = setInterval(() => {
                if (this.loadingProgress < 90) {
                    this.loadingProgress += 5;
                    if (onProgress) onProgress(this.loadingProgress);
                }
            }, 50);

            // Parse the model
            const object = await new Promise((resolve, reject) => {
                try {
                    const parsed = loader.parse(modelData);
                    resolve(parsed);
                } catch (error) {
                    reject(error);
                }
            });

            clearInterval(progressInterval);
            this.loadingProgress = 100;
            if (onProgress) onProgress(100);

            // Process the loaded model
            this.processModel(object);

            // Track load time
            this.stats.loadTime = performance.now() - startTime;
            this.isLoading = false;

            return object;

        } catch (error) {
            this.isLoading = false;
            throw error;
        }
    }

    /**
     * Process loaded model (center, scale, add to scene)
     */
    processModel(object) {
        const THREE = this.THREE;

        // Calculate bounding box
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        // Calculate scale to fit in view
        const maxDim = Math.max(size.x, size.y, size.z);
        const targetSize = 5; // Target size in world units
        const scale = targetSize / maxDim;

        // Center and scale
        object.position.sub(center.multiplyScalar(scale));
        object.scale.multiplyScalar(scale);

        // Enable shadows
        if (this.config.enableShadows) {
            object.traverse((child) => {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;

                    // Track stats
                    if (child.geometry) {
                        this.stats.vertices += child.geometry.attributes.position?.count || 0;
                        this.stats.faces += child.geometry.index ?
                            child.geometry.index.count / 3 :
                            (child.geometry.attributes.position?.count || 0) / 3;
                    }
                }
            });
        }

        // Remove old model if exists
        if (this.model) {
            this.scene.remove(this.model);
        }

        this.model = object;
        this.scene.add(object);

        // Focus camera on model
        this.focusOnModel();
    }

    /**
     * Focus camera on loaded model
     */
    focusOnModel() {
        if (!this.model) return;

        const THREE = this.THREE;
        const box = new THREE.Box3().setFromObject(this.model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = this.camera.fov * (Math.PI / 180);
        const cameraDistance = Math.abs(maxDim / Math.sin(fov / 2)) * 1.5;

        this.camera.position.set(
            center.x + cameraDistance * 0.5,
            center.y + cameraDistance * 0.5,
            center.z + cameraDistance * 0.5
        );

        this.controls.target.copy(center);
        this.controls.update();
    }

    /**
     * Animation loop
     */
    animate() {
        requestAnimationFrame(() => this.animate());

        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }

    /**
     * Handle window resize
     */
    onWindowResize() {
        const container = document.getElementById(this.config.containerId);
        const width = container.clientWidth;
        const height = container.clientHeight;

        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    /**
     * Reset camera to default position
     */
    resetCamera() {
        this.camera.position.set(...this.config.cameraPosition);
        this.controls.target.set(0, 0, 0);
        this.controls.update();

        if (this.model) {
            this.focusOnModel();
        }
    }

    /**
     * Toggle wireframe mode
     */
    toggleWireframe(enabled = null) {
        if (!this.model) return;

        const isEnabled = enabled !== null ? enabled : !this.isWireframeEnabled();

        this.model.traverse((child) => {
            if (child.isMesh && child.material) {
                if (Array.isArray(child.material)) {
                    child.material.forEach(mat => mat.wireframe = isEnabled);
                } else {
                    child.material.wireframe = isEnabled;
                }
            }
        });

        return isEnabled;
    }

    /**
     * Check if wireframe is enabled
     */
    isWireframeEnabled() {
        if (!this.model) return false;

        let wireframeEnabled = false;
        this.model.traverse((child) => {
            if (child.isMesh && child.material) {
                const mat = Array.isArray(child.material) ? child.material[0] : child.material;
                if (mat.wireframe) wireframeEnabled = true;
            }
        });

        return wireframeEnabled;
    }

    /**
     * Toggle auto-rotation
     */
    toggleAutoRotate(enabled = null) {
        this.controls.autoRotate = enabled !== null ? enabled : !this.controls.autoRotate;
        return this.controls.autoRotate;
    }

    /**
     * Set background color
     */
    setBackgroundColor(color) {
        this.scene.background.set(color);
        this.config.backgroundColor = color;
    }

    /**
     * Toggle grid visibility
     */
    toggleGrid(visible = null) {
        if (this.helpers.grid) {
            this.helpers.grid.visible = visible !== null ? visible : !this.helpers.grid.visible;
            return this.helpers.grid.visible;
        }
        return false;
    }

    /**
     * Toggle fullscreen
     */
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
            return true;
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
            return false;
        }
    }

    /**
     * Take screenshot
     */
    screenshot(filename = 'terra-viewer-screenshot.png') {
        this.renderer.render(this.scene, this.camera);
        const dataURL = this.renderer.domElement.toDataURL('image/png');

        const link = document.createElement('a');
        link.download = filename;
        link.href = dataURL;
        link.click();

        return dataURL;
    }

    /**
     * Get viewer statistics
     */
    getStats() {
        return {
            ...this.stats,
            vertices: this.stats.vertices.toLocaleString(),
            faces: this.stats.faces.toLocaleString(),
            loadTime: `${this.stats.loadTime.toFixed(0)}ms`
        };
    }

    /**
     * Dispose viewer resources
     */
    dispose() {
        if (this.renderer) {
            this.renderer.dispose();
        }

        if (this.model) {
            this.model.traverse((child) => {
                if (child.geometry) child.geometry.dispose();
                if (child.material) {
                    if (Array.isArray(child.material)) {
                        child.material.forEach(mat => mat.dispose());
                    } else {
                        child.material.dispose();
                    }
                }
            });
        }
    }
}

/**
 * PLY-specific viewer extension
 */
export class PLYViewer extends TerraViewer {
    constructor(config = {}) {
        super({
            showAxes: true,
            enableShadows: false,
            ...config
        });

        this.pointSize = config.pointSize || 3;
        this.pointCloud = null;
    }

    /**
     * Process PLY point cloud
     */
    processModel(geometry) {
        const THREE = this.THREE;

        // Create material for point cloud
        const material = new THREE.PointsMaterial({
            size: this.pointSize,
            vertexColors: true,
            sizeAttenuation: true
        });

        // Create point cloud
        this.pointCloud = new THREE.Points(geometry, material);

        // Center the point cloud
        geometry.computeBoundingBox();
        const center = new THREE.Vector3();
        geometry.boundingBox.getCenter(center);
        this.pointCloud.position.sub(center);

        // Track stats
        this.stats.vertices = geometry.attributes.position.count;
        this.stats.faces = 0; // Point clouds don't have faces

        // Remove old model if exists
        if (this.model) {
            this.scene.remove(this.model);
        }

        this.model = this.pointCloud;
        this.scene.add(this.pointCloud);

        // Focus camera on model
        this.focusOnModel();
    }

    /**
     * Set point size
     */
    setPointSize(size) {
        this.pointSize = size;
        if (this.pointCloud && this.pointCloud.material) {
            this.pointCloud.material.size = size;
        }
    }

    /**
     * Get point count
     */
    getPointCount() {
        return this.stats.vertices;
    }
}

/**
 * Utility: Check WebGL support
 */
export function checkWebGLSupport() {
    try {
        const canvas = document.createElement('canvas');
        return !!(window.WebGLRenderingContext &&
            (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch(e) {
        return false;
    }
}

/**
 * Utility: Check browser compatibility
 */
export function checkBrowserCompatibility() {
    const ua = navigator.userAgent;
    const warnings = [];

    // Check for import map support
    if (!HTMLScriptElement.supports || !HTMLScriptElement.supports('importmap')) {
        warnings.push('Import maps not supported. Please update your browser.');
    }

    // Check for old Safari
    if (/Safari/.test(ua) && !/Chrome/.test(ua)) {
        const match = ua.match(/Version\/(\d+)/);
        if (match && parseInt(match[1]) < 16) {
            warnings.push('Safari 16.4+ required for import maps');
        }
    }

    return {
        supported: warnings.length === 0,
        warnings
    };
}
