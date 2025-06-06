import { Routes, Route, useNavigate } from 'react-router-dom';

import ScansPage from './pages/Scans';
import PesquisarScanWAS from './pages/PesquisarScanWAS';
import Relatorios from './pages/Relatorios';
import GerarRelatorio from './pages/GerarRelatorio';
import GerarRelatorioFinal from './pages/GerarRelatorioFinal';
import ListaDeScans from './pages/ListaDeScans';
import EditarLista from './pages/EditarLista';
import CriarLista from './pages/CriarLista';
import PesquisarScansVM from './pages/PesquisarScanVM';
import RelatoriosGerados from './pages/RelatoriosGerados';
import GerenciarVulnerabilidades from './pages/GerenciarVulnerabilidades'; 



function Home() {
  const navigate = useNavigate();

  return (
    <div
      className="min-h-screen bg-cover bg-center text-white"
      style={{ backgroundImage: "url('/assets/fundo.png')" }}
    >
      {/* Top Bar com Logo */}
      <div className="absolute top-4 left-4"> {/* Adicionado um pequeno padding */}
        <img
          src="/assets/logocogel.jpg"
          alt="COGEL Logo"
          className="w-38 h-auto"
        />
      </div>

      {/* Conteúdo Central */}
      <div className="flex justify-center items-center h-[calc(100vh-64px)]">
        <div className="flex space-x-12"> {/* Espaçamento entre os itens */}
          {/* Relatórios */}
          <div
            className="bg-white rounded-lg p-6 text-center text-black shadow-lg hover:scale-105 transition-transform 
                       w-40 h-40 cursor-pointer flex flex-col items-center justify-center" // <-- Alterado para w-48 h-48 e adicionado flexbox para centralização
            id="relatorios"
            onClick={() => navigate('/relatorios')}
          >
            <img
              src="/assets/icone-relatorios.png"
              alt="Relatórios"
              className="w-16 h-16 mx-auto mb-2"
            />
            <p className="text-lg font-medium">Relatórios</p>
          </div>

          {/* Scans */}
          <div
            className="bg-white rounded-lg p-6 text-center text-black shadow-lg hover:scale-105 transition-transform 
                       w-40 h-40 cursor-pointer flex flex-col items-center justify-center" // <-- Alterado para w-48 h-48 e adicionado flexbox para centralização
            id="scans"
            onClick={() => navigate('/scans')}
          >
            <img
              src="/assets/icone-scan.png"
              alt="Scans"
              className="w-18 h-16 mx-auto mb-2"
            />
            <p className="text-lg font-medium">Scans</p>
          </div>

          {/* Gerenciar Vulnerabilidades */}
          <div
            className="bg-white rounded-lg p-6 text-center text-black shadow-lg hover:scale-105 transition-transform 
                       w-40 h-40 cursor-pointer flex flex-col items-center justify-center" // <-- Alterado para w-48 h-48 e adicionado flexbox para centralização
            id="gerenciar-vulnerabilidades"
            onClick={() => navigate('/gerenciar-vulnerabilidades')}
          >
            <img
              src="/assets/icone-gerenciar-vulnerabilidades.png" // Seu novo ícone
              alt="Gerenciar Vulnerabilidades"
              className="w-16 h-16 mx-auto mb-2"
            />
            <p className="text-lg font-medium">Gerenciar Vulnerabilidades</p>
          </div>


        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/scans" element={<ScansPage />} />
      <Route path="/webapp-scans" element={<PesquisarScanWAS />} />
      <Route path="/relatorios" element={<Relatorios />} />
      <Route path="/gerar-relatorio" element={<GerarRelatorio />} />
      <Route path="/gerar-relatorio/:idLista" element={<GerarRelatorioFinal />} />
      <Route path="/lista-de-scans" element={<ListaDeScans />} />
      <Route path="/editar-lista" element={<EditarLista />} />
      <Route path="/criar-lista" element={<CriarLista />} />
      <Route path="/vm-scans" element={<PesquisarScansVM />} />
      <Route path="/relatorios-gerados" element={<RelatoriosGerados />} />
      <Route path="/gerenciar-vulnerabilidades" element={<GerenciarVulnerabilidades />} /> {/* <-- Adicione esta linha */}
      {/* Adicione outras rotas aqui */}
        </Routes>
  );
}

export default App;