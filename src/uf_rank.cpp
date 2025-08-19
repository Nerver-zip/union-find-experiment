#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <chrono>
#include <filesystem>

using namespace std;
using namespace std::chrono;

class UnionFind {
private:
    vector<int> parent;
    vector<int> rank;
public:
    UnionFind(int n) : parent(n), rank(n,0) {
        for (int i = 0; i < n; ++i) 
            parent[i] = i;
    }

    int find(int x) {
        while (x != parent[x]) {
            parent[x] = parent[parent[x]]; 
            x = parent[x];
        }
        return x;
    }

    void unite(int x, int y) {
        int rx = find(x), ry = find(y);
        if (rx == ry) return;

        if (rank[rx] < rank[ry]) parent[rx] = ry;
        else if (rank[rx] > rank[ry]) parent[ry] = rx;
        else { parent[ry] = rx; ++rank[rx]; }
    }
};

int main(int argc, char* argv[]) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (argc < 3) {
        cerr << "Uso: " << argv[0] << " <input_file> <output_csv>\n";
        return 1;
    }

    string input_file = argv[1];
    string output_file = argv[2];

    ifstream fin(input_file);
    if (!fin) {
        cerr << "Erro ao abrir arquivo\n";
        return 1;
    }

    int num_nodes;
    fin >> num_nodes;
    fin.ignore(numeric_limits<streamsize>::max(), '\n'); // pular primeira linha

    string workload_label;
    getline(fin, workload_label); // segunda linha: label do workload

    vector<vector<int>> ops;
    string line;
    while (getline(fin, line)) {
        if (line.empty()) continue;
        stringstream ss(line);
        int a, b;
        ss >> a;
        if (ss >> b)
            ops.push_back({a, b});
        else
            ops.push_back({a});
    }
    fin.close();

    UnionFind uf(num_nodes);

    auto start = steady_clock::now();
    for (auto &op : ops) {
        if (op.size() == 1)
            uf.find(op[0]);
        else
            uf.unite(op[0], op[1]);
    }
    auto end = steady_clock::now();
    auto duration_us = duration_cast<microseconds>(end - start).count();

    bool write_header = !filesystem::exists(output_file);
    ofstream fout(output_file, ios::app);
    if (write_header)
        fout << "impl,workload_label,num_nodes,num_ops,time_us\n";

    fout << "UF-Rank," << workload_label << "," << num_nodes << "," << ops.size() << "," << duration_us << "\n";
    fout.close();

    return 0;
}
