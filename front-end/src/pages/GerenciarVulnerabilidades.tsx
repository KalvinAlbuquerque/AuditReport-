import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

// Tipagem para uma vulnerabilidade (mantida)
type Vulnerabilidade = {
  Categoria: string;
  Subcategoria: string;
  Vulnerabilidade: string;
  Descrição: string;
  Solução: string;
  Imagem: string; // Caminho da imagem (URL ou caminho relativo)
};

// NOVAS Tipagens para os dados descritivos (categorias e subcategorias)
type SubcategoriaDescritiva = {
  subcategoria: string;
  descricao: string;
};

type CategoriaDescritiva = {
  categoria: string;
  descricao: string;
  subcategorias: SubcategoriaDescritiva[];
};


// --- Funções de API Reais ---
const API_BASE_URL = "http://127.0.0.1:5000/vulnerabilidades"; // Base da URL para seu backend

const fetchAllVulnerabilities = async (vulnType: 'sites' | 'servers'): Promise<Vulnerabilidade[]> => {
  const response = await fetch(`${API_BASE_URL}/getVulnerabilidades/?type=${vulnType}`);
  if (!response.ok) {
    // Tenta ler o erro como JSON, mas se for HTML, `response.json()` vai falhar.
    // É uma boa prática tentar ler o texto se o JSON falhar.
    try {
      const errorData = await response.json();
      throw new Error(errorData.error || `Erro ao buscar vulnerabilidades: ${response.status} ${response.statusText}`);
    } catch (e) {
      const errorText = await response.text();
      console.error("Erro na resposta (não JSON):", errorText);
      throw new Error(`Erro ao buscar vulnerabilidades: ${response.status} ${response.statusText}. Resposta inesperada do servidor.`);
    }
  }
  return response.json();
};

// NOVA: Função de API para fazer upload da imagem
const uploadImageApi = async (file: File, categoria: string, subcategoria: string, vulnerabilidade: string) => {
    const formData = new FormData();
    formData.append('image', file);
    formData.append('categoria', categoria);
    formData.append('subcategoria', subcategoria);
    formData.append('vulnerabilidade', vulnerabilidade);

    const response = await fetch(`${API_BASE_URL}/uploadImage/`, {
        method: "POST",
        body: formData, // FormData não precisa de 'Content-Type' header; o navegador o define automaticamente
    });

    if (!response.ok) {
        try {
            const errorData = await response.json();
            throw new Error(errorData.error || `Erro ao enviar imagem: ${response.status} ${response.statusText}`);
        } catch (e) {
            const errorText = await response.text();
            console.error("Erro na resposta do upload (não JSON):", errorText);
            throw new Error(`Erro ao enviar imagem: ${response.status} ${response.statusText}. Resposta inesperada do servidor.`);
        }
    }
    const result = await response.json();
    return result.imagePath; // Retorna o caminho da imagem fornecido pelo backend
};

// NOVA: Função de API para buscar categorias e subcategorias descritivas
const fetchDescritivos = async (vulnType: 'sites' | 'servers'): Promise<CategoriaDescritiva[]> => {
  const response = await fetch(`${API_BASE_URL}/getDescritivos/?type=${vulnType}`);
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.error || `Erro ao buscar descritivos: ${response.status} ${response.statusText}`);
    } catch (e) {
      const errorText = await response.text();
      console.error("Erro na resposta dos descritivos (não JSON):", errorText);
      throw new Error(`Erro ao buscar descritivos: ${response.status} ${response.statusText}. Resposta inesperada do servidor.`);
    }
  }
  return response.json();
};


