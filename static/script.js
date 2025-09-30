document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const emailsList = document.getElementById('emailsList');
    const stats = document.getElementById('stats');
    const comments = document.getElementById('comments');
    const errorMessage = document.getElementById('errorMessage');

    // API endpoint
    const API_URL = '/categorizar';

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            if (e.target.files.length === 1) {
                fileName.textContent = `✓ ${e.target.files[0].name}`;
            } else {
                fileName.textContent = `✓ ${e.target.files.length} arquivos selecionados`;
            }
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        const files = fileInput.files;
        
        if (files.length === 0) {
            showError('Por favor, selecione pelo menos um arquivo.');
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
        formData.append('comentarios', comments.value);

        analyzeBtn.disabled = true;
        loading.classList.add('active');
        results.classList.remove('active');
        errorMessage.classList.remove('active');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }

            const data = await response.json();
            displayResults(data.resultado_categorizacao);
        } catch (error) {
            console.error('Erro:', error);
            showError(`Ocorreu um erro: ${error.message}`);
        } finally {
            analyzeBtn.disabled = false;
            loading.classList.remove('active');
        }
    });

    function displayResults(emails) {
        if (!emails || emails.length === 0) {
            showError('Nenhum resultado para exibir. Verifique o formato do arquivo ou a resposta da API.');
            return;
        }

        // Estatísticas
        const importantes = emails.filter(e => e.classificacao === 'Importante').length;
        const naoImportantes = emails.length - importantes;

        stats.innerHTML = `
            <div class="stat-box importante">
                <div class="stat-number">${importantes}</div>
                <div class="stat-label">E-mails Importantes</div>
            </div>
            <div class="stat-box nao-importante">
                <div class="stat-number">${naoImportantes}</div>
                <div class="stat-label">E-mails Não Importantes</div>
            </div>
        `;

        // Ordenar: importantes primeiro
        emails.sort((a, b) => {
            if (a.classificacao === 'Importante' && b.classificacao !== 'Importante') return -1;
            if (a.classificacao !== 'Importante' && b.classificacao === 'Importante') return 1;
            return 0;
        });

        // Lista de e-mails
        emailsList.innerHTML = emails.map(email => {
            const classe = email.classificacao === 'Importante' ? 'importante' : 'nao-importante';
            const titulo = email.titulo || 'Sem título';
            return `
                <div class="email-item ${classe}">
                    <div class="email-header">
                        <span class="email-id">E-mail #${email.id_email || 'N/A'} - ${titulo}</span>
                        <span class="badge ${classe}">${email.classificacao}</span>
                    </div>
                    <div class="email-content">
                        <h3>Justificativa:</h3>
                        <p>${email.justificativa_curta}</p>
                    </div>
                    <div class="email-content">
                        <h3>Sugestão de Resposta:</h3>
                        <p>${email.ideia_de_resposta}</p>
                    </div>
                </div>
            `;
        }).join('');

        results.classList.add('active');
        results.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.add('active');
    }
});