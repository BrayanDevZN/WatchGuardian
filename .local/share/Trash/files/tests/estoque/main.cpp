#include "models.hpp"
#include "servico.hpp"
#include "utils.hpp"
#include <iostream>
#include <unordered_map>

int main() {
    Estoque estoque;
    estoque.adicionar(Produto("A1", "Teclado", 150.0, 10));
    estoque.adicionar(Produto("B2", "Mouse", 80.5, 25));
    estoque.adicionar(Produto("C3", "Monitor", 900.0, 4));
    estoque.adicionar(Produto("A1", "Teclado", 150.0, 5));

    std::cout << linha() << std::endl;
    for (const auto& produto : estoque.produtos) {
        std::cout << produto.second << std::endl;
    }
    std::cout << linha() << std::endl;

    try {
        estoque.retirar("B2", 5);
        estoque.retirar("C3", 10);
    } catch (const EstoqueError& erro) {
        std::cout << "Erro: " << erro.what() << std::endl;
    }

    std::cout << "Busca 'mo': " << estoque.buscar("mo") << std::endl;
    std::cout << "Valor total: " << formatar_moeda(estoque.valor_total()) << std::endl;

    return 0;
}