const addVulnerabilidadeApi = async (vulnType: 'sites' | 'servers', data: Vulnerabilidade) => {
  const response = await fetch(`${API_BASE_URL}/addVulnerabilidade/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: vulnType, data: data }),
  });
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.error || `Erro ao adicionar vulnerabilidade: ${response.status} ${response.statusText}`);
    } catch (e) {
      const errorText = await response.text();
      console.error("Erro na resposta (não JSON):", errorText);
      throw new Error(`Erro ao adicionar vulnerabilidade: ${response.status} ${response.statusText}. Resposta inesperada do servidor.`);
    }
  }
  return response.json();
};

const updateVulnerabilidadeApi = async (vulnType: 'sites' | 'servers', oldName: string, data: Vulnerabilidade) => {
  const response = await fetch(`${API_BASE_URL}/updateVulnerabilidade/`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: vulnType, oldName: oldName, data: data }),
  });
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.error || `Erro ao atualizar vulnerabilidade: ${response.status} ${response.statusText}`);
    } catch (e) {
      const errorText = await response.text();
      console.error("Erro na resposta (não JSON):", errorText);
      throw new Error(`Erro ao atualizar vulnerabilidade: ${response.status} ${response.statusText}. Resposta inesperada do servidor.`);
    }
  }
  return response.json();
};

const deleteVulnerabilidadeApi = async (vulnType: 'sites' | 'servers', name: string) => {
  const response = await fetch(`${API_BASE_URL}/deleteVulnerabilidade/`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: vulnType, name: name }),
  });
  if (!response.ok) {
    try {
      const errorData = await response.json();
      throw new Error(errorData.error || `Erro ao deletar vulnerabilidade: ${response.status} ${response.statusText}`);
    } catch (e) {
      const errorText = await response.text();
      console.error("Erro na resposta (não JSON):", errorText);
      throw new Error(`Erro ao deletar vulnerabilidade: ${response.status} ${response.statusText}. Resposta inesperada do servidor.`);
    }
  }
  return response.json();
};
// --- FIM DAS FUNÇÕES DE API REAIS ---


const GerenciarVulnerabilidades = () => {
  const [vulnerabilidades, setVulnerabilidades] = useState<Vulnerabilidade[]>([]);
  const [vulnSelecionada, setVulnSelecionada] = useState<Vulnerabilidade | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formMode, setFormMode] = useState<"add" | "edit">("add");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedVulnType, setSelectedVulnType] = useState<'sites' | 'servers'>('sites'); 
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // NOVO: Estado para armazenar as categorias e subcategorias descritivas
  const [categoriasDescritivas, setCategoriasDescritivas] = useState<CategoriaDescritiva[]>([]);

  // Estado do formulário
  const [formData, setFormData] = useState<Vulnerabilidade>({
    Categoria: "",
    Subcategoria: "",
    Vulnerabilidade: "",
    Descrição: "",
    Solução: "",
    Imagem: "",
  });

  // Função para carregar as vulnerabilidades
  const loadVulnerabilities = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchAllVulnerabilities(selectedVulnType);
      setVulnerabilidades(data);
    } catch (err: any) {
      console.error("Erro ao buscar vulnerabilidades:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // NOVO: Função para carregar as categorias descritivas
  const loadCategoriasDescritivas = async () => {
    try {
      const data = await fetchDescritivos(selectedVulnType);
      setCategoriasDescritivas(data);
    } catch (err: any) {
      console.error("Erro ao buscar categorias descritivas:", err);
      // Você pode optar por exibir um erro ao usuário aqui também
    }
  };

  // Carregar vulnerabilidades e categorias descritivas ao montar o componente ou quando o tipo selecionado muda
  useEffect(() => {
    loadVulnerabilities();
    loadCategoriasDescritivas(); // Carrega as categorias descritivas também
  }, [selectedVulnType]);

  // Filtra as vulnerabilidades baseadas no termo de pesquisa
  const filteredVulnerabilities = vulnerabilidades.filter((vuln) =>
    vuln.Vulnerabilidade.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vuln.Categoria.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vuln.Subcategoria.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelectVuln = (vuln: Vulnerabilidade) => {
    setVulnSelecionada(vuln);
  };

  const handleAddClick = () => {
    setFormMode("add");
    setFormData({ // Limpa o formulário para uma nova entrada
      Categoria: "",
      Subcategoria: "",
      Vulnerabilidade: "",
      Descrição: "",
      Solução: "",
      Imagem: "",
    });
    setSelectedFile(null); // Limpa o arquivo selecionado ao adicionar nova vulnerabilidade
    setIsModalOpen(true);
  };

  const handleEditClick = () => {
    if (vulnSelecionada) {
      setFormMode("edit");
      setFormData({ ...vulnSelecionada }); // Preenche o formulário com dados da vulnerabilidade selecionada
      setSelectedFile(null); // Limpa o arquivo selecionado, o usuário pode escolher um novo
      setIsModalOpen(true);
    } else {
      alert("Selecione uma vulnerabilidade para editar.");
    }
  };

  const handleDeleteClick = async () => {
    if (vulnSelecionada && window.confirm(`Tem certeza que deseja deletar a vulnerabilidade "${vulnSelecionada.Vulnerabilidade}"?`)) {
      try {
        const result = await deleteVulnerabilidadeApi(selectedVulnType, vulnSelecionada.Vulnerabilidade);
        alert(result.message);
        setVulnSelecionada(null);
        loadVulnerabilities();
      } catch (err: any) {
        console.error("Erro ao deletar vulnerabilidade:", err);
        alert(`Erro ao deletar vulnerabilidade: ${err.message}`);
      }
    }
  };

  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  // Handler para o input de arquivo
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    } else {
      setSelectedFile(null);
    }
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validações básicas antes de enviar o arquivo ou os dados
    if (!formData.Categoria || !formData.Subcategoria || !formData.Vulnerabilidade || !formData.Descrição || !formData.Solução) {
      alert("Por favor, preencha todos os campos obrigatórios (Categoria, Subcategoria, Vulnerabilidade, Descrição, Solução).");
      return;
    }

    let imagePathToSave = formData.Imagem; // Mantém o caminho existente se não houver novo upload

    // Se um novo arquivo foi selecionado, primeiro faça o upload
    if (selectedFile) {
        // Valida que o nome da vulnerabilidade está preenchido antes de tentar fazer upload
        if (!formData.Vulnerabilidade) {
            alert("O nome da vulnerabilidade é obrigatório para fazer o upload da imagem, pois ele define o nome do arquivo.");
            return;
        }
        try {
            // Chama a API de upload, passando o arquivo e os dados para criar o caminho da pasta
            const uploadedPath = await uploadImageApi(
                selectedFile,
                formData.Categoria,
                formData.Subcategoria,
                formData.Vulnerabilidade
            );
            imagePathToSave = uploadedPath; // Atualiza o caminho da imagem com o retornado pelo backend
            alert("Imagem enviada com sucesso!");
        } catch (err: any) {
            console.error("Erro ao enviar imagem:", err);
            alert(`Erro ao enviar imagem: ${err.message}. A vulnerabilidade não será salva.`);
            return; // Interrompe o processo se o upload da imagem falhar
        }
    } else if (formMode === "add") {
        imagePathToSave = ""; // Garante que é uma string vazia se nenhum arquivo foi selecionado ao adicionar
    }

    // Prepara os dados finais a serem enviados para adicionar/atualizar a vulnerabilidade
    const finalFormData = { ...formData, Imagem: imagePathToSave };

    if (formMode === "add") {
      try {
        const result = await addVulnerabilidadeApi(selectedVulnType, finalFormData);
        alert(result.message);
        setIsModalOpen(false);
        loadVulnerabilities();
      } catch (err: any) {
        console.error("Erro ao adicionar vulnerabilidade:", err);
        alert(`Erro ao adicionar vulnerabilidade: ${err.message}`);
      }
    } else if (formMode === "edit" && vulnSelecionada) {
      try {
        const result = await updateVulnerabilidadeApi(selectedVulnType, vulnSelecionada.Vulnerabilidade, finalFormData);
        alert(result.message);
        setIsModalOpen(false);
        setVulnSelecionada(null); // Limpa a seleção após edição
        loadVulnerabilities();
      } catch (err: any) {
        console.error("Erro ao atualizar vulnerabilidade:", err);
        alert(`Erro ao atualizar vulnerabilidade: ${err.message}`);
      }
    }
  };

  // Filtra as subcategorias com base na categoria selecionada no formulário
  const subcategoriasFiltradas = categoriasDescritivas.find(
    (cat) => cat.categoria === formData.Categoria
  )?.subcategorias || [];


  return (
    <div
      className="min-h-screen bg-cover bg-center flex"
      style={{ backgroundImage: "url('/assets/fundo.png')" }}
    >
      <div className="w-1/5 bg-white-800 text-white flex items-center justify-center p-4">
        <Link to="/">
          <img
            src="/assets/logocogel.jpg"
            alt="COGEL Logo"
            className="w-32 h-auto"
          />
        </Link>
      </div>

      <div className="w-4/5 p-8 bg-white rounded-l-lg shadow-md">
        <h1 className="text-xl font-bold text-black mb-4">Gerenciar Vulnerabilidades</h1>

        {/* Botões de seleção de tipo de vulnerabilidade */}
        <div className="mb-4 flex space-x-4">
          <button
            className={`px-4 py-2 rounded-md font-medium ${
              selectedVulnType === 'sites' ? 'bg-[#007BB4] text-white' : 'bg-gray-200 text-black hover:bg-gray-300'
            }`}
            onClick={() => setSelectedVulnType('sites')}
          >
            Gerenciar Vulnerabilidades de Sites
          </button>
          <button
            className={`px-4 py-2 rounded-md font-medium ${
              selectedVulnType === 'servers' ? 'bg-[#007BB4] text-white' : 'bg-gray-200 text-black hover:bg-gray-300'
            }`}
            onClick={() => setSelectedVulnType('servers')}
          >
            Gerenciar Vulnerabilidades de Servidores
          </button>
        </div>

        {/* Barra de Pesquisa */}
        <input
          type="text"
          placeholder="Pesquisar por categoria, subcategoria ou vulnerabilidade..."
          className="w-full p-2 border border-gray-300 rounded-md mb-4 text-black"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <div className="bg-gray-100 h-80 overflow-y-auto rounded-md p-4 mb-6">
          {loading ? (
            <p className="text-gray-500">Carregando vulnerabilidades...</p>
          ) : error ? (
            <p className="text-red-500">Erro: {error}</p>
          ) : filteredVulnerabilities.length > 0 ? (
            <ul className="space-y-2">
              {filteredVulnerabilities.map((vuln) => (
                <li
                  key={vuln.Vulnerabilidade} // Assumindo nome da vulnerabilidade é único
                  className={`p-3 rounded cursor-pointer border ${
                    vulnSelecionada?.Vulnerabilidade === vuln.Vulnerabilidade
                      ? "bg-[#007BB4] text-white"
                      : "bg-white hover:bg-gray-200 text-black"
                  }`}
                  onClick={() => handleSelectVuln(vuln)}
                >
                  <p className="font-semibold">{vuln.Vulnerabilidade}</p>
                  <p className="text-sm">
                    Categoria: {vuln.Categoria} | Subcategoria: {vuln.Subcategoria}
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">Nenhuma vulnerabilidade encontrada para {selectedVulnType === 'sites' ? 'sites' : 'servidores'}.</p>
          )}
        </div>

        <div className="flex justify-end space-x-4">
          <button
            className="px-6 py-2 rounded text-white font-medium bg-green-600 hover:bg-green-700"
            onClick={handleAddClick}
          >
            Adicionar
          </button>
          <button
            className={`px-6 py-2 rounded text-white font-medium ${
              vulnSelecionada ? "bg-yellow-600 hover:bg-yellow-700" : "bg-gray-400 cursor-not-allowed"
            }`}
            disabled={!vulnSelecionada}
            onClick={handleEditClick}
          >
            Editar
          </button>
          <button
            className={`px-6 py-2 rounded text-white font-medium ${
              vulnSelecionada ? "bg-red-600 hover:bg-red-700" : "bg-gray-400 cursor-not-allowed"
            }`}
            disabled={!vulnSelecionada}
            onClick={handleDeleteClick}
          >
            Excluir
          </button>
        </div>
      </div>

      {/* Modal para Adicionar/Editar Vulnerabilidade */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-lg shadow-xl w-1/2 max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold text-black mb-4">
              {formMode === "add" ? "Adicionar Nova Vulnerabilidade" : "Editar Vulnerabilidade"}
            </h2>
            <form onSubmit={handleFormSubmit}>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="Vulnerabilidade">
                  Nome da Vulnerabilidade:
                </label>
                <input
                  type="text"
                  id="Vulnerabilidade"
                  name="Vulnerabilidade"
                  value={formData.Vulnerabilidade}
                  onChange={handleFormChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                  disabled={formMode === "edit"} // Não permite mudar o nome ao editar (chave de identificação)
                />
                {formMode === "edit" && <p className="text-xs text-gray-500 mt-1">O nome da vulnerabilidade não pode ser alterado durante a edição. Para isso, exclua e adicione novamente.</p>}
              </div>

              {/* CAMPO CATEGORIA AGORA É UM SELECT */}
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="Categoria">
                  Categoria:
                </label>
                <select
                  id="Categoria"
                  name="Categoria"
                  value={formData.Categoria}
                  onChange={handleFormChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                >
                  <option value="">Selecione uma Categoria</option>
                  {categoriasDescritivas.map((cat) => (
                    <option key={cat.categoria} value={cat.categoria}>
                      {cat.categoria}
                    </option>
                  ))}
                </select>
              </div>

              {/* CAMPO SUBCATEGORIA AGORA É UM SELECT DEPENDENTE */}
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="Subcategoria">
                  Subcategoria:
                </label>
                <select
                  id="Subcategoria"
                  name="Subcategoria"
                  value={formData.Subcategoria}
                  onChange={handleFormChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  required
                  disabled={!formData.Categoria} // Desabilita se nenhuma categoria for selecionada
                >
                  <option value="">Selecione uma Subcategoria</option>
                  {subcategoriasFiltradas.map((subcat) => (
                    <option key={subcat.subcategoria} value={subcat.subcategoria}>
                      {subcat.subcategoria}
                    </option>
                  ))}
                </select>
                {!formData.Categoria && <p className="text-xs text-gray-500 mt-1">Selecione uma categoria primeiro para ver as subcategorias.</p>}
              </div>

              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="Descrição">
                  Descrição:
                </label>
                <textarea
                  id="Descrição"
                  name="Descrição"
                  value={formData.Descrição}
                  onChange={handleFormChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-24"
                  required
                ></textarea>
              </div>

              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="Solução">
                  Solução:
                </label>
                <textarea
                  id="Solução"
                  name="Solução"
                  value={formData.Solução}
                  onChange={handleFormChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-24"
                  required
                ></textarea>
              </div>

              {/* CAMPO DE UPLOAD DA IMAGEM */}
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="ImagemUpload">
                  Upload da Imagem (PNG, JPG, JPEG, GIF):
                </label>
                <input
                  type="file"
                  id="ImagemUpload"
                  name="ImagemUpload"
                  accept=".png,.jpg,.jpeg,.gif"
                  onChange={handleFileChange}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                />
                {/* Exibe o caminho da imagem atual se estiver em modo de edição e houver uma imagem */}
                {formMode === "edit" && formData.Imagem && !selectedFile && (
                    <p className="text-sm text-gray-600 mt-2">
                        Imagem atual: <a href={`/${formData.Imagem}`} target="_blank" rel="noopener noreferrer" className="text-[#007BB4] hover:underline">{formData.Imagem}</a>
                    </p>
                )}
                {/* Exibe o nome do arquivo selecionado para upload */}
                {selectedFile && (
                    <p className="text-sm text-gray-600 mt-2">
                        Arquivo selecionado: {selectedFile.name}
                    </p>
                )}
              </div>

              <div className="flex justify-end space-x-4 mt-6">
                <button
                  type="button"
                  className="px-6 py-2 rounded text-black font-medium bg-gray-300 hover:bg-gray-400"
                  onClick={() => setIsModalOpen(false)}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 rounded text-white font-medium bg-[#007BB4] hover:bg-[#009BE2]"
                >
                  {formMode === "add" ? "Adicionar" : "Salvar Alterações"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GerenciarVulnerabilidades;