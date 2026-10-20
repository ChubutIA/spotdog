import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SPOT DOG OS - IoT", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        header[data-testid="stHeader"] { display: none; }
        .block-container {
            padding-top: 0.4rem !important;
            padding-bottom: 0.4rem !important;
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
<!-- Librería oficial MQTT para IoT en tiempo real -->
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
<style>
    * { box-sizing: border-box; }
    body {
        background: radial-gradient(circle at top, #1e2530, #0d1015);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center;
        margin: 0;
        padding: 16px 18px;
        border-radius: 14px;
        border: 1px solid #2d3748;
        user-select: none;
    }
    h1 { letter-spacing: 3px; font-size: 21px; margin: 0 0 10px 0; color: #e2e8f0; }
    
    .conn-bar {
        margin-bottom: 12px;
        display: flex;
        justify-content: center;
        gap: 8px;
        align-items: center;
        flex-wrap: wrap;
        background: rgba(0,0,0,0.3);
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #2d3748;
    }
    select, input {
        background: #1a202c;
        border: 1px solid #4a5568;
        color: #00e5ff;
        padding: 6px 10px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 13px;
    }

    .status-bar {
        display: flex;
        justify-content: space-around;
        border-top: 1px solid #2d3748;
        border-bottom: 1px solid #2d3748;
        padding: 8px 0;
        margin-bottom: 12px;
    }
    .metric-label { font-size: 10px; color: #a0aec0; letter-spacing: 1px; }
    .metric-val { font-size: 14px; font-weight: bold; color: #00e5ff; margin-top: 2px; }

    .section-title {
        font-size: 10px;
        color: #718096;
        letter-spacing: 1.5px;
        margin: 6px 0 6px 0;
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
        padding: 8px 6px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 11px;
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

    .joysticks-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 12px 0 10px 0;
    }
    .joy-wrapper { display: flex; flex-direction: column; align-items: center; }
    .joy-label { font-size: 11px; color: #a0aec0; margin-bottom: 6px; }
    .joystick-zone {
        width: 126px;
        height: 126px;
        border: 2px solid rgba(0, 229, 255, 0.45);
        border-radius: 50%;
        position: relative;
        background: radial-gradient(circle, rgba(0,229,255,0.1) 0%, rgba(0,0,0,0.45) 100%);
        touch-action: none;
    }
    .stick {
        width: 40px;
        height: 40px;
        background: #00e5ff;
        border-radius: 50%;
        position: absolute;
        top: 41px;
        left: 41px;
        box-shadow: 0 0 16px #00e5ff;
        cursor: grab;
    }
    .gamepad-bar {
        margin-top: 6px;
        padding: 7px 10px;
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid #2d3748;
        border-radius: 6px;
        font-size: 12px;
        color: #a0aec0;
    }
</style>
</head>
<body>

    <h1>SPOT DOG OS <span style="font-size:12px; color:#00e5ff;">IoT CLOUD</span></h1>

    <!-- Selector de Modo: Nube IoT (4G / Cualquier Wi-Fi) o IP Local Directa -->
    <div class="conn-bar">
        <select id="conn-mode" onchange="toggleMode()">
            <option value="iot">🌐 Modo IoT Cloud (Datos Móviles / Cualquier Wi-Fi)</option>
            <option value="lan">📡 Modo Local Directo (Mismo Wi-Fi / AP del Perro)</option>
        </select>
        <input type="text" id="robot-id" value="spotdog_sergio_chubut" placeholder="ID del Perro" style="width:175px;">
        <input type="text" id="esp-ip" value="192.168.4.1" placeholder="IP Local" style="width:130px; display:none;">
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
            <div class="metric-label">CONEXIÓN</div>
            <div class="metric-val" id="st-ping" style="color:#ecc94b;">CONECTANDO...</div>
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
    const maxDist = 42;
    let mqttClient = null;

    function getTopicPrefix() {
        return "spotdog/" + document.getElementById('robot-id').value.trim();
    }

    // --- CONEXIÓN AL BROKER IoT (Funciona con Datos Móviles 4G/5G y cualquier Wi-Fi) ---
    function initMQTT() {
        const pingEl = document.getElementById('st-ping');
        // Broker público gratuito sobre WebSockets Seguros (WSS)
        mqttClient = mqtt.connect('wss://broker.emqx.io:8084/mqtt');

        mqttClient.on('connect', () => {
            pingEl.innerText = "ONLINE (IoT)";
            pingEl.style.color = "#48bb78";
            mqttClient.subscribe(getTopicPrefix() + "/status");
        });

        mqttClient.on('message', (topic, message) => {
            try {
                const data = JSON.parse(message.toString());
                if (data.mode) document.getElementById('st-mode').innerText = data.mode.toUpperCase();
                if (data.roll !== undefined) {
                    document.getElementById('st-imu').innerText = `${Math.round(data.roll)}° / ${Math.round(data.pitch)}°`;
                }
            } catch (e) {}
        });

        mqttClient.on('offline', () => {
            if (document.getElementById('conn-mode').value === 'iot') {
                pingEl.innerText = "RECONECTANDO";
                pingEl.style.color = "#f56565";
            }
        });
    }

    initMQTT();

    function toggleMode() {
        const mode = document.getElementById('conn-mode').value;
        document.getElementById('robot-id').style.display = (mode === 'iot') ? 'inline-block' : 'none';
        document.getElementById('esp-ip').style.display = (mode === 'lan') ? 'inline-block' : 'none';
        const pingEl = document.getElementById('st-ping');
        if (mode === 'lan') {
            pingEl.innerText = "MODO LAN";
            pingEl.style.color = "#00e5ff";
        } else if (mqttClient && mqttClient.connected) {
            pingEl.innerText = "ONLINE (IoT)";
            pingEl.style.color = "#48bb78";
        }
    }

    function flashButton(cmd) {
        const btn = document.getElementById('btn-' + cmd);
        if (btn) {
            btn.classList.add('active-btn');
            setTimeout(() => btn.classList.remove('active-btn'), 250);
        }
    }

    // Enviar Acción (Por IoT Cloud o por IP Local)
    async function sendAct(cmd) {
        document.getElementById('st-mode').innerText = cmd.toUpperCase();
        flashButton(cmd);
        const mode = document.getElementById('conn-mode').value;

        if (mode === 'iot' && mqttClient && mqttClient.connected) {
            mqttClient.publish(getTopicPrefix() + "/cmd", JSON.stringify({ type: "act", cmd: cmd }));
        } else {
            const ip = document.getElementById('esp-ip').value.trim();
            const base = ip.startsWith('http') ? ip : `http://${ip}`;
            try { await fetch(`${base}/r/act?cmd=${cmd}&act=${cmd}`, { method: 'GET', mode: 'no-cors' }); } catch (e) {}
        }
    }

    // Enviar Movimiento (Por IoT Cloud o por IP Local)
    async function sendMove(vx, vy, wz) {
        const mode = document.getElementById('conn-mode').value;

        if (mode === 'iot' && mqttClient && mqttClient.connected) {
            mqttClient.publish(getTopicPrefix() + "/cmd", JSON.stringify({ type: "move", vx: vx, vy: vy, wz: wz }));
        } else {
            const ip = document.getElementById('esp-ip').value.trim();
            const base = ip.startsWith('http') ? ip : `http://${ip}`;
            try {
                await fetch(`${base}/r/move?vx=${vx}&vy=${vy}&wz=${wz}&x=${vx}&y=${vy}&turn=${wz}`, {
                    method: 'GET', mode: 'no-cors'
                });
            } catch (e) {}
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

            if (btnJustPressed(gp, 0)) sendAct('stand');
            if (btnJustPressed(gp, 1)) sendAct('sit');
            if (btnJustPressed(gp, 2)) sendAct('lie');
            if (btnJustPressed(gp, 3)) sendAct('auto');
            if (btnJustPressed(gp, 4)) sendAct('wave');
            if (btnJustPressed(gp, 5)) sendAct('dance');
            if (btnJustPressed(gp, 8)) sendAct('relax');
            if (btnJustPressed(gp, 9)) sendAct('stop');
            if (btnJustPressed(gp, 12)) sendAct('bow');
            if (btnJustPressed(gp, 13)) sendAct('wiggle');
            if (btnJustPressed(gp, 14)) sendAct('shake');
        }
        requestAnimationFrame(pollGamepad);
    }
</script>
</body>
</html>
"""

components.html(html_code, height=660, scrolling=False)
