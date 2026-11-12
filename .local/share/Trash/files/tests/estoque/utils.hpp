#pragma once

#include <string>
#include <vector>
#include <optional>
#include "../models.hpp"

namespace estoque {

class Produto;

bool contem(const std::string& texto, const std::string& busca);

} // namespace estoque