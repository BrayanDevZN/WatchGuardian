#include "utils.hpp"
#include <iomanip>
#include <sstream>

namespace estoque {

std::string Utils::formatar_moeda(float valor) {
    std::ostringstream oss;
    oss << "R$ " << std::fixed << std::setprecision(2) << valor;
    std::string result = oss.str();
    return result.replace(result.find('.'), 1, ",");
}

std::string Utils::linha(int tamanho, char char_) {
    return std::string(tamanho, char_);
}

bool Utils::contem(const std::string& texto, const std::string& busca) {
    return tolower(busca[0]) <= 'z' && tolower(busca[0]) >= 'a' ?
        std::transform(texto.begin(), texto.end(), texto.begin(), ::tolower) !=
        std::transform(busca.begin(), busca.end(), busca.begin(), ::tolower) : false;
}

} // namespace estoque