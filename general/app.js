// 解答ファイルのリスト（手動で管理、または自動生成）
let solutions = [];

// 解答情報を抽出する関数
async function extractSolutionInfo(filePath, fileName) {
    try {
        // ファイル名から情報を抽出
        // 形式: solution_問番号_YYYYMMDD_HHMMSS.html または solution.html
        const nameMatch = fileName.match(/solution_(.+?)_(\d{8})_(\d{6})\.html/) || 
                         fileName.match(/solution\.html/);
        
        let question = '';
        let date = '';
        let subject = '';
        let section = '';

        if (nameMatch && nameMatch.length > 1) {
            question = nameMatch[1];
            const dateStr = nameMatch[2];
            const timeStr = nameMatch[3];
            // 日付をISO形式で保存（ソート用）
            date = `${dateStr.substring(0,4)}-${dateStr.substring(4,6)}-${dateStr.substring(6,8)}T${timeStr.substring(0,2)}:${timeStr.substring(2,4)}:${timeStr.substring(4,6)}`;
        } else if (fileName === 'solution.html') {
            // 現在の解答の場合、日付は現在時刻
            const now = new Date();
            date = now.toISOString();
        }

        // HTMLファイルから情報を抽出
        try {
            const response = await fetch(filePath);
            if (!response.ok) return null;
            const html = await response.text();
            
            // titleタグから科目名を抽出
            const titleMatch = html.match(/<title>(.+?)<\/title>/);
            if (titleMatch) {
                const title = titleMatch[1];
                // 「線形代数 解答」のような形式から科目名を抽出
                subject = title.replace(/\s*解答.*$/, '').trim();
            }

            // h1タグからも情報を抽出
            const h1Match = html.match(/<h1>(.+?)<\/h1>/);
            if (h1Match) {
                const h1Text = h1Match[1];
                if (!subject) {
                    subject = h1Text.replace(/\s*問.*$/, '').trim();
                }
                if (!question && h1Text.includes('問')) {
                    const questionMatch = h1Text.match(/問[０-９0-9]+/);
                    if (questionMatch) {
                        question = questionMatch[0];
                    }
                }
            }
        } catch (e) {
            console.warn(`Failed to fetch ${filePath}:`, e);
        }

        // input.txtから情報を取得（現在の解答の場合）
        if (fileName === 'solution.html') {
            try {
                const inputResponse = await fetch('general/input.txt');
                if (inputResponse.ok) {
                    const inputText = await inputResponse.text();
                    const lines = inputText.split('\n');
                    if (lines.length > 0) {
                        const subjectLine = lines[0].trim();
                        // 「線形代数（坂口）2025 90」のような形式から科目名を抽出
                        subject = subjectLine.replace(/\s+\d+\s+\d+.*$/, '').trim();
                    }
                    if (lines.length > 1) {
                        const sectionLine = lines[1].trim();
                        // 「§9 直交性」のような形式からセクションを抽出
                        section = sectionLine.match(/§\d+/)?.[0] || sectionLine.split(/\s+/)[0] || '';
                    }
                }
            } catch (e) {
                console.warn('Failed to fetch general/input.txt:', e);
            }

            // assignment.txtから問番号を取得
            try {
                const assignmentResponse = await fetch('general/assignment.txt');
                if (assignmentResponse.ok) {
                    const assignmentText = await assignmentResponse.text();
                    question = assignmentText.trim();
                }
            } catch (e) {
                console.warn('Failed to fetch general/assignment.txt:', e);
            }
        }

        // 表示用の日付を設定
        let displayDate;
        if (date && date.includes('T')) {
            // ISO形式の日付を表示用に変換
            const dateObj = new Date(date);
            if (!isNaN(dateObj.getTime())) {
                displayDate = dateObj.toLocaleString('ja-JP');
            } else {
                // ファイル名から直接抽出した場合
                const dateMatch = fileName.match(/(\d{8})_(\d{6})/);
                if (dateMatch) {
                    const dateStr = dateMatch[1];
                    const timeStr = dateMatch[2];
                    displayDate = `${dateStr.substring(0,4)}/${dateStr.substring(4,6)}/${dateStr.substring(6,8)} ${timeStr.substring(0,2)}:${timeStr.substring(2,4)}:${timeStr.substring(4,6)}`;
                } else {
                    displayDate = new Date().toLocaleString('ja-JP');
                }
            }
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
            displayDate: displayDate
        };
    } catch (e) {
        console.error(`Error extracting info from ${fileName}:`, e);
        return null;
    }
}

// 解答ファイルのリストを取得
async function loadSolutions() {
    const solutionsList = [];
    
    // 現在の解答（general/output/solution.html）
    const currentSolution = await extractSolutionInfo('general/output/solution.html', 'solution.html');
    if (currentSolution) {
        solutionsList.push(currentSolution);
    }

    // アーカイブされた解答を取得
    // 注意: GitHub Pagesではファイルシステムへの直接アクセスができないため、
    // 解答ファイルのリストを手動で管理するか、GitHub APIを使用する必要があります
    
    // 方法1: 既知のアーカイブファイルをチェック（必要に応じて手動で追加）
    // アーカイブファイル名をここに追加してください
    const knownArchives = [
        'solution_問3 (2)_20251124_141437.html',
        'solution_問3 (１)_20251124_143914.html',
        'solution_問3 (３)_20251124_142313.html'
    ];
    
    // 既知のアーカイブファイルを読み込む
    for (const archiveFile of knownArchives) {
        const archivePath = `general/archive/${archiveFile}`;
        const archiveInfo = await extractSolutionInfo(archivePath, archiveFile);
        if (archiveInfo) {
            solutionsList.push(archiveInfo);
        }
    }

    // 方法1.5: アーカイブディレクトリのインデックスファイルを読み込む（存在する場合）
    try {
        const indexResponse = await fetch('general/archive/index.txt');
        if (indexResponse.ok) {
            const indexText = await indexResponse.text();
            const archiveFiles = indexText.split('\n').map(line => line.trim()).filter(line => line && line.endsWith('.html'));
            for (const archiveFile of archiveFiles) {
                // 既に読み込んだファイルはスキップ
                if (!knownArchives.includes(archiveFile)) {
                    const archivePath = `general/archive/${archiveFile}`;
                    const archiveInfo = await extractSolutionInfo(archivePath, archiveFile);
                    if (archiveInfo) {
                        solutionsList.push(archiveInfo);
                    }
                }
            }
        }
    } catch (e) {
        // インデックスファイルが存在しない場合は無視
        console.debug('Archive index file not found, using known archives only');
    }

    // 方法2: メタデータJSONファイルを読み込む（推奨）
    // 解答生成時にmetadata.jsonを作成する場合は、以下のコードを有効化してください
    /*
    try {
        const metadataResponse = await fetch('metadata.json');
        if (metadataResponse.ok) {
            const metadata = await metadataResponse.json();
            for (const item of metadata.solutions) {
                const solutionInfo = await extractSolutionInfo(item.path, item.fileName);
                if (solutionInfo) {
                    // メタデータから情報を補完
                    if (item.subject) solutionInfo.subject = item.subject;
                    if (item.section) solutionInfo.section = item.section;
                    if (item.question) solutionInfo.question = item.question;
                    if (item.date) solutionInfo.date = item.date;
                    solutionsList.push(solutionInfo);
                }
            }
        }
    } catch (e) {
        console.warn('Failed to load metadata.json:', e);
    }
    */
    
    return solutionsList;
}

// 解答カードを表示
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

// 解答を新しいタブで開く
function viewSolutionInNewTab(filePath) {
    window.open(filePath, '_blank');
}

// 解答を表示
async function viewSolution(filePath) {
    const modal = document.getElementById('solutionModal');
    const modalBody = document.getElementById('modalBody');
    
    modal.style.display = 'block';
    modalBody.innerHTML = '<p class="loading">読み込んでいます...</p>';

    try {
        const response = await fetch(filePath);
        if (!response.ok) throw new Error('Failed to load solution');
        
        const html = await response.text();
        
        // HTMLをパースしてbodyの内容を取得
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const bodyContent = doc.body.innerHTML;
        
        // MathJaxを再読み込みするために、コンテナを作成
        modalBody.innerHTML = bodyContent;
        
        // MathJaxを再レンダリング
        if (window.MathJax) {
            window.MathJax.typesetPromise([modalBody]).catch(function (err) {
                console.error('MathJax rendering error:', err);
            });
        }
    } catch (e) {
        modalBody.innerHTML = `<p class="error">解答の読み込みに失敗しました: ${e.message}</p>`;
    }
}

// フィルタリングとソート
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

    // ソート
    filtered.sort((a, b) => {
        switch (sortBy) {
            case 'date-desc':
                const dateA = new Date(a.date);
                const dateB = new Date(b.date);
                return isNaN(dateB.getTime()) ? -1 : (isNaN(dateA.getTime()) ? 1 : dateB.getTime() - dateA.getTime());
            case 'date-asc':
                const dateA2 = new Date(a.date);
                const dateB2 = new Date(b.date);
                return isNaN(dateA2.getTime()) ? 1 : (isNaN(dateB2.getTime()) ? -1 : dateA2.getTime() - dateB2.getTime());
            case 'question':
                return a.question.localeCompare(b.question, 'ja');
            case 'subject':
                return a.subject.localeCompare(b.subject, 'ja');
            default:
                return 0;
        }
    });

    // 表示
    const listContainer = document.getElementById('solutionsList');
    listContainer.innerHTML = '';

    if (filtered.length === 0) {
        listContainer.innerHTML = '<p class="no-results">該当する解答が見つかりませんでした。</p>';
        return;
    }

    filtered.forEach(solution => {
        const card = renderSolutionCard(solution);
        listContainer.appendChild(card);
    });
}

// フィルタオプションを更新
function updateFilterOptions() {
    const subjects = [...new Set(solutions.map(s => s.subject))].sort();
    const sections = [...new Set(solutions.map(s => s.section))].sort();
    const questions = [...new Set(solutions.map(s => s.question))].sort();

    const subjectSelect = document.getElementById('filterSubject');
    const sectionSelect = document.getElementById('filterSection');
    const questionSelect = document.getElementById('filterQuestion');

    // 科目
    subjects.forEach(subject => {
        if (!Array.from(subjectSelect.options).some(opt => opt.value === subject)) {
            const option = document.createElement('option');
            option.value = subject;
            option.textContent = subject;
            subjectSelect.appendChild(option);
        }
    });

    // セクション
    sections.forEach(section => {
        if (!Array.from(sectionSelect.options).some(opt => opt.value === section)) {
            const option = document.createElement('option');
            option.value = section;
            option.textContent = section;
            sectionSelect.appendChild(option);
        }
    });

    // 問番号
    questions.forEach(question => {
        if (!Array.from(questionSelect.options).some(opt => opt.value === question)) {
            const option = document.createElement('option');
            option.value = question;
            option.textContent = question;
            questionSelect.appendChild(option);
        }
    });
}

// モーダルを閉じる
function closeModal() {
    document.getElementById('solutionModal').style.display = 'none';
}

// 初期化
async function init() {
    // モーダルの閉じるボタン
    document.querySelector('.close').addEventListener('click', closeModal);
    document.getElementById('solutionModal').addEventListener('click', (e) => {
        if (e.target.id === 'solutionModal') {
            closeModal();
        }
    });

    // フィルタとソートのイベントリスナー
    document.getElementById('filterSubject').addEventListener('change', filterAndSort);
    document.getElementById('filterSection').addEventListener('change', filterAndSort);
    document.getElementById('filterQuestion').addEventListener('change', filterAndSort);
    document.getElementById('sortBy').addEventListener('change', filterAndSort);

    // 解答を読み込む
    solutions = await loadSolutions();
    
    if (solutions.length === 0) {
        document.getElementById('solutionsList').innerHTML = 
            '<p class="no-results">解答が見つかりませんでした。</p>';
        return;
    }

    updateFilterOptions();
    filterAndSort();
}

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', init);

// グローバルスコープにviewSolutionとviewSolutionInNewTabを公開
window.viewSolution = viewSolution;
window.viewSolutionInNewTab = viewSolutionInNewTab;

