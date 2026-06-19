/*
 * Bug: std::sort requires random-access iterators, but std::map iterators
 * are bidirectional. Must copy to vector first.
 * Compile: g++ -std=c++17 -o ex5_buggy ex5_buggy.cpp
 */
#include <iostream>
#include <map>
#include <vector>
#include <string>
#include <algorithm>

int main() {
    std::map<std::string, std::vector<int>> gradebook = {
        {"alice",   {90, 85, 92}},
        {"bob",     {78, 88}},
        {"charlie", {95, 70, 80}},
    };

    std::map<std::string, int> averages;
    for (auto& [name, scores] : gradebook) {
        int sum = 0;
        for (int s : scores) sum += s;
        averages[name] = sum / scores.size();
    }

    // BUG: cannot std::sort on map iterators (not random-access)
    // std::sort(averages.begin(), averages.end());

    // FIX: copy to vector of pairs
    std::vector<std::pair<std::string, int>> sorted(averages.begin(), averages.end());
    std::sort(sorted.begin(), sorted.end(),
        [](const auto& a, const auto& b) { return a.second > b.second; });

    std::cout << "Rankings:" << std::endl;
    for (auto& [name, avg] : sorted) {
        std::cout << "  " << name << ": " << avg << std::endl;
    }

    return 0;
}
