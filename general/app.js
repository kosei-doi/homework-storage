// 解答一覧データ
let solutions = [];

// 単一の解答ファイルから情報を抽出
async function extractSolutionInfo(filePath, fileName) {
    try {
        // ファイル名から問番号と日時を抽出
        const nameMatch = fileName.match(/solution_(.+?)_(\d{8})_(\d{6})\.html/) ||
                          fileName.match(/solution\.html/);

        let question = '';
        let date = '';
        let subject = '';
        let section = '';

        if (nameMatch && nameMatch.length >= 4) {
            // アーカイブファイル: solution_問番号_YYYYMMDD_HHMMSS.html
            question = nameMatch[1] || '';
            const dateStr = nameMatch[2] || '';
            const timeStr = nameMatch[3] || '';
            if (dateStr && timeStr) {
                date = `${dateStr.substring(0,4)}-${dateStr.substring(4,6)}-${dateStr.substring(6,8)}T${timeStr.substring(0,2)}:${timeStr.substring(2,4)}:${timeStr.substring(4,6)}`;
            }
        } else if (fileName === 'solution.html') {
            // 現在の解答: 日付は現在時刻
            const now = new Date();
            date = now.toISOString();
        }

        // HTML本体から科目名・問番号などを抽出
        try {
            const response = await fetch(filePath);
            if (response.ok) {
                const html = await response.text();

                // <title> から科目名を抽出
                const titleMatch = html.match(/<title>(.+?)<\/title>/);
                if (titleMatch) {
                    const title = titleMatch[1];
                    subject = title.replace(/\s*解答.*$/, '').trim();
                }

                // <h1> から科目名・問番号を補完
                const h1Match = html.match(/<h1>(.+?)<\/h1>/);
                if (h1Match) {
                    const h1Text = h1Match[1];
                    if (!subject) {
                        subject = h1Text.replace(/\s*問.*$/, '').trim();
                    }
                    if (!question && h1Text.includes('問')) {
                        const qMatch = h1Text.match(/問[０-９0-9]+[^】\s]*/);
                        if (qMatch) {
                            question = qMatch[0].trim();
                        }
                    }
                }
            }
        } catch (e) {
            console.warn(`Failed to fetch ${filePath}:`, e);
        }

        // 現在の解答の場合は input.txt / assignment.txt から補完
        if (fileName === 'solution.html') {
            try {
                const inputResp = await fetch('general/input.txt');
                if (inputResp.ok) {
                    const inputText = await inputResp.text();
                    const lines = inputText.split('\n');
                    if (lines.length > 0) {
                        const subjectLine = lines[0].trim();
                        subject = subjectLine.replace(/\s+\d+\s+\d+.*$/, '').trim();
                    }
                    if (lines.length > 1) {
                        const sectionLine = lines[1].trim();
                        section = sectionLine.match(/§\d+/)?.[0] || sectionLine.split(/\s+/)[0] || '';
                    }
                }
            } catch (e) {
                console.warn('Failed to fetch general/input.txt:', e);
            }

            try {
                const assignResp = await fetch('general/assignment.txt');
                if (assignResp.ok) {
                    const assignText = await assignResp.text();
                    question = assignText.trim();
                }
            } catch (e) {
                console.warn('Failed to fetch general/assignment.txt:', e);
            }
        }

        // 表示用日時
        let displayDate;
        if (date && date.includes('T')) {
            const d = new Date(date);
            displayDate = isNaN(d.getTime()) ? new Date().toLocaleString('ja-JP') : d.toLocaleString('ja-JP');
        } else {
            displayDate = new Date().toLocaleString('ja-JP');
        }

        return {
            filePath,
            fileName,
            subject: subject || '不明',
            section: section || '不明',
            question: question || '不明',
            date: date || new Date().toISOString(),
            displayDate
        };
    } catch (e) {
        console.error(`Error extracting info from ${fileName}:`, e);
        return null;
    }
}

// 解答リストの読み込み
async function loadSolutions() {
    const list = [];

    // 現在の解答
    const current = await extractSolutionInfo('general/output/solution.html', 'solution.html');
    if (current) list.push(current);

    // アーカイブ（index.txt 経由）
    try {
        const resp = await fetch('general/archive/index.txt');
        if (resp.ok) {
            const text = await resp.text();
            const files = text.split('\n').map(l => l.trim()).filter(l => l && l.endsWith('.html'));
            for (const f of files) {
                const info = await extractSolutionInfo(`general/archive/${f}`, f);
                if (info) list.push(info);
            }
        }
    } catch (e) {
        console.warn('Failed to load archive index:', e);
    }

    return list;
}

// カード描画
function renderSolutionCard(solution) {
    const card = document.createElement('div');
    card.className = 'solution-card';
    card.dataset.subject = solution.subject;
    card.dataset.section = solution.section;
    card.dataset.question = solution.question;
    card.dataset.date = solution.date;

    card.innerHTML = `
        <div class="card-header">
            <h3 class="card-title">${solution.question}</h3>
            <span class="card-date">${solution.displayDate}</span>
        </div>
        <div class="card-body">
            <div class="card-info">
                <span class="info-item"><strong>科目:</strong> ${solution.subject}</span>
                <span class="info-item"><strong>セクション:</strong> ${solution.section}</span>
            </div>
        </div>
        <div class="card-footer">
            <button class="view-btn" onclick="viewSolution('${solution.filePath}')">閲覧</button>
            <button class="view-btn external-btn" onclick="viewSolutionInNewTab('${solution.filePath}')" title="新しいタブで開く">🔗</button>
        </div>
    `;

    return card;
}

// 解答をモーダルで表示
async function viewSolution(filePath) {
    const modal = document.getElementById('solutionModal');
    const modalBody = document.getElementById('modalBody');

    modal.style.display = 'block';
    modalBody.innerHTML = '<p class="loading">読み込んでいます...</p>';

    try {
        const resp = await fetch(filePath);
        if (!resp.ok) throw new Error('Failed to load solution');
        const html = await resp.text();

        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        modalBody.innerHTML = doc.body.innerHTML;

        if (window.MathJax) {
            window.MathJax.typesetPromise([modalBody]).catch(err => {
                console.error('MathJax rendering error:', err);
            });
        }
    } catch (e) {
        modalBody.innerHTML = `<p class="error">解答の読み込みに失敗しました: ${e.message}</p>`;
    }
}

// 新しいタブで表示
function viewSolutionInNewTab(filePath) {
    window.open(filePath, '_blank');
}

// フィルタ & ソート
function filterAndSort() {
    const subjectFilter = document.getElementById('filterSubject').value;
    const sectionFilter = document.getElementById('filterSection').value;
    const questionFilter = document.getElementById('filterQuestion').value;
    const sortBy = document.getElementById('sortBy').value;

    let filtered = solutions.filter(sol => {
        return (!subjectFilter || sol.subject === subjectFilter) &&
               (!sectionFilter || sol.section === sectionFilter) &&
               (!questionFilter || sol.question === questionFilter);
    });

    filtered.sort((a, b) => {
        switch (sortBy) {
            case 'date-desc':
                return new Date(b.date) - new Date(a.date);
            case 'date-asc':
                return new Date(a.date) - new Date(b.date);
            case 'question':
                return a.question.localeCompare(b.question, 'ja');
            case 'subject':
                return a.subject.localeCompare(b.subject, 'ja');
            default:
                return 0;
        }
    });

    const list = document.getElementById('solutionsList');
    list.innerHTML = '';

    if (filtered.length === 0) {
        list.innerHTML = '<p class="no-results">解答が見つかりませんでした。</p>';
        return;
    }

    filtered.forEach(sol => {
        list.appendChild(renderSolutionCard(sol));
    });
}

// フィルタの選択肢更新
function updateFilterOptions() {
    const subjects = [...new Set(solutions.map(s => s.subject))].sort();
    const sections = [...new Set(solutions.map(s => s.section))].sort();
    const questions = [...new Set(solutions.map(s => s.question))].sort();

    const subjectSelect = document.getElementById('filterSubject');
    const sectionSelect = document.getElementById('filterSection');
    const questionSelect = document.getElementById('filterQuestion');

    subjects.forEach(sub => {
        const opt = document.createElement('option');
        opt.value = sub;
        opt.textContent = sub;
        subjectSelect.appendChild(opt);
    });

    sections.forEach(sec => {
        const opt = document.createElement('option');
        opt.value = sec;
        opt.textContent = sec;
        sectionSelect.appendChild(opt);
    });

    questions.forEach(q => {
        const opt = document.createElement('option');
        opt.value = q;
        opt.textContent = q;
        questionSelect.appendChild(opt);
    });
}

// モーダルを閉じる
function closeModal() {
    document.getElementById('solutionModal').style.display = 'none';
}

// 初期化
async function init() {
    // モーダルのイベント
    const closeBtn = document.querySelector('.close');
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    const modal = document.getElementById('solutionModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target.id === 'solutionModal') closeModal();
        });
    }

    // フィルタ・ソートイベント
    document.getElementById('filterSubject').addEventListener('change', filterAndSort);
    document.getElementById('filterSection').addEventListener('change', filterAndSort);
    document.getElementById('filterQuestion').addEventListener('change', filterAndSort);
    document.getElementById('sortBy').addEventListener('change', filterAndSort);

    // 解答読み込み
    solutions = await loadSolutions();

    if (solutions.length === 0) {
        document.getElementById('solutionsList').innerHTML = '<p class="no-results">解答が見つかりませんでした。</p>';
        return;
    }

    updateFilterOptions();
    filterAndSort();
}

// DOMロード時に初期化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// グローバルに公開
window.viewSolution = viewSolution;
window.viewSolutionInNewTab = viewSolutionInNewTab;
