// ====================== GLOBAL VARIABLES ======================
let currentDS = 'stack_array';
let bstTree = null;

let hanoiTowers = [[], [], []];
let currentHanoiMoves = [];
let hanoiInterval = null;
let isHanoiRunning = false;
const canvas = document.getElementById('graph-canvas');
const ctx = canvas ? canvas.getContext('2d') : null;

// ====================== BIG-O COMPLEXITY MAP ======================
// Maps every DS + operation combination to { time, space } Big-O strings.
const BIG_O = {
    // ---- Stacks & Queues ----
    stack_array: {
        push:  { time: 'O(1)', space: 'O(1)', note: 'Amortised O(1) for dynamic array' },
        pop:   { time: 'O(1)', space: 'O(1)' },
        peek:  { time: 'O(1)', space: 'O(1)' },
        info:  { time: 'O(1)', space: 'O(1)' },
    },
    stack_linked: {
        push:  { time: 'O(1)', space: 'O(1)' },
        pop:   { time: 'O(1)', space: 'O(1)' },
        peek:  { time: 'O(1)', space: 'O(1)' },
        info:  { time: 'O(1)', space: 'O(1)' },
    },
    queue_array: {
        push:  { time: 'O(1)', space: 'O(1)', note: 'Amortised; O(n) worst on resize' },
        pop:   { time: 'O(n)', space: 'O(1)', note: 'Shift on plain array; O(1) with circular buffer' },
        peek:  { time: 'O(1)', space: 'O(1)' },
        info:  { time: 'O(1)', space: 'O(1)' },
    },
    queue_linked: {
        push:  { time: 'O(1)', space: 'O(1)' },
        pop:   { time: 'O(1)', space: 'O(1)' },
        peek:  { time: 'O(1)', space: 'O(1)' },
        info:  { time: 'O(1)', space: 'O(1)' },
    },
    // ---- Linked Lists ----
    singly_linked: {
        insert_beginning: { time: 'O(1)', space: 'O(1)' },
        insert_end:       { time: 'O(n)', space: 'O(1)', note: 'O(1) if tail pointer maintained' },
        insert_position:  { time: 'O(n)', space: 'O(1)' },
        delete_value:     { time: 'O(n)', space: 'O(1)' },
        delete_position:  { time: 'O(n)', space: 'O(1)' },
        search:           { time: 'O(n)', space: 'O(1)' },
        info:             { time: 'O(1)', space: 'O(1)' },
    },
    doubly_linked: {
        insert_beginning: { time: 'O(1)', space: 'O(1)' },
        insert_end:       { time: 'O(1)', space: 'O(1)', note: 'O(1) with head + tail pointers' },
        insert_position:  { time: 'O(n)', space: 'O(1)' },
        delete_value:     { time: 'O(n)', space: 'O(1)' },
        delete_position:  { time: 'O(n)', space: 'O(1)' },
        search:           { time: 'O(n)', space: 'O(1)' },
        info:             { time: 'O(1)', space: 'O(1)' },
    },
    // ---- Sorting ----
    sorting: {
        bubble:     { time: 'O(n²)',      best: 'O(n)',      space: 'O(1)' },
        selection:  { time: 'O(n²)',      best: 'O(n²)',     space: 'O(1)' },
        insertion:  { time: 'O(n²)',      best: 'O(n)',      space: 'O(1)' },
        merge:      { time: 'O(n log n)', best: 'O(n log n)',space: 'O(n)' },
        quick:      { time: 'O(n²)',      best: 'O(n log n)',space: 'O(log n)', note: 'Avg O(n log n); worst O(n²) on sorted input' },
        heap:       { time: 'O(n log n)', best: 'O(n log n)',space: 'O(1)' },
        counting:   { time: 'O(n + k)',   best: 'O(n + k)',  space: 'O(k)', note: 'k = range of values' },
        radix:      { time: 'O(nk)',      best: 'O(nk)',     space: 'O(n + k)', note: 'k = number of digits' },
    },
    // ---- Searching ----
    searching: {
        linear: { time: 'O(n)',      best: 'O(1)',      space: 'O(1)' },
        binary: { time: 'O(log n)',  best: 'O(1)',      space: 'O(1)', note: 'Requires sorted array' },
        jump:   { time: 'O(√n)',     best: 'O(1)',      space: 'O(1)', note: 'Requires sorted array' },
    },
    // ---- BST ----
    bst: {
        insert: { time: 'O(log n)', worst: 'O(n)', space: 'O(1)', note: 'O(n) on unbalanced/degenerate tree' },
        search: { time: 'O(log n)', worst: 'O(n)', space: 'O(1)' },
        delete: { time: 'O(log n)', worst: 'O(n)', space: 'O(1)' },
    },
    // ---- Graph ----
    graph: {
        bfs:            { time: 'O(V + E)', space: 'O(V)', note: 'V = vertices, E = edges' },
        dfs:            { time: 'O(V + E)', space: 'O(V)' },
        shortest_path:  { time: 'O((V + E) log V)', space: 'O(V)', note: "Dijkstra's with min-heap" },
        add_edge:       { time: 'O(1)',     space: 'O(1)' },
    },
    // ---- Hash Table ----
    hash_table: {
        insert: { time: 'O(1)', worst: 'O(n)', space: 'O(1)', note: 'Worst case on all keys colliding' },
        get:    { time: 'O(1)', worst: 'O(n)', space: 'O(1)' },
        delete: { time: 'O(1)', worst: 'O(n)', space: 'O(1)' },
    },
    // ---- Hanoi ----
    hanoi: {
        solve: { time: 'O(2ⁿ)', space: 'O(n)', note: 'Exactly 2ⁿ − 1 moves required' },
    },
};

/**
 * Builds a compact HTML badge strip for a Big-O entry.
 * @param {object} complexity  - entry from BIG_O map
 * @param {number} measuredMs  - measured wall-clock time in ms (optional)
 */
function buildComplexityHTML(complexity, measuredMs) {
    if (!complexity) return '';

    const badge = (label, value, color) =>
        `<span style="
            display:inline-block; padding:3px 10px; border-radius:20px;
            background:${color}22; border:1.5px solid ${color};
            color:${color}; font-weight:700; font-size:0.82em;
            margin:2px 3px; font-family:monospace; letter-spacing:0.03em;">
            ${label}: ${value}
        </span>`;

    let html = `<div style="margin-top:10px; line-height:2;">`;
    html += badge('Time (avg)', complexity.time, '#667eea');
    if (complexity.best)  html += badge('Best',  complexity.best,  '#4caf50');
    if (complexity.worst) html += badge('Worst', complexity.worst, '#e53935');
    html += badge('Space', complexity.space, '#ff9800');

    if (measuredMs !== undefined) {
        html += badge('Measured', `${measuredMs} ms`, '#00bcd4');
    }

    if (complexity.note) {
        html += `<div style="margin-top:6px; font-size:0.8em; color:#888; font-style:italic;">
            💡 ${complexity.note}</div>`;
    }

    html += `</div>`;
    return html;
}

/**
 * Writes complexity + timing into a target element.
 * @param {string} elementId   - DOM id to update
 * @param {object} complexity  - BIG_O entry
 * @param {number} measuredMs  - measured ms
 * @param {string} label       - operation label shown as header
 */
function renderPerformancePanel(elementId, complexity, measuredMs, label) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.innerHTML = `
        <strong style="font-size:0.95em; color:#34495e;">⏱ ${label}</strong>
        ${buildComplexityHTML(complexity, measuredMs)}
    `;
}

// ====================== TAB SWITCHING ======================
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));

    const tabElement = document.getElementById(`${tabName}-tab`);
    if (tabElement) tabElement.classList.add('active');

    const activeBtn = Array.from(document.querySelectorAll('.tab-btn'))
                        .find(btn => btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(tabName));
    if (activeBtn) activeBtn.classList.add('active');

    if (tabName === 'ds') updateDSOperations();
    if (tabName === 'graph') {
        setTimeout(() => {
            if (typeof initGraphCanvas === 'function') initGraphCanvas();
            if (typeof drawGraph === 'function') drawGraph();
        }, 300);
    }
    if (tabName === 'hashtable') {
        setTimeout(() => {
            fetch('/api/ds/hash_table/display')
                .then(res => res.json())
                .then(data => {
                    if (data.success) renderHashTable(data.data);
                });
        }, 300);
    }
}

// ====================== DYNAMIC OPERATIONS PANEL ======================
function updateDSOperations() {
    currentDS = document.getElementById('ds-select').value;
    const panel = document.getElementById('ds-operations');

    let html = `<div class="operation-buttons">`;

    if (currentDS.includes('stack') || currentDS.includes('queue')) {
        html += `
            <button class="btn-operation" onclick="performDSOperation('push')">Push / Enqueue</button>
            <button class="btn-operation" onclick="performDSOperation('pop')">Pop / Dequeue</button>
            <button class="btn-operation" onclick="performDSOperation('peek')">Peek</button>
            <button class="btn-operation" onclick="performDSOperation('info')">Info</button>
        `;
    } else if (currentDS.includes('linked')) {
        html += `
            <button class="btn-operation" onclick="performDSOperation('insert_beginning')">Insert Beginning</button>
            <button class="btn-operation" onclick="performDSOperation('insert_end')">Insert End</button>
            <button class="btn-operation" onclick="performDSOperation('insert_position')">Insert at Position</button>
            <button class="btn-operation" onclick="performDSOperation('delete_value')">Delete by Value</button>
            <button class="btn-operation" onclick="performDSOperation('delete_position')">Delete at Position</button>
            <button class="btn-operation" onclick="performDSOperation('search')">Search</button>
            <button class="btn-operation" onclick="performDSOperation('info')">Info</button>
        `;
    }else if (currentDS.includes('heap')) {
    html += `
        <button class="btn-operation" onclick="heapOperation('${currentDS}', 'push')">Insert</button>
        <button class="btn-operation" onclick="heapOperation('${currentDS}', 'pop')">Extract</button>
        <button class="btn-operation" onclick="heapOperation('${currentDS}', 'peek')">Peek</button>
    `;
}

    html += `<br><input type="text" id="ds-input" placeholder="Value" style="width:180px; margin-top:10px;">`;
    html += `<input type="number" id="position-input" placeholder="Position" style="width:100px; margin-left:8px; margin-top:10px;">`;
    html += `</div>`;
    panel.innerHTML = html;
}

async function performDSOperation(operation) {
    const value = document.getElementById('ds-input')?.value.trim();
    const position = document.getElementById('position-input')?.value.trim();

    let endpoint = '';
    let body = {};

    switch(operation) {
        case 'push':
            endpoint = currentDS.includes('queue') ? '/enqueue' : '/push';
            body = { value };
            break;
        case 'pop':
            endpoint = currentDS.includes('queue') ? '/dequeue' : '/pop';
            break;
        case 'peek':
            endpoint = '/peek';
            break;
        case 'insert_beginning':
            endpoint = '/push';
            body = { value };
            break;
        case 'insert_end':
            endpoint = '/insert_end';
            body = { value };
            break;
        case 'insert_position':
            if (!value || !position) return showMessage("Value and Position required", "error");
            endpoint = '/insert_position';
            body = { value, position: parseInt(position) };
            break;
        case 'delete_value':
            endpoint = '/delete';
            body = { value };
            break;
        case 'delete_position':
            if (!position) return showMessage("Position required", "error");
            endpoint = '/delete_at_position';
            body = { position: parseInt(position) };
            break;
        case 'search':
            endpoint = '/search';
            body = { value };
            break;
        case 'info':
            showStructureInfo();
            return;
    }

    try {
        const start = performance.now();

        const res = await fetch(`/api/ds/${currentDS}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: Object.keys(body).length ? JSON.stringify(body) : null
        });

        const data = await res.json();
        const measuredMs = (performance.now() - start).toFixed(2);

        if (data.success) {
            updateDSVisualization(data.data || []);
            showMemoryUsage();

            // Resolve complexity: use exact DS key, fall back to generic ds type
            const dsKey = BIG_O[currentDS] ? currentDS
                        : currentDS.includes('stack') ? 'stack_array'
                        : currentDS.includes('queue') ? 'queue_array'
                        : currentDS.includes('doubly') ? 'doubly_linked'
                        : 'singly_linked';

            const complexity = BIG_O[dsKey]?.[operation];
            renderPerformancePanel(
                'ds-performance',
                complexity,
                measuredMs,
                `${operation.replace(/_/g, ' ').toUpperCase()} on ${currentDS}`
            );
        } else {
            showMessage(data.error || "Operation failed", "error");
        }
    } catch (err) {
        showMessage("Server connection error. Is Flask running?", "error");
    }
}

function updateDSVisualization(data) {
    const viz = document.getElementById('ds-visualization');
    if (!data || data.length === 0) {
        viz.innerHTML = '<p style="color:#999; padding:30px;">Structure is empty</p>';
        return;
    }
    viz.innerHTML = data.map(item => `<div class="data-item">${item}</div>`).join('');
}

// ====================== MEMORY USAGE ======================
async function showMemoryUsage() {
    try {
        const res = await fetch(`/api/ds/${currentDS}/memory`);
        const data = await res.json();

        if (data.success) {
            const mem = data.memory;
            const existing = document.getElementById('ds-performance').innerHTML;
            document.getElementById('ds-performance').innerHTML = existing + `
                <div style="margin-top:8px; font-size:0.85em; color:#555;">
                    <strong>Memory:</strong> ${mem.elements} elements | ${mem.memory_kb} KB (${mem.memory_bytes} bytes)
                </div>
            `;
        }
    } catch(e) {
        console.warn("Memory tracking unavailable");
    }
}

async function showStructureInfo() {
    try {
        const res = await fetch(`/api/ds/${currentDS}/display`);
        const data = await res.json();

        if (data.success) {
            const size = data.data.length;
            const isEmpty = size === 0;
            showMessage(`Size: ${size} | Empty: ${isEmpty}`, "success");
        }
    } catch(e) {
        showMessage("Could not fetch structure info", "error");
    }
}

// ====================== SORTING ======================
async function executeSortWithMetrics() {
    const algo = document.getElementById('sort-algorithm').value;
    const inputStr = document.getElementById('sort-input').value.trim();

    if (!inputStr) return showMessage("Please enter numbers", "error");

    const arr = inputStr.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));

    try {
        const start = performance.now();

        const res = await fetch('/api/algorithms/sort_with_metrics', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({algorithm: algo, data: arr})
        });
        const data = await res.json();
        const measuredMs = (performance.now() - start).toFixed(2);

        if (data.success) {
            const complexity = BIG_O.sorting[algo] || BIG_O.sorting[algo.toLowerCase()];

            document.getElementById('sort-result').innerHTML = `
                <div class="success-message">
                    <strong>${algo.toUpperCase()} SORT</strong><br><br>
                    Sorted: [${data.sorted.join(', ')}]<br><br>
                    Comparisons: ${data.metrics.comparisons} | Swaps: ${data.metrics.swaps}<br>
                    Server time: ${data.metrics.time_taken} ms
                    ${buildComplexityHTML(complexity, measuredMs)}
                </div>`;
            visualizeArray(arr, data.sorted);
        }
    } catch(e) {
        showMessage("Sorting failed", "error");
    }
}

function visualizeArray(original, sorted) {
    const container = document.getElementById('array-container');
    container.innerHTML = original.map((num) => `
        <div class="array-bar" style="height: ${Math.max(num * 4, 20)}px;" title="${num}">
            ${num}
        </div>
    `).join('');
}

// ====================== SEARCHING ======================
async function executeSearch() {
    const algo = document.getElementById('search-algorithm').value;
    const input = document.getElementById('search-input').value.trim();
    const target = parseInt(document.getElementById('search-target').value);

    if (!input || isNaN(target)) return showMessage("Invalid input", "error");

    const arr = input.split(',').map(n => parseInt(n.trim()));

    try {
        const start = performance.now();

        const res = await fetch('/api/algorithms/search', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({algorithm: algo, data: arr, target: target})
        });
        const data = await res.json();
        const measuredMs = (performance.now() - start).toFixed(2);

        const complexity = BIG_O.searching[algo] || BIG_O.searching[algo.toLowerCase()];

        const resultDiv = document.getElementById('search-result');
        resultDiv.innerHTML = (data.found
            ? `<div class="success-message"> Found at index ${data.index}`
            : `<div class="error-message"> Not Found`)
            + buildComplexityHTML(complexity, measuredMs)
            + `</div>`;

        visualizeSearch(arr, data.index);
    } catch(e) {
        showMessage("Search failed", "error");
    }
    if (algo === 'interpolation') {
    executeInterpolationSearch();
    return;
    }
}

function visualizeSearch(arr, foundIndex) {
    const container = document.getElementById('search-container');
    container.innerHTML = arr.map((num, i) => `
        <div class="array-bar ${i === foundIndex ? 'active' : ''}" 
             style="height: ${Math.max(num*4, 20)}px;">
            ${num}
        </div>
    `).join('');
}

// ====================== BINARY SEARCH TREE ======================
async function insertBST() {
    const value = document.getElementById('bst-input').value;
    if (!value) return;

    try {
        const start = performance.now();

        const res = await fetch('/api/bst/insert', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({value: parseInt(value)})
        });
        const data = await res.json();
        const measuredMs = (performance.now() - start).toFixed(2);

        if (data.success) {
            renderBST(data.data);
            renderPerformancePanel(
                'bst-performance',
                BIG_O.bst.insert,
                measuredMs,
                'BST INSERT'
            );
        }
    } catch(e) {
        showMessage("BST Insert failed", "error");
    }
}

function resetBST() {
    fetch('/api/bst/reset', { method: 'POST' })
        .then(() => {
            document.getElementById('bst-canvas').innerHTML = '<p style="text-align:center; padding:100px; color:#999;">Tree is Empty</p>';
            document.getElementById('bst-performance').innerHTML = '';
        });
}

function renderBST(data) {
    const bstCanvas = document.getElementById('bst-canvas');
    bstCanvas.innerHTML = `<pre style="padding:20px; font-size:1.1em;">In-order: ${data.join(' → ')}</pre>`;
}

// ====================== TOWER OF HANOI ======================
function startHanoi() {
    startHanoiVisualization();
}

function startHanoiVisualization() {
    if (isHanoiRunning) return;

    const n = parseInt(document.getElementById('hanoi-disks').value) || 4;
    if (n < 1 || n > 7) {
        showMessage("Please select 1 to 7 disks", "error");
        return;
    }

    hanoiTowers = [
        Array.from({length: n}, (_, i) => n - i),
        [],
        []
    ];

    currentHanoiMoves = [];
    generateHanoiMoves(n, 0, 2, 1);

    const totalMoves = Math.pow(2, n) - 1;
    const complexity = BIG_O.hanoi.solve;

    document.getElementById('hanoi-status').innerHTML = `
        Solving ${n} disks... (${totalMoves} moves)
        ${buildComplexityHTML(complexity)}
    `;
    isHanoiRunning = true;

    const hanoiStart = performance.now();
    let moveIndex = 0;
    hanoiInterval = setInterval(() => {
        if (moveIndex < currentHanoiMoves.length) {
            const [from, to] = currentHanoiMoves[moveIndex];
            moveDisk(from, to);
            moveIndex++;
        } else {
            clearInterval(hanoiInterval);
            isHanoiRunning = false;
            const measuredMs = (performance.now() - hanoiStart).toFixed(2);
            document.getElementById('hanoi-status').innerHTML = `
                <span style="color:#4caf50">✅ Solved in ${currentHanoiMoves.length} moves!</span>
                ${buildComplexityHTML(complexity, measuredMs)}
            `;
        }
    }, 700);
}

function generateHanoiMoves(n, source, target, auxiliary) {
    if (n === 1) {
        currentHanoiMoves.push([source, target]);
        return;
    }
    generateHanoiMoves(n-1, source, auxiliary, target);
    currentHanoiMoves.push([source, target]);
    generateHanoiMoves(n-1, auxiliary, target, source);
}

function moveDisk(from, to) {
    const disk = hanoiTowers[from].pop();
    hanoiTowers[to].push(disk);
    renderHanoiTowers();
}

function renderHanoiTowers() {
    const container = document.getElementById('hanoi-visual');
    container.innerHTML = '';

    const towerNames = ['A', 'B', 'C'];

    hanoiTowers.forEach((tower, index) => {
        const towerElement = document.createElement('div');
        towerElement.style.textAlign = 'center';

        const pole = document.createElement('div');
        pole.style.width = '14px';
        pole.style.height = '300px';
        pole.style.background = '#2c3e50';
        pole.style.margin = '0 auto 8px';
        pole.style.borderRadius = '8px';

        const disksContainer = document.createElement('div');
        disksContainer.style.display = 'flex';
        disksContainer.style.flexDirection = 'column-reverse';
        disksContainer.style.alignItems = 'center';
        disksContainer.style.gap = '5px';
        disksContainer.style.minHeight = '200px';

        tower.forEach((size) => {
            const disk = document.createElement('div');
            disk.style.width = `${50 + size * 22}px`;
            disk.style.height = '32px';
            disk.style.background = `hsl(${180 + size * 25}, 85%, 55%)`;
            disk.style.borderRadius = '8px';
            disk.style.boxShadow = '0 6px 12px rgba(0,0,0,0.25)';
            disk.style.display = 'flex';
            disk.style.alignItems = 'center';
            disk.style.justifyContent = 'center';
            disk.style.color = 'white';
            disk.style.fontWeight = 'bold';
            disk.style.fontSize = '0.95em';
            disk.textContent = size;
            disksContainer.appendChild(disk);
        });

        const label = document.createElement('div');
        label.textContent = `Tower ${towerNames[index]}`;
        label.style.marginTop = '12px';
        label.style.fontWeight = '600';
        label.style.color = '#34495e';

        towerElement.appendChild(pole);
        towerElement.appendChild(disksContainer);
        towerElement.appendChild(label);
        container.appendChild(towerElement);
    });
}

function resetHanoi() {
    if (hanoiInterval) clearInterval(hanoiInterval);
    isHanoiRunning = false;
    hanoiTowers = [[], [], []];
    document.getElementById('hanoi-visual').innerHTML = `
        <p style="padding: 100px 20px; color:#888; text-align:center; font-size:1.1em;">
            Click "Start Animation" to begin
        </p>`;
    document.getElementById('hanoi-status').innerHTML = '';
}

// ====================== HELPER ======================
function showMessage(msg, type = 'success') {
    const div = document.createElement('div');
    div.className = type === 'error' ? 'error-message' : 'success-message';
    div.style.position = 'fixed';
    div.style.bottom = '20px';
    div.style.left = '50%';
    div.style.transform = 'translateX(-50%)';
    div.style.padding = '15px 25px';
    div.style.borderRadius = '8px';
    div.textContent = msg;
    document.body.appendChild(div);
    setTimeout(() => div.remove(), 4000);
}

// ====================== GRAPH ALGORITHMS ======================
let currentGraphType = "Undirected";

function createNewGraph(directed = false) {
    currentGraphType = directed ? "Directed" : "Undirected";

    fetch('/api/graph/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ directed: directed })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showMessage(`New ${currentGraphType} Graph Created Successfully!`, "success");
            document.getElementById('graph-display').innerHTML = "Graph is empty. Add some edges!";
        }
    });
}

function addGraphEdge() {
    const from = document.getElementById('edge-from').value.trim();
    const to   = document.getElementById('edge-to').value.trim();
    const weight = parseInt(document.getElementById('edge-weight').value) || 1;

    if (!from || !to) return showMessage("Both From and To vertices are required!", "error");

    const start = performance.now();

    fetch('/api/graph/add_edge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from, to, weight })
    })
    .then(res => res.json())
    .then(data => {
        const measuredMs = (performance.now() - start).toFixed(2);
        if (data.success) {
            showMessage(`Edge ${from} → ${to} (w=${weight}) added!`, "success");
            displayCurrentGraph();
            renderPerformancePanel(
                'graph-result',
                BIG_O.graph.add_edge,
                measuredMs,
                'ADD EDGE'
            );
        }
    });
}

function displayCurrentGraph() {
    fetch('/api/graph/display')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById('graph-display').innerHTML =
                    `<strong>Graph (${currentGraphType}):</strong><br><br>` +
                    data.display.replace(/\n/g, '<br>');
            }
        });
}

async function runBFS() {
    const start = prompt("Enter starting vertex for BFS:");
    if (!start) return;

    const t0 = performance.now();
    const res = await fetch('/api/graph/bfs', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({start: start})
    });
    const data = await res.json();
    const measuredMs = (performance.now() - t0).toFixed(2);

    if (data.success) {
        document.getElementById('graph-result').innerHTML = `
            <div class="success-message">
                <strong>BFS Traversal from ${start}:</strong><br>
                ${data.result.join(' → ')}
                ${buildComplexityHTML(BIG_O.graph.bfs, measuredMs)}
            </div>`;
    }
}

async function runDFS() {
    const start = prompt("Enter starting vertex for DFS:");
    if (!start) return;

    const t0 = performance.now();
    const res = await fetch('/api/graph/dfs', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({start: start})
    });
    const data = await res.json();
    const measuredMs = (performance.now() - t0).toFixed(2);

    if (data.success) {
        document.getElementById('graph-result').innerHTML = `
            <div class="success-message">
                <strong>DFS Traversal from ${start}:</strong><br>
                ${data.result.join(' → ')}
                ${buildComplexityHTML(BIG_O.graph.dfs, measuredMs)}
            </div>`;
    }
}

async function runShortestPath() {
    const start = prompt("Enter start vertex:");
    const end   = prompt("Enter end vertex:");
    if (!start || !end) return;

    const t0 = performance.now();
    const res = await fetch('/api/graph/shortest_path', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({start: start, end: end})
    });
    const data = await res.json();
    const measuredMs = (performance.now() - t0).toFixed(2);

    if (data.success) {
        if (data.path) {
            document.getElementById('graph-result').innerHTML = `
                <div class="success-message">
                    <strong>Shortest Path:</strong><br>
                    ${data.path.join(' → ')}<br>
                    <small>Total Weight: ${data.weight}</small>
                    ${buildComplexityHTML(BIG_O.graph.shortest_path, measuredMs)}
                </div>`;
        } else {
            document.getElementById('graph-result').innerHTML = `
                <div class="error-message">No path exists between ${start} and ${end}</div>`;
        }
    }
}

// ====================== HASH TABLE ======================
let currentHashMethod = "division";

function changeHashMethod() {
    currentHashMethod = document.getElementById('hash-method').value;
    showMessage(`Hash method changed to: ${currentHashMethod}`, "success");
}

async function insertHash() {
    const key   = document.getElementById('hash-key').value.trim();
    const value = document.getElementById('hash-value').value.trim();
    if (!key) return showMessage("Key is required!", "error");

    try {
        const start = performance.now();

        const res = await fetch('/api/ds/hash_table/insert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key, value: value || "(no value)", hash_method: currentHashMethod })
        });
        const data = await res.json();
        const measuredMs = (performance.now() - start).toFixed(2);

        if (data.success) {
            renderHashTable(data.data);
            document.getElementById('hash-info').innerHTML = `
                <strong>Hash Method:</strong> ${data.hash_method} | 
                <strong>Load Factor:</strong> ${data.load_factor}
                ${buildComplexityHTML(BIG_O.hash_table.insert, measuredMs)}
            `;
            showMessage(`Inserted "${key}" → "${value}"`, "success");
        } else {
            showMessage(data.error, "error");
        }
    } catch (err) {
        showMessage("Failed to insert into hash table", "error");
    }
}

async function getHash() {
    const key = document.getElementById('hash-key').value.trim();
    if (!key) return showMessage("Enter a key to search", "error");

    try {
        const start = performance.now();

        const res = await fetch('/api/ds/hash_table/get', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key })
        });
        const data = await res.json();
        const measuredMs = (performance.now() - start).toFixed(2);

        if (data.success) {
            const found = data.value !== null;
            showMessage(found ? `Found: "${key}" → "${data.value}"` : `Key "${key}" not found`,
                        found ? "success" : "error");
            renderHashTable(data.data);
            document.getElementById('hash-info').innerHTML =
                buildComplexityHTML(BIG_O.hash_table.get, measuredMs);
        }
    } catch (err) {
        showMessage("Search failed", "error");
    }
}

async function deleteHash() {
    const key = document.getElementById('hash-key').value.trim();
    if (!key) return showMessage("Enter a key to delete", "error");

    try {
        const start = performance.now();

        const res = await fetch('/api/ds/hash_table/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key })
        });
        const data = await res.json();
        const measuredMs = (performance.now() - start).toFixed(2);

        if (data.success) {
            showMessage(data.message, "success");
            renderHashTable(data.data);
            document.getElementById('hash-info').innerHTML =
                buildComplexityHTML(BIG_O.hash_table.delete, measuredMs);
        } else {
            showMessage(data.error || "Delete failed", "error");
        }
    } catch (err) {
        showMessage("Delete operation failed", "error");
    }
}

function clearHashTable() {
    if (confirm("Clear the entire hash table?")) {
        fetch('/api/ds/hash_table/clear', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    renderHashTable([]);
                    document.getElementById('hash-info').innerHTML = '';
                    showMessage("Hash Table cleared", "success");
                }
            })
            .catch(() => showMessage("Failed to clear our hash table", "error"));
    }
}

function renderHashTable(data) {
    const container = document.getElementById('hash-visualization');
    let html = `<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:15px;">`;

    data.forEach(bucket => {
        html += `
            <div style="background:white; padding:15px; border-radius:10px; border:2px solid #ddd;">
                <strong style="color:#667eea;">Bucket ${bucket.index}</strong>
                <div style="margin-top:10px; font-size:0.95em;">`;

        if (bucket.bucket && bucket.bucket.length > 0) {
            bucket.bucket.forEach(item => {
                html += `<div style="padding:6px 10px; background:#f0f0f0; margin:4px 0; border-radius:6px;">${item}</div>`;
            });
        } else {
            html += `<div style="color:#999; font-style:italic;">Empty bucket</div>`;
        }

        html += `</div></div>`;
    });

    html += `</div>`;
    container.innerHTML = html || '<p style="text-align:center; color:#999; padding:60px;">Hash Table is empty</p>';
}
// ====================== HEAPS (Min & Max) ======================
async function heapOperation(heapType, operation) {
    const valueInput = document.getElementById('heap-input');
    const value = valueInput ? valueInput.value.trim() : null;

    let endpoint = `/api/ds/${heapType}/${operation}`;

    let body = {};
    if ((operation === 'push' || operation === 'insert') && value) {
        body = { value: isNaN(value) ? value : Number(value) };
    }

    try {
        const start = performance.now();
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: Object.keys(body).length ? JSON.stringify(body) : null
        });

        const data = await res.json();
        const timeTaken = (performance.now() - start).toFixed(2);

        if (data.success) {
            updateDSVisualization(data.data || []);
            document.getElementById('ds-performance').innerHTML = `
                <strong style="color:#28a745">Running Time:</strong> ${timeTaken} ms
            `;
            showMessage(`${operation.toUpperCase()} successful on ${heapType}`, "success");
        } else {
            showMessage(data.error || "Operation failed", "error");
        }
    } catch (err) {
        showMessage(`Heap operation failed. Check blueprint routes.`, "error");
    }
}
// ====================== INTERPOLATION SEARCH ======================
async function executeInterpolationSearch() {
    const input = document.getElementById('search-input').value.trim();
    const target = parseInt(document.getElementById('search-target').value);

    if (!input || isNaN(target)) return showMessage("Invalid input", "error");

    const arr = input.split(',').map(n => parseInt(n.trim()));

    try {
        const res = await fetch('/api/algorithms/interpolation/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: arr, target: target })
        });

        const data = await res.json();

        const resultDiv = document.getElementById('search-result');
        if (data.found) {
            resultDiv.innerHTML = `
                <div class="success-message">
                     Interpolation Search<br><br>
                    Target <strong>${target}</strong> found at index <strong>${data.index}</strong><br>
                    <small>Comparisons: ${data.comparisons} | Time: ${data.time_taken_ms} ms</small>
                </div>`;
        } else {
            resultDiv.innerHTML = `<div class="error-message">❌ Target ${target} not found</div>`;
        }

        // Optional: Show steps
        console.log("Interpolation Steps:", data.steps);

    } catch (err) {
        showMessage("Interpolation Search failed", "error");
    }
}



// ====================== INITIALIZATION ======================
document.addEventListener('DOMContentLoaded', () => {
    showTab('ds');
    resetHanoi();
    createNewGraph();

    const sortInput = document.getElementById('sort-input');
    if (sortInput) sortInput.addEventListener('keypress', e => { if(e.key === 'Enter') executeSortWithMetrics(); });
});