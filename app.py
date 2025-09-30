import os
import json
import fitz
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura a aplicação Flask
app = Flask(__name__)
CORS(app) # Permite requisições de origens diferentes (nosso frontend)

# Configura a API do Gemini com a chave
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")
    print("Verifique se a variável de ambiente 'GEMINI_API_KEY' está configurada corretamente.")

# Rota principal que renderiza a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota para receber os dados e categorizar
@app.route('/categorizar', methods=['POST'])
def categorizar_emails():
    # Verifica se os arquivos foram enviados na requisição
    if 'files' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    files = request.files.getlist('files')
    comentarios_adicionais = request.form.get('comentarios', '')

    # Se o usuário não selecionou nenhum arquivo
    if len(files) == 0 or all(file.filename == '' for file in files):
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    texto_emails = ""
    
    for file in files:
        if file.filename == '':
            continue
            
        try:
            if file.filename.lower().endswith('.pdf'):
                # Processa o arquivo PDF
                with fitz.open(stream=file.read(), filetype="pdf") as doc:
                    for page in doc:
                        texto_emails += page.get_text() + "\n"
            elif file.filename.lower().endswith('.txt'):
                # Processa o arquivo TXT
                texto_emails += file.read().decode('utf-8') + "\n"
            else:
                return jsonify({"error": f"Formato de arquivo não suportado: {file.filename}. Use .txt ou .pdf"}), 400
        except Exception as e:
            return jsonify({"error": f"Erro ao ler o arquivo {file.filename}: {e}"}), 500

    # Monta o prompt exatamente como especificado
    prompt = f"""
Você é um categorizador de e-mails. Sua tarefa é analisar o texto de e-mails fornecido abaixo e classificá-los em 'Importante' ou 'Não Importante'.

Critérios de Classificação (Use estes critérios ou adicione os critérios do usuário nos 'Comentários Adicionais'):
- 'Importante' se for sobre faturas, prazos, projetos de alto nível, ou contém palavras-chave de risco/urgência.
- 'Não Importante' se for propaganda, newsletters, ou notificação de pouco valor.

Por padrão coloque como resposta uma resposta curta, porém formate a resposta como o usuário requisitar, podendo ser longa ou em formataçaõ específica, além de responder e classificar de acordo com ele, a palavra mais forte é a do usuário

Comentários Adicionais do Usuário: [{comentarios_adicionais}]

E-mails para Classificar (Os e-mails podem ou não ser numerados):
--- INÍCIO DOS E-MAILS ---
{texto_emails}
--- FIM DOS E-MAILS ---

---
Formato de Saída Obrigatório: Retorne a saída estritamente como um JSON formatado da seguinte forma. Não inclua texto explicativo antes ou depois.
{{
  "resultado_categorizacao": [
    {{ "id_email": 1, "titulo": "Fatura Vencida", "classificacao": "Importante", "justificativa_curta": "Menciona 'Fatura Vencida'.", "ideia_de_resposta": "Política da empresa sobre fatura atrasada" }},
    {{ "id_email": 2, "titulo": "Newsletter Marketing", "classificacao": "Não Importante", "justificativa_curta": "É uma newsletter semanal de marketing.", "ideia_de_resposta": "Não responder" }}
  ]
}}
"""

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        cleaned_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        
        resultado_json = json.loads(cleaned_response)

        return jsonify(resultado_json)

    except json.JSONDecodeError:
        return jsonify({"error": "A resposta da API não foi um JSON válido.", "raw_response": response.text}), 500
    except Exception as e:
        return jsonify({"error": f"Ocorreu um erro ao chamar a API do Gemini: {e}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)