import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SPOT DOG OS - Sergio", layout="wide", initial_sidebar_state="collapsed")

# Eliminar márgenes y barra superior de Streamlit para que no corte el recuadro
st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none; }
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            max-width: 760px !important;
        }
        body, .stApp { background-color: #0b0e14; color: white; }
        iframe { border: none; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    * { box-sizing: border-box; }
    body {
        background: radial-gradient(circle at top, #1e2530, #0d1015);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        margin: 0;
        padding: 18px 20px;
        border-radius: 14px;
        border: 1px solid #2d3748;
        user-select: none;
    }
    h1 {
        letter-spacing: 3px;
        font-size: 22px;
        margin: 0 0 12px 0;
        color: #e2e8f0;
    }
    
    .ip-bar {
        margin-bottom: 12px;
        display: flex;
        justify-content: center;
        gap: 8px;
        align-items: center;
    }
    .ip-bar input {
        background: #1a202c;
        border: 1px solid #4a5568;
        color: #00e5ff;
        padding: 7px 12px;
        border-radius: 6px;
        text-align: center;
        font-family: monospace;
        font-size: 14px;
        width: 170px;
    }

    .status-bar {
        display: flex;
        justify-content: space-around;
        border-top: 1px solid #2d3748;
        border-bottom: 1px solid #2d3748;
        padding: 8px 0;
        margin-bottom: 14px;
    }
    .metric-label { font-size: 10px; color: #a0aec0; letter-spacing: 1px; }
    .metric-val { font-size: 14px; font-weight: bold; color: #00e5ff; margin-top: 2px; }

    .section-title {
        font-size: 10px;
        color: #718096;
        letter-spacing: 1.5px;
        margin: 8px 0 6px 0;
        text-transform: uppercase;
    }

    .btn-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 10px;
    }
    .btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: white;
        padding: 9px 6px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 11px;
        letter-spacing: 0.5px;
        cursor: pointer;
        transition: all 0.15s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
    }
    .btn:hover, .btn.active-btn {
        background: rgba(0, 229, 255, 0.22);
        border-color: #00e5ff;
        box-shadow: 0 0 12px rgba(0, 229, 255, 0.45);
        transform: scale(0.98);
    }
    .btn-stop {
        background: rgba(245, 101, 101, 0.15);
        border-color: #f56565;
        color: #feb2b2;
        grid-column: span 2;
    }
    .btn-stop:hover, .btn-stop.active-btn {
        background: rgba(245, 101, 101, 0.4);
        box-shadow: 0 0 12px rgba(245, 101, 101, 0.6);
    }
    .btn-auto { border-color: #48bb78; color: #9ae6b4; }

    /* Etiquetas de botones de PS4 */
    .ps-badge {
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
        background: rgba(0, 0, 0, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.15);
        font-family: monospace;
        color: #cbd5e0;
    }
    .ps-cross { color: #63b3ed; border-color: #63b3ed55; }
    .ps-circle { color: #fc8181; border-color: #fc818155; }
    .ps-square { color: #f687b3; border-color: #f687b355; }
    .ps-triangle { color: #68d391; border-color: #68d39155; }

    /* Joysticks */
    .joysticks-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 14px 0 12px 0;
    }
    .joy-wrapper { display: flex; flex-direction: column; align-items: center; }
    .joy-label { font-size: 11px; color: #a0aec0; margin-bottom: 6px; }
    .joystick-zone {
        width: 130px;
        height: 130px;
        border: 2px solid rgba(0, 229, 255, 0.45);
        border-radius: 50%;
        position: relative;
        background: radial-gradient(circle, rgba(0,229,255,0.1) 0%, rgba(0,0,0,0.45) 100%);
        touch-action: none;
    }
    .stick {
        width: 42px;
        height: 42px;
        background: #00e5ff;
        border-radius: 50%;
        position: absolute;
        top: 42px;
        left: 42px;
        box-shadow: 0 0 16px #00e5ff;
        cursor: grab;
    }
    .gamepad-bar {
        margin-top: 8px;
        padding: 8px 12px;
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid #2d3748;
        border-radius: 6px;
        font-size: 12px;
        color: #a0aec0;
    }
</style>
</head>
<body>

    <h1>SPOT DOG OS</h1>

    <div class="ip-bar">
        <input type="text" id="esp-ip" value="192.168.4.1" placeholder="IP o sergio.local">
        <button class="btn" style="flex-direction:row; padding: 8px 14px;" onclick="checkStatus()">CONECTAR</button>
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

    <div class="section-title">Posturas y Modos</div>
    <div class="btn-grid">
        <button class="btn" id="btn-stand" onclick="sendAct('stand')">
            <span>DE PIE</span>
            <span class="ps-badge ps-cross">✖ Cruz</span>
        </button>
        <button class="btn" id="btn-sit" onclick="sendAct('sit')">
            <span>SENTADO</span>
            <span class="ps-badge ps-circle">● Círculo</span>
        </button>
        <button class="btn" id="btn-lie" onclick="sendAct('lie')">
            <span>ACOSTADO</span>
            <span class="ps-badge ps-square">■ Cuadrado</span>
        </button>
        <button class="btn btn-auto" id="btn-auto" onclick="sendAct('auto')">
            <span>EXPLORAR (AUTO)</span>
            <span class="ps-badge ps-triangle">▲ Triángulo</span>
        </button>
    </div>

    <div class="section-title">Animaciones y Control</div>
    <div class="btn-grid">
        <button class="btn" id="btn-wave" onclick="sendAct('wave')">
            <span>SALUDAR</span>
            <span class="ps-badge">L1</span>
        </button>
        <button class="btn" id="btn-dance" onclick="sendAct('dance')">
            <span>BAILAR</span>
            <span class="ps-badge">R1</span>
        </button>
        <button class="btn" id="btn-shake" onclick="sendAct('shake')">
            <span>PATITA</span>
            <span class="ps-badge">⬅ D-Pad Izq</span>
        </button>
        <button class="btn" id="btn-bow" onclick="sendAct('bow')">
            <span>REVERENCIA</span>
            <span class="ps-badge">⬆ D-Pad Arr</span>
        </button>
        <button class="btn" id="btn-wiggle" onclick="sendAct('wiggle')">
            <span>MENEAR</span>
            <span class="ps-badge">⬇ D-Pad Abj</span>
        </button>
        <button class="btn" id="btn-relax" onclick="sendAct('relax')">
            <span>RELAJAR</span>
            <span class="ps-badge">SHARE</span>
        </button>
        <button class="btn btn-stop" id="btn-stop" onclick="sendAct('stop')">
            <span>🚨 STOP (KILL SERVOS)</span>
            <span class="ps-badge" style="color:#feb2b2; border-color:#f56565;">OPTIONS</span>
        </button>
    </div>

    <div class="joysticks-container">
        <div class="joy-wrapper">
            <div class="joy-label">AVANZAR / LATERAL (Stick Izq)</div>
            <div class="joystick-zone" id="zone-left">
                <div class="stick" id="stick-left"></div>
            </div>
        </div>
        <div class="joy-wrapper">
            <div class="joy-label">GIRAR (Stick Der)</div>
            <div class="joystick-zone" id="zone-right">
                <div class="stick" id="stick-right"></div>
            </div>
        </div>
    </div>

    <div class="gamepad-bar" id="gp-status">
        🎮 DualShock 4: Conectá el mando y presioná cualquier botón
    </div>

<script>
    let moveState = { vx: 0, vy: 0, wz: 0 };
    const maxDist = 44;

    function getBaseUrl() {
        const ip = document.getElementById('esp-ip').value.trim();
        return ip.startsWith('http') ? ip : `http://${ip}`;
    }

    function flashButton(cmd) {
        const btn = document.getElementById('btn-' + cmd);
        if (btn) {
            btn.classList.add('active-btn');
            setTimeout(() => btn.classList.remove('active-btn'), 250);
        }
    }

    async function sendAct(cmd) {
        document.getElementById('st-mode').innerText = cmd.toUpperCase();
        flashButton(cmd);
        const base = getBaseUrl();
        try {
            await fetch(`${base}/r/act?cmd=${cmd}&act=${cmd}`, { method: 'GET', mode: 'no-cors' });
        } catch (e) {}
    }

    async function sendMove(vx, vy, wz) {
        const base = getBaseUrl();
        try {
            await fetch(`${base}/r/move?vx=${vx}&vy=${vy}&wz=${wz}&x=${vx}&y=${vy}&turn=${wz}`, {
                method: 'GET', mode: 'no-cors'
            });
        } catch (e) {}
    }

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
            pingEl.innerText = "LISTO (LAN)";
            pingEl.style.color = "#ecc94b";
        }
    }

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

            const normX = +(px / maxDist).toFixed(2);
            const normY = +(-py / maxDist).toFixed(2);
            onMoveCallback(normX, normY);
        }
    }

    setupJoystick('zone-left', 'stick-left', (x, y) => { moveState.vy = x; moveState.vx = y; });
    setupJoystick('zone-right', 'stick-right', (x, y) => { moveState.wz = x; });

    setInterval(() => {
        if (moveState.vx !== 0 || moveState.vy !== 0 || moveState.wz !== 0) {
            sendMove(moveState.vx, moveState.vy, moveState.wz);
        }
    }, 180);

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

            if (btnJustPressed(gp, 0)) sendAct('stand');   // Cruz (X)
            if (btnJustPressed(gp, 1)) sendAct('sit');     // Círculo
            if (btnJustPressed(gp, 2)) sendAct('lie');     // Cuadrado
            if (btnJustPressed(gp, 3)) sendAct('auto');    // Triángulo
            if (btnJustPressed(gp, 4)) sendAct('wave');    // L1
            if (btnJustPressed(gp, 5)) sendAct('dance');   // R1
            if (btnJustPressed(gp, 8)) sendAct('relax');   // Share
            if (btnJustPressed(gp, 9)) sendAct('stop');    // Options
            if (btnJustPressed(gp, 12)) sendAct('bow');    // D-Pad Arriba
            if (btnJustPressed(gp, 13)) sendAct('wiggle'); // D-Pad Abajo
            if (btnJustPressed(gp, 14)) sendAct('shake');  // D-Pad Izq
        }
        requestAnimationFrame(pollGamepad);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=650, scrolling=False)
