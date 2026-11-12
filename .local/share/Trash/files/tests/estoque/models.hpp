#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <optional>

struct Produto {
    std::string codigo;
    std::string nome;
    double preco;
    int quantidade;
};

struct Estoque {
    void adicionar(const Produto& produto);
    void retirar(const std::string& codigo, int quantidade);
    std::vector<Produto> buscar(const std::string& termo) const;
    double valor_total() const;
};
