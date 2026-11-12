#pragma once

#include <string>
#include <optional>

struct Produto {
    std::string codigo;
    std::string nome;
    double preco;
    int quantidade = 0;

    Produto(std::string codigo, std::string nome, double preco, int quantidade = 0) : codigo(codigo), nome(nome), preco(preco), quantidade(quantidade) {}

    double valor_total() const {
        return preco * quantidade;
    }

    std::string to_string() const {
        return codigo + " | " + nome + " | R$ " + std::to_string(preco) + " | qtd: " + std::to_string(quantidade);
    }
};
