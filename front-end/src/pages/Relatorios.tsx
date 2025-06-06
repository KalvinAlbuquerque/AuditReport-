import { Link } from "react-router-dom";  

const Relatorios = () => {
  return (
    <div
      className="min-h-screen bg-cover bg-center flex"
      style={{ backgroundImage: "url('/assets/fundo.png')" }}
    >
      {/* Sidebar azul à esquerda */}
      <div className="w-1/5 bg-white-800 text-white flex items-center justify-center p-4">
      <Link to="/">
      <img
        src="/assets/logocogel.jpg"
        alt="COGEL Logo"
        className="w-32 h-auto"
      />
      </Link>
    </div>

      {/* Conteúdo central */}
      <div className="w-4/5 flex items-center justify-center bg-white">
        <div className="grid grid-cols-2 gap-20 text-center">
          {/* Item 1 */}
          
          <Link to="/relatorios-gerados">
          <div className="hover:scale-105 transition">
            <img src="/assets/gerados.png" alt="Relatórios Gerados" className="mx-auto h-30 mb-4 cursor-pointer" />
            <p className="text-black font-medium !font-black">Relatórios Gerados</p>
          </div>
          </Link>
          

          {/* Item 2 */}
          <Link to="/gerar-relatorio">
          <div className="hover:scale-105 transition">
            <img src="/assets/gerar.png" alt="Gerar Relatórios" className="mx-auto h-30 mb-4 cursor-pointer" />
            <p className="text-black font-medium !font-black">Gerar Relatórios</p>
          </div>
          </Link>
          

        </div>
      </div>
    </div>
  );
};

export default Relatorios;