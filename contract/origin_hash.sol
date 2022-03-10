// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Storage {
    uint ultimo_id_dado;
    address private proprietario;
   
    struct Dado {
        uint id_blockchain;
        string info;
    }
    mapping(uint => Dado) dados;
    event Dado_Registrado(uint id_blockchain);

    event Proprietario_Registrado(address indexed velhoProprietario, address indexed novoProprietario);
    
    modifier isDado(uint _id_dado) {
        require(dados[_id_dado].id_blockchain > 0, "Recurso Inexistente!");
        _;
    }
    modifier isProprietario() {
        require(msg.sender == proprietario, "Usuario invalido");
        _;
    }
    
    constructor() {
        ultimo_id_dado = 0;
        proprietario = msg.sender;
        emit Proprietario_Registrado(address(0), proprietario);
    }
    
    function setProprietario(address novoProprietario) public isProprietario {
        emit Proprietario_Registrado(proprietario, novoProprietario);
        proprietario = novoProprietario;
    }

    function getProprietario() external view returns (address) {
        return proprietario;
    }
    
    function addInfo(string memory _info) public isProprietario {
        ultimo_id_dado = ultimo_id_dado + 1;
        dados[ultimo_id_dado] = Dado(
            {id_blockchain: ultimo_id_dado,
            info: _info});
        emit Dado_Registrado(ultimo_id_dado);
    }

    function seeInfo(uint _id) public view isDado(_id) isProprietario
        returns (string memory info){
                info = dados[_id].info;
    }
}

 