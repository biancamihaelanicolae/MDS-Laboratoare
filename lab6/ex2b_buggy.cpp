/*
 * Buggy version. Bug: range-for iterates over to_install while push_back
 * can invalidate iterators. Use address sanitizer to detect.
 * Compile: g++ -std=c++17 -fsanitize=address -o ex2b_buggy ex2b_buggy.cpp && ./ex2b_buggy
 */
#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <string>

int main() {
    std::map<std::string, std::vector<std::string>> deps = {
        {"curl",    {"openssl", "nghttp2"}},
        {"openssl", {"zlib", "libcrypt"}},
        {"nghttp2", {"zlib"}},
        {"python",  {"zlib", "libffi", "readline"}},
    };

    std::cout << "Resolving dependencies... \n";
    std::vector<std::string> to_install = {"curl", "python", "vim"};
    std::set<std::string> seen(to_install.begin(), to_install.end());

    // BUG: range-for invalidated when push_back reallocates
    for (const auto& pkg : to_install) {
        if (deps.count(pkg)) {
            for (const auto& dep : deps[pkg]) {
                if (seen.insert(dep).second) {
                    to_install.push_back(dep);
                }
            }
        }
    }

    std::cout << "Packages to install: " << to_install.size() << " packages" << std::endl;
    for (const auto& pkg : to_install) {
        std::cout << "  installing " << pkg << std::endl;
    }
    std::cout << "done." << std::endl;
    return 0;
}
