import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SPOT DOG OS - Sergio", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        .block-container { padding-top: 0.8rem; padding-bottom: 0rem; max-width: 750px; }
        body { background-color: #0d1015; color: white; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        background: radial-gradient(circle at top, #1e2530, #0d1015);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        margin: 0;
        padding: 15px;
        border-radius: 12px;
        user-select: none;
    }
    h1 { letter-spacing: 3px; font-size: 24px; margin: 5px 0 12px 0; color: #e2e8f0; }
    
    .ip-bar { margin-bottom: 15px; display: flex; justify-content: center; gap: 8px; align-items: center; }
    .ip-bar input {
        background: #1a202c; border: 1px solid #4a5568; color: #00e5ff;
        padding: 7px 10px; border-radius: 6px; text-align: center; font-family: monospace; width: 150px;
    }

    .status-bar {
        display: flex; justify-content: space-around;
        border-top: 1px solid #2d3748; border-bottom: 1px solid #2d3748;
        padding: 10px 0; margin-bottom: 18px;
    }
    .metric-label { font-size: 10px; color: #a0aec0; letter-spacing: 1px; }
    .metric-val { font-size: 15px; font-weight: bold; color: #00e5ff; margin-top: 3px; }

    .section-title { font-size: 11px; color: #718096; letter-spacing: 1.5px; margin: 10px 0 6px 0; text-transform: uppercase; }

    .btn-grid {
        display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px;
    }
    .btn {
        background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.2);
        color: white; padding: 10px 6px; border-radius: 7px; font-weight: bold;
        font-size: 11px; letter-spacing: 0.8px; cursor: pointer; transition: 0.15s;
    }
    .btn:hover, .btn:active {
        background: rgba(0, 229, 255, 0.2); border-color: #00e5ff;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.4);
    }
    .btn-stop {
        background: rgba(245, 101, 101, 0.2); border-color: #f56565; color: #feb2b2;
        grid-column: span 2;
    }
    .btn-stop:hover { background: rgba(245, 101, 101, 0.45); box-shadow: 0 0 12px rgba(245, 101, 101, 0.6); }
    .btn-auto { border-color: #48bb78; color: #9ae6b4; }

    /* Doble Joystick */
    .joysticks-container {
        display: flex; justify-content: space-around; align-items: center; margin: 18px 0 10px 0;
    }
    .joy-wrapper { display: flex; flex-direction: column; align-items: center; }
    .joy-label { font-size: 11px; color: #a0aec0; margin-bottom: 6px; }
    .joystick-zone {
        width: 140px; height: 140px; border: 2px solid rgba(0, 229, 255, 0.45);
        border-radius: 50%; position: relative;
        background: radial-gradient(circle, rgba(0,229,255,0.1) 0%, rgba(0,0,0,0.45) 100%);
        touch-action: none;
    }
    .stick {
        width: 44px; height: 44px; background: #00e5ff; border-radius: 50%;
        position: absolute; top: 48px; left: 48px; box-shadow: 0 0 18px #00e5ff;
        cursor: grab;
    }
    .gamepad-bar {
        margin-top: 12px; padding: 8px; background: rgba(0,0,0,0.3);
        border-radius: 6px; font-size: 12px; color: #a0aec0;
    }
</style>
</head>
<body>

    <h1>SPOT DOG OS</h1>

    <div class="ip-bar">
        <input type="text" id="esp-ip" value="192.168.4.1" placeholder="IP o sergio.local">
        <button class="btn" onclick="checkStatus()">CONECTAR</button>
    </div>

    <div class="status-bar">
        <div>
            <div class="metric-label">ESTADO</div>
            <div class="metric-val" id="st-mode">IDLE</div>
        </div>
        <div>
            <div class="metric-label">MARCHA</div>
            <div class="metric-val" id="st-gait">TROTE</div>
        </div>
        <div>
            <div class="metric-label">IMU (R/P)</div>
            <div class="metric-val" id="st-imu">0° / 0°</div>
        </div>
        <div>
            <div class="metric-label">PING</div>
            <div class="metric-val" id="st-ping" style="color:#f56565;">OFF</div>
        </div>
    </div>

    <!-- Posturas Principales y Modos (de tu diseño original + Sergio) -->
    <div class="section-title">Posturas y Modos</div>
    <div class="btn-grid">
        <button class="btn" onclick="sendAct('stand')">DE PIE</button>
        <button class="btn" onclick="sendAct('sit')">SENTADO</button>
        <button class="btn" onclick="sendAct('lie')">ACOSTADO (REPOSO)</button>
        <button class="btn btn-auto" onclick="sendAct('auto')">EXPLORAR (AUTO)</button>
    </div>

    <!-- Acciones y Animaciones -->
    <div class="section-title">Animaciones y Control</div>
    <div class="btn-grid">
        <button class="btn" onclick="sendAct('wave')">SALUDAR</button>
        <button class="btn" onclick="sendAct('shake')">PATITA</button>
        <button class="btn" onclick="sendAct('dance')">BAILAR</button>
        <button class="btn" onclick="sendAct('bow')">REVERENCIA</button>
        <button class="btn" onclick="sendAct('wiggle')">MENEAR</button>
        <button class="btn" onclick="sendAct('relax')">RELAJAR</button>
        <button class="btn btn-stop" onclick="sendAct('stop')">🚨 STOP (KILL SERVOS)</button>
    </div>

    <!-- Joysticks Izquierdo (Traslación) y Derecho (Giro) -->
    <div class="joysticks-container">
        <div class="joy-wrapper">
            <div class="joy-label">AVANZAR / LATERAL (L-Stick)</div>
            <div class="joystick-zone" id="zone-left">
                <div class="stick" id="stick-left"></div>
            </div>
        </div>
        <div class="joy-wrapper">
            <div class="joy-label">GIRAR (R-Stick)</div>
            <div class="joystick-zone" id="zone-right">
                <div class="stick" id="stick-right"></div>
            </div>
        </div>
    </div>

    <div class="gamepad-bar" id="gp-status">
        🎮 DualShock 4: Conectá el mando por Bluetooth/USB a tu PC o Celular y tocá un botón
    </div>

<script>
    let moveState = { vx: 0, vy: 0, wz: 0 };
    const maxDist = 48;

    function getBaseUrl() {
        const ip = document.getElementById('esp-ip').value.trim();
        return ip.startsWith('http') ? ip : `http://${ip}`;
    }

    // 1. Enviar acciones (/r/act y /r/voice como respaldo)
    async function sendAct(cmd) {
        document.getElementById('st-mode').innerText = cmd.toUpperCase();
        const base = getBaseUrl();
        try {
            // Llama al endpoint /r/act de SergioElPerro (pasando cmd tanto en query como JSON por compatibilidad)
            await fetch(`${base}/r/act?cmd=${cmd}&act=${cmd}`, { method: 'GET', mode: 'no-cors' });
        } catch (e) {}
    }

    // 2. Enviar movimiento (/r/move)
    async function sendMove(vx, vy, wz) {
        const base = getBaseUrl();
        try {
            // Envía velocidades X (adelante/atrás), Y (lateral) y Z/Yaw (giro)
            await fetch(`${base}/r/move?vx=${vx}&vy=${vy}&wz=${wz}&x=${vx}&y=${vy}&turn=${wz}`, {
                method: 'GET', mode: 'no-cors'
            });
        } catch (e) {}
    }

    // 3. Consultar telemetría (/r/status)
    async function checkStatus() {
        const base = getBaseUrl();
        const pingEl = document.getElementById('st-ping');
        const t0 = performance.now();
        try {
            const res = await fetch(`${base}/r/status`);
            const data = await res.json();
            const dt = Math.round(performance.now() - t0);
            pingEl.innerText = dt + " ms";
            pingEl.style.color = "#48bb78";
            if (data.mode || data.state) document.getElementById('st-mode').innerText = (data.mode || data.state).toUpperCase();
            if (data.roll !== undefined) document.getElementById('st-imu').innerText = `${Math.round(data.roll)}° / ${Math.round(data.pitch)}°`;
        } catch (e) {
            pingEl.innerText = "ONLINE (NO-CORS)";
            pingEl.style.color = "#ecc94b";
        }
    }

    // Configurar Joysticks Táctiles
    function setupJoystick(zoneId, stickId, onMoveCallback) {
        const zone = document.getElementById(zoneId);
        const stick = document.getElementById(stickId);
        let dragging = false;

        zone.addEventListener('pointerdown', (e) => { dragging = true; updatePos(e); });
        window.addEventListener('pointermove', (e) => { if (dragging) updatePos(e); });
        window.addEventListener('pointerup', () => {
            if (!dragging) return;
            dragging = false;
            stick.style.transform = `translate(0px, 0px)`;
            onMoveCallback(0, 0);
            sendMove(moveState.vx, moveState.vy, moveState.wz);
        });

        function updatePos(e) {
            const rect = zone.getBoundingClientRect();
            const dx = e.clientX - (rect.left + rect.width / 2);
            const dy = e.clientY - (rect.top + rect.height / 2);
            const dist = Math.min(Math.hypot(dx, dy), maxDist);
            const angle = Math.atan2(dy, dx);
            const px = Math.cos(angle) * dist;
            const py = Math.sin(angle) * dist;
            stick.style.transform = `translate(${px}px, ${py}px)`;

            // Valores de -1.00 a 1.00
            const normX = +(px / maxDist).toFixed(2);
            const normY = +(-py / maxDist).toFixed(2);
            onMoveCallback(normX, normY);
        }
    }

    setupJoystick('zone-left', 'stick-left', (x, y) => { moveState.vy = x; moveState.vx = y; });
    setupJoystick('zone-right', 'stick-right', (x, y) => { moveState.wz = x; });

    // Loop de envío cada 180 ms (Respeta el watchdog de 0,7s de SergioElPerro sin saturar el Wi-Fi)
    setInterval(() => {
        if (moveState.vx !== 0 || moveState.vy !== 0 || moveState.wz !== 0) {
            sendMove(moveState.vx, moveState.vy, moveState.wz);
        }
    }, 180);

    // --- Integración DualShock 4 (Gamepad API) ---
    let lastBtn = {};
    window.addEventListener("gamepadconnected", (e) => {
        document.getElementById('gp-status').innerHTML = `🟢 <b>DualShock 4 Activo:</b> ${e.gamepad.id}`;
        requestAnimationFrame(pollGamepad);
    });

    function btnJustPressed(gp, idx) {
        const pressed = gp.buttons[idx]?.pressed;
        const wasPressed = lastBtn[idx] || false;
        lastBtn[idx] = pressed;
        return pressed && !wasPressed;
    }

    function pollGamepad() {
        const gp = navigator.getGamepads()[0];
        if (gp) {
            const deadzone = 0.12;
            let lx = Math.abs(gp.axes[0]) > deadzone ? +gp.axes[0].toFixed(2) : 0;
            let ly = Math.abs(gp.axes[1]) > deadzone ? +(-gp.axes[1]).toFixed(2) : 0;
            let rx = Math.abs(gp.axes[2]) > deadzone ? +gp.axes[2].toFixed(2) : 0;

            moveState.vx = ly;
            moveState.vy = lx;
            moveState.wz = rx;

            document.getElementById('stick-left').style.transform = `translate(${lx * maxDist}px, ${-ly * maxDist}px)`;
            document.getElementById('stick-right').style.transform = `translate(${rx * maxDist}px, 0px)`;

            // Mapeo de Botones de PS4 a las acciones de SergioElPerro
            if (btnJustPressed(gp, 0)) sendAct('stand');   // Cruz (X) -> De pie
            if (btnJustPressed(gp, 1)) sendAct('sit');     // Círculo -> Sentado
            if (btnJustPressed(gp, 2)) sendAct('lie');     // Cuadrado -> Acostado
            if (btnJustPressed(gp, 3)) sendAct('auto');    // Triángulo -> Modo Autónomo
            if (btnJustPressed(gp, 4)) sendAct('wave');    // L1 -> Saludar
            if (btnJustPressed(gp, 5)) sendAct('dance');   // R1 -> Bailar
            if (btnJustPressed(gp, 8)) sendAct('relax');   // Share -> Relajar
            if (btnJustPressed(gp, 9)) sendAct('stop');    // Options -> STOP Emergencia
            if (btnJustPressed(gp, 12)) sendAct('bow');    // D-Pad Arriba -> Reverencia
            if (btnJustPressed(gp, 13)) sendAct('wiggle'); // D-Pad Abajo -> Menear
            if (btnJustPressed(gp, 14)) sendAct('shake');  // D-Pad Izq -> Patita
        }
        requestAnimationFrame(pollGamepad);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=680)
