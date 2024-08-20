#include "core.h"

int main() {
    std::vector<Rule> rules = {
            {1,   {{0,  1, 1, 1, 0},
                          {3, 2, 22, 22, 0}}, 2},
            {128, {{0,  1, 2, 2, 0},
                          {2, 1, 3, 3, 0},
                          {5, 2, 80, 80, 0},
                          {11, 4, 180184321, 180184575, 0},
                  },
                                            4},
            {3,   {{27, 1, 6, 6, 0},
                          {2, 1, 0, 2, 1}}, 2},

    };

    vector<vector<uint8_t>> packets = {
            {1, 2, 0, 22,  0, 23, 0, 1, 101, 189, 10, 255, 101,
                                                                189, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                       0, 0, 6, 0, 0, 0,
                                                                                                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            },
            {2, 0, 3, 142, 2, 80, 0, 1, 101, 189, 10, 250, 101,
                                                                189, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0,
                                                                                                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            },
            {2, 0, 3, 142, 2, 80, 0, 1, 101, 189, 10, 250, 101, 189, 10,
                                                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0,
                                                                                                                                     0, 0, 0, 0, 0, 0, 0, 0, 0},
            {3, 0, 3, 142, 2, 80, 0, 1, 101, 189, 10, 250, 101, 189, 10,
                                                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0,
                                                                                                                                     0, 0, 0, 0, 0, 0, 0, 0, 0}
    };

    for (auto rule: rules) {
        AddRule(&rule);
    }


    for (auto packet: packets) {
        uint8_t actions[10] = {};
        Process(packet.data(), actions, sizeof actions);
        for (auto value: actions) {
            if (value != 0) {
                cout << (uint32_t) value << " ";
            }
        }
        cout << std::endl;
    }
    return 0;
}