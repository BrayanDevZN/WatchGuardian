#pragma once

#include "estoque/utils.hpp"
#include "../models.hpp"
#include <unordered_map>
#include <optional>

namespace estoque {

class ProdutoNaoEncontrado : public std::runtime_error {
public:
    explicit ProdutoNaoEncontrado(const std::string& message) : std::runtime_error(message) {}
};

class EstoqueInsuficiente : public std::runtime_error {
public:
    explicit EstoqueInsuficiente(const std::string& message) : std::runtime_error(message) {}
};

struct Produto {
    std::string codigo;
    int quantidade;
    double valor;

    double valor_total() const { return quantidade * valor; }
};

class Estoque {
public:
    void adicionar(const Produto& produto);
    Produto obter(const std::string& codigo) const;
    void retirar(const std::string& codigo, int quantidade);
    std::vector<Produto> buscar(const std::string& texto) const;
    double valor_total() const;

private:
    std::unordered_map<std::string, Produto> produtos;
};

} // namespace estoque