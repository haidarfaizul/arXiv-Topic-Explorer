// arXiv Topic Explorer Application Logic

// Complete metadata dictionary for 15 clusters
const CLUSTERS_DATA = {
    "0": {
        "id": "00",
        "name": "Gravitasi, Kosmologi & Fisika Energi Tinggi (General Relativity & Cosmology)",
        "title_keywords": ["gravity", "black hole", "relativity", "gravitational", "cosmology", "inflationary", "cosmic", "einstein", "spacetime", "metric"],
        "abstract_keywords": ["gravity", "black", "hole", "relativity", "gravitational", "wave", "cosmology", "inflationary", "cosmic", "field", "horizon"],
        "categories": [
            { "name": "gr-qc (General Relativity & Quantum Cosmology)", "percent": 58.87 },
            { "name": "hep-th (High Energy Physics - Theory)", "percent": 37.70 },
            { "name": "astro-ph.HE (High Energy Astrophysical Phenomena)", "percent": 20.27 }
        ]
    },
    "1": {
        "id": "01",
        "name": "Pemrosesan Bahasa Alami & AI Core (Natural Language Processing & Core AI)",
        "title_keywords": ["language", "translation", "semantic", "parser", "parsing", "corpus", "sentences", "word", "nlp", "text"],
        "abstract_keywords": ["language", "translation", "semantic", "parser", "parsing", "corpus", "sentences", "word", "nlp", "text", "machine"],
        "categories": [
            { "name": "cs.CL (Computation and Language)", "percent": 22.54 },
            { "name": "cs.AI (Artificial Intelligence)", "percent": 21.94 },
            { "name": "cs.LG (Machine Learning)", "percent": 21.48 }
        ]
    },
    "2": {
        "id": "02",
        "name": "Sistem Kontrol, Optimasi & Sistem Dinamis (Control Systems & Optimization)",
        "title_keywords": ["control", "optimal", "state", "optimization", "system", "feedback", "linear", "controller", "trajectory", "robust"],
        "abstract_keywords": ["control", "optimal", "state", "optimization", "system", "feedback", "linear", "controller", "trajectory", "robust", "lyapunov"],
        "categories": [
            { "name": "cs.LG (Machine Learning)", "percent": 9.73 },
            { "name": "cs.CV (Computer Vision)", "percent": 9.51 },
            { "name": "cs.AI (Artificial Intelligence)", "percent": 8.92 }
        ]
    },
    "3": {
        "id": "03",
        "name": "Fisika Kuantum & Informasi Kuantum (Quantum Physics & Information)",
        "title_keywords": ["quantum", "spin", "entanglement", "qubit", "teleportation", "gate", "coherence", "superconducting", "cavity", "photon"],
        "abstract_keywords": ["quantum", "spin", "entanglement", "qubit", "teleportation", "gate", "coherence", "superconducting", "cavity", "photon", "state"],
        "categories": [
            { "name": "quant-ph (Quantum Physics)", "percent": 60.89 },
            { "name": "cond-mat.mes-hall (Mesoscale and Nanoscale Physics)", "percent": 14.28 },
            { "name": "hep-th (High Energy Physics - Theory)", "percent": 10.38 }
        ]
    },
    "4": {
        "id": "04",
        "name": "Fisika Energi Tinggi Teoretis (Theoretical High Energy Physics)",
        "title_keywords": ["string", "supersymmetry", "conformal", "field", "branes", "dual", "duality", "holographic", "gravity", "dimensions"],
        "abstract_keywords": ["string", "supersymmetry", "conformal", "field", "branes", "dual", "duality", "holographic", "gravity", "dimensions", "gauge"],
        "categories": [
            { "name": "hep-th (High Energy Physics - Theory)", "percent": 27.48 },
            { "name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 11.16 },
            { "name": "gr-qc (General Relativity & Quantum Cosmology)", "percent": 7.97 }
        ]
    },
    "5": {
        "id": "05",
        "name": "Fisika Fenomenologi & Sistem Kompleks (Phenomenology & Complex Systems)",
        "title_keywords": ["model", "standard", "neutrino", "physics", "particles", "collider", "dark", "mass", "decay", "higgs"],
        "abstract_keywords": ["model", "standard", "neutrino", "physics", "particles", "collider", "dark", "mass", "decay", "higgs", "coupling"],
        "categories": [
            { "name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 12.78 },
            { "name": "cs.LG (Machine Learning)", "percent": 9.12 },
            { "name": "cs.AI (Artificial Intelligence)", "percent": 7.76 }
        ]
    },
    "6": {
        "id": "06",
        "name": "Fisika Benda Terkondensasi & Ilmu Bahan (Condensed Matter & Materials Science)",
        "title_keywords": ["superconducting", "materials", "crystal", "topological", "insulator", "transport", "magnetic", "electronic", "band", "structure"],
        "abstract_keywords": ["superconducting", "materials", "crystal", "topological", "insulator", "transport", "magnetic", "electronic", "band", "structure", "transition"],
        "categories": [
            { "name": "cond-mat.mes-hall (Mesoscale Physics)", "percent": 21.61 },
            { "name": "cond-mat.str-el (Strongly Correlated Electrons)", "percent": 21.11 },
            { "name": "cond-mat.mtrl-sci (Materials Science)", "percent": 17.66 }
        ]
    },
    "7": {
        "id": "07",
        "name": "Pembelajaran Mesin & Deep Learning Utama (Machine Learning & Deep Learning)",
        "title_keywords": ["learning", "deep", "reinforcement", "machine", "supervised", "data", "training", "performance", "neural", "network"],
        "abstract_keywords": ["learning", "deep", "reinforcement", "machine", "supervised", "data", "training", "performance", "neural", "network", "models"],
        "categories": [
            { "name": "cs.LG (Machine Learning)", "percent": 54.37 },
            { "name": "cs.AI (Artificial Intelligence)", "percent": 24.67 },
            { "name": "cs.CV (Computer Vision)", "percent": 23.00 }
        ]
    },
    "8": {
        "id": "08",
        "name": "Astrofisika & Astronomi (Astrophysics & Astronomy)",
        "title_keywords": ["galaxy", "star", "ray", "mass", "emission", "stellar", "gas", "radio", "telescope", "cluster"],
        "abstract_keywords": ["galaxy", "star", "ray", "mass", "emission", "stellar", "gas", "radio", "telescope", "cluster", "observations"],
        "categories": [
            { "name": "astro-ph.GA (Astrophysics of Galaxies)", "percent": 30.06 },
            { "name": "astro-ph (Astrophysics)", "percent": 29.17 },
            { "name": "astro-ph.SR (Solar and Stellar Astrophysics)", "percent": 19.55 }
        ]
    },
    "9": {
        "id": "09",
        "name": "Visi Komputer & Jaringan Saraf (Computer Vision & Neural Networks)",
        "title_keywords": ["neural", "network", "convolutional", "deep", "graph", "wireless", "detection", "layered", "hidden", "activation"],
        "abstract_keywords": ["neural", "network", "convolutional", "deep", "graph", "wireless", "detection", "layered", "hidden", "activation", "learning"],
        "categories": [
            { "name": "cs.LG (Machine Learning)", "percent": 35.61 },
            { "name": "cs.CV (Computer Vision)", "percent": 16.95 },
            { "name": "cs.AI (Artificial Intelligence)", "percent": 12.28 }
        ]
    },
    "10": {
        "id": "10",
        "name": "Topik Multidisiplin & Umum (Multidisciplinary & General Science)",
        "title_keywords": ["data", "analysis", "multi", "graphs", "dynamics", "dimensional", "functions", "high", "study", "field"],
        "abstract_keywords": ["data", "analysis", "multi", "graphs", "dynamics", "dimensional", "functions", "high", "study", "field", "results"],
        "categories": [
            { "name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 7.03 },
            { "name": "cs.LG (Machine Learning)", "percent": 6.50 },
            { "name": "cs.CV (Computer Vision)", "percent": 6.02 }
        ]
    },
    "11": {
        "id": "11",
        "name": "Aljabar, Teori Grup & Teori Representasi (Algebra & Group Theory)",
        "title_keywords": ["group", "algebra", "lie", "finite", "representation", "subgroups", "abelian", "free", "compact", "ring"],
        "abstract_keywords": ["group", "algebra", "lie", "finite", "representation", "subgroups", "abelian", "free", "compact", "ring", "prove"],
        "categories": [
            { "name": "math.GR (Group Theory)", "percent": 25.40 },
            { "name": "math.RT (Representation Theory)", "percent": 18.09 },
            { "name": "math.RA (Rings and Algebras)", "percent": 15.16 }
        ]
    },
    "12": {
        "id": "12",
        "name": "Persamaan Diferensial & Analisis Numerik (Differential Equations & Numerical Analysis)",
        "title_keywords": ["equation", "differential", "solution", "boundary", "value", "existence", "uniqueness", "nonlinear", "numerical", "method"],
        "abstract_keywords": ["equation", "differential", "solution", "boundary", "value", "existence", "uniqueness", "nonlinear", "numerical", "method", "paper"],
        "categories": [
            { "name": "math.AP (Analysis of PDEs)", "percent": 24.71 },
            { "name": "math-ph (Mathematical Physics)", "percent": 9.04 },
            { "name": "math.MP (Mathematical Physics)", "percent": 9.04 }
        ]
    },
    "13": {
        "id": "13",
        "name": "AI Generatif, Difusi & Retrieval (Generative AI, Diffusion & Information Retrieval)",
        "title_keywords": ["image", "text", "generation", "diffusion", "retrieval", "augmented", "video", "generative", "gan", "style"],
        "abstract_keywords": ["image", "text", "generation", "diffusion", "retrieval", "augmented", "video", "generative", "gan", "style", "models"],
        "categories": [
            { "name": "cs.CV (Computer Vision)", "percent": 25.87 },
            { "name": "cs.AI (Artificial Intelligence)", "percent": 20.72 },
            { "name": "cs.CL (Computation and Language)", "percent": 17.90 }
        ]
    },
    "14": {
        "id": "14",
        "name": "Kosmologi & Fenomenologi Partikel (Cosmology & Particle Physics Phenomenology)",
        "title_keywords": ["dark", "energy", "matter", "cosmic", "inflation", "gravitational", "lensing", "background", "cosmological", "acceleration"],
        "abstract_keywords": ["dark", "energy", "matter", "cosmic", "inflation", "gravitational", "lensing", "background", "cosmological", "acceleration", "hep-ph"],
        "categories": [
            { "name": "hep-ph (High Energy Physics - Phenomenology)", "percent": 34.22 },
            { "name": "astro-ph.CO (Cosmology and Nongalactic Astrophysics)", "percent": 19.22 },
            { "name": "gr-qc (General Relativity & Quantum Cosmology)", "percent": 13.14 }
        ]
    }
};

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', () => {
    // 1. Tab switching logic
    const tabs = document.querySelectorAll('.nav-tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            tab.classList.add('active');
            const targetId = `tab-${tab.dataset.tab}`;
            document.getElementById(targetId).classList.add('active');
            
            // Trigger animation repaint if explorer tab is loaded
            if (tab.dataset.tab === 'explorer') {
                const activeBtn = document.querySelector('.cluster-item-btn.active');
                if (activeBtn) {
                    loadClusterDetails(activeBtn.dataset.id);
                }
            }
        });
    });

    // 2. Initialize Topic Explorer
    initTopicExplorer();

    // 3. Initialize Interactive Predictor
    initPredictor();
});

// Topic Explorer initialization
function initTopicExplorer() {
    const listContainer = document.getElementById('cluster-selector-list');
    listContainer.innerHTML = '';

    // Populate sidebar list
    Object.keys(CLUSTERS_DATA).forEach((key, index) => {
        const cluster = CLUSTERS_DATA[key];
        const btn = document.createElement('button');
        btn.className = `cluster-item-btn ${index === 0 ? 'active' : ''}`;
        btn.dataset.id = key;
        btn.innerHTML = `
            <span class="cluster-num-badge">${cluster.id}</span>
            <span>${cluster.name.split(' (')[0]}</span>
        `;
        
        btn.addEventListener('click', () => {
            document.querySelectorAll('.cluster-item-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadClusterDetails(key);
        });

        listContainer.appendChild(btn);
    });

    // Load first cluster details by default
    loadClusterDetails("0");
}

// Display cluster details
function loadClusterDetails(id) {
    const cluster = CLUSTERS_DATA[id];
    const detailsPanel = document.getElementById('cluster-details-panel');

    if (!cluster) return;

    // Create list of tags
    const titleTags = cluster.title_keywords.map(w => `<span class="tag-badge">${w}</span>`).join('');
    const abstractTags = cluster.abstract_keywords.map(w => `<span class="tag-badge tag-badge-abstract">${w}</span>`).join('');

    // Create category bar lists
    const catListHtml = cluster.categories.map(cat => `
        <div class="cat-bar-item">
            <div class="cat-bar-label">
                <span class="cat-bar-name">${cat.name}</span>
                <span class="cat-bar-pct">${cat.percent}%</span>
            </div>
            <div class="cat-bar-outer">
                <div class="cat-bar-inner" style="width: 0%"></div>
            </div>
        </div>
    `).join('');

    detailsPanel.innerHTML = `
        <div class="cluster-title-area">
            <div class="cluster-meta-id">KLASTER ${cluster.id}</div>
            <h1 class="cluster-title-text">${cluster.name}</h1>
        </div>
        
        <div class="result-divider"></div>

        <div class="tags-area">
            <div class="tags-label">KATA KUNCI UTAMA (JUDUL PAPER)</div>
            <div class="tags-container">
                ${titleTags}
            </div>
        </div>

        <div class="tags-area">
            <div class="tags-label">KATA KUNCI UTAMA (ABSTRAK PAPER)</div>
            <div class="tags-container">
                ${abstractTags}
            </div>
        </div>

        <div class="result-divider"></div>

        <div class="categories-area">
            <div class="tags-label">KATEGORI ARXIV ASLI DOMINAN</div>
            ${catListHtml}
        </div>
    `;

    // Trigger progressive animation of category bars
    setTimeout(() => {
        const bars = detailsPanel.querySelectorAll('.cat-bar-inner');
        bars.forEach((bar, idx) => {
            bar.style.width = `${cluster.categories[idx].percent}%`;
        });
    }, 100);
}

// Interactive Predictor initialization
function initPredictor() {
    const btnPredict = document.getElementById('btn-predict-topic');
    
    btnPredict.addEventListener('click', () => {
        const title = document.getElementById('paper-title').value.trim();
        const abstract = document.getElementById('paper-abstract').value.trim();

        if (!title || !abstract) {
            alert('Harap masukkan Judul dan Abstrak paper terlebih dahulu.');
            return;
        }

        // Run prediction calculation
        const scores = predictTopicHeuristic(title, abstract);
        
        // Update UI with results
        displayPredictionResults(scores);
    });
}

// Client-side Heuristic Text Classification (TF-IDF keyword score matching)
function predictTopicHeuristic(title, abstract) {
    const titleClean = cleanAndTokenize(title);
    const abstractClean = cleanAndTokenize(abstract);
    
    const results = [];

    // Calculate score for each cluster
    Object.keys(CLUSTERS_DATA).forEach(key => {
        const cluster = CLUSTERS_DATA[key];
        let score = 0;

        // 1. Check title keywords (Title gets x2.0 weight!)
        cluster.title_keywords.forEach(word => {
            const matches = countOccurrences(titleClean, word);
            score += matches * 2.0;
        });

        // 2. Check abstract keywords
        cluster.abstract_keywords.forEach(word => {
            const matches = countOccurrences(abstractClean, word);
            score += matches * 1.0;
        });

        results.push({
            id: key,
            name: cluster.name,
            score: score
        });
    });

    // Normalize scores into percentages
    const totalScore = results.reduce((sum, item) => sum + item.score, 0);
    
    if (totalScore === 0) {
        // Fallback: If no keywords matched, distribute scores evenly with low values,
        // but rank "Topik Multidisiplin & Umum" (Cluster 10) highest as fallback.
        results.forEach(item => {
            item.percent = item.id === "10" ? 25 : 5;
        });
    } else {
        results.forEach(item => {
            item.percent = Math.round((item.score / totalScore) * 100);
        });
    }

    // Sort descending by percentage score
    results.sort((a, b) => b.percent - a.percent);
    return results;
}

// String cleaning and tokenization helper
function cleanAndTokenize(text) {
    return text.toLowerCase()
        .replace(/[^\w\s-]/g, ' ') // replace punctuation with space
        .split(/\s+/)
        .filter(word => word.length > 2); // only keep words with >2 chars
}

// Count occurrences of a word/phrase in tokens
function countOccurrences(tokens, keyword) {
    const keywordTokens = keyword.toLowerCase().split(/\s+/);
    if (keywordTokens.length === 1) {
        return tokens.filter(t => t === keywordTokens[0]).length;
    }
    
    // For multi-word keywords (e.g. "black hole"), check n-grams
    let count = 0;
    for (let i = 0; i <= tokens.length - keywordTokens.length; i++) {
        let match = true;
        for (let j = 0; j < keywordTokens.length; j++) {
            if (tokens[i + j] !== keywordTokens[j]) {
                match = false;
                break;
            }
        }
        if (match) {
            count++;
            i += keywordTokens.length - 1; // skip forward
        }
    }
    return count;
}

// Display top prediction results
function displayPredictionResults(scores) {
    const placeholder = document.getElementById('predictor-results-placeholder');
    const content = document.getElementById('predictor-results-content');
    
    placeholder.classList.add('hidden');
    content.classList.remove('hidden');

    const topResult = scores[0];
    const topClusterMeta = CLUSTERS_DATA[topResult.id];

    // Set top prediction labels
    document.getElementById('res-top-id').textContent = `Klaster ${topClusterMeta.id}`;
    document.getElementById('res-top-name').textContent = topResult.name;

    // Populated Top 3 Match bar charts
    const matchScoresContainer = document.getElementById('match-scores-container');
    matchScoresContainer.innerHTML = '';

    // Display Top 3 results
    scores.slice(0, 3).forEach(item => {
        const clusterMeta = CLUSTERS_DATA[item.id];
        const barItem = document.createElement('div');
        barItem.className = 'cat-bar-item';
        barItem.innerHTML = `
            <div class="cat-bar-label">
                <span class="cat-bar-name">Klaster ${clusterMeta.id} - ${item.name.split(' (')[0]}</span>
                <span class="cat-bar-pct">${item.percent}%</span>
            </div>
            <div class="cat-bar-outer">
                <div class="cat-bar-inner match-score-bar-inner" style="width: 0%"></div>
            </div>
        `;
        matchScoresContainer.appendChild(barItem);

        // Animate width expansion
        setTimeout(() => {
            barItem.querySelector('.cat-bar-inner').style.width = `${item.percent}%`;
        }, 100);
    });
}
