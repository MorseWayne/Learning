//
// Created by q00576748 on 2024/7/29.
//
#include <cstdint>
#include <cstring>
#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <vector>
#include <unistd.h>
#include <unordered_set>

using namespace std;

#define LEN1_TO_UINT64(msg) ((uint64_t) * ((const uint8_t*)msg))
#define LEN2_TO_UINT64(msg) ((uint64_t) * ((const uint16_t*)msg))
#define LEN4_TO_UINT64(msg) ((uint64_t) * ((const uint32_t*)msg))
#define LEN6_TO_UINT64(arr)                                                                              \
    ((uint64_t)arr[0] << 40 | (uint64_t)arr[1] << 32 | (uint64_t)arr[2] << 24 | (uint64_t)arr[3] << 16 | \
     (uint64_t)arr[4] << 8 | (uint64_t)arr[5])
#define LEN8_TO_UINT64(msg) (*((const uint64_t*)msg))

#define MAX_COND_NUM 8

struct Condition {
    uint16_t offset{0};
    uint8_t len{0};
    uint64_t min{0};
    uint64_t max{0};
    uint8_t nott{0};
    uint32_t condId{0};
    uint32_t ruleId{0};
    bool isMatch{false};
};

struct Rule {
    uint8_t action;                // 动作id
    Condition cond[MAX_COND_NUM];  // 规则列表
    uint8_t condNum;               // 规则数量
};

struct RuleEx {
    uint8_t action;                // 动作id
    vector<uint32_t> cond;  // 规则列表
    uint32_t ruleId{0};
};

vector<RuleEx> g_rules;
vector<Condition> g_conditions;
uint32_t g_totalRuleNum = 0;

constexpr uint8_t MAX_OFFSET = 64;
constexpr uint8_t MAX_LEN = 8;

uint64_t g_cachedResult[MAX_OFFSET][MAX_LEN]{0};
uint8_t g_hasCached[MAX_OFFSET][MAX_LEN]{0};
unordered_map<uint16_t, vector<uint32_t>> g_conflictRelations;
unordered_map<uint16_t, vector<uint32_t>> g_containedRelations;
unordered_map<uint16_t, std::unordered_map<uint16_t, vector<uint32_t>>> g_category;
uint8_t* g_isNotMatch{nullptr};

uint64_t extractValue(const uint8_t *packet, uint16_t offset, uint8_t len) {
    packet = packet + offset;
    switch (len) {
        case 1: {
            return LEN1_TO_UINT64(packet);
        }
        case 2: {
            return LEN2_TO_UINT64(packet);
        }
        case 4: {
            return LEN4_TO_UINT64(packet);
        }
        case 6: {
            return LEN6_TO_UINT64(packet);
        }
        case 8: {
            return LEN8_TO_UINT64(packet);
        }
        default:
            return 0;
    }
}

bool matchCondition(const Condition &cond, const uint8_t *packet) {

    uint64_t value = 0;
    if (g_hasCached[cond.offset][cond.len] == 1) {
        value = g_cachedResult[cond.offset][cond.len];
    } else {
        value = extractValue(packet, cond.offset, cond.len);
        g_hasCached[cond.offset][cond.len] = 1;
        g_cachedResult[cond.offset][cond.len] = value;
    }

    if (cond.nott == 1) {
        // Non-match
        return value < cond.min || value > cond.max;
    } else {
        // Normal match
        return value >= cond.min && value <= cond.max;
    }
}

void Init(uint32_t ruleNum) {
    g_rules.clear();
    g_rules.reserve(ruleNum);

    g_conditions.clear();
    g_conditions.reserve(ruleNum * MAX_COND_NUM);

    g_totalRuleNum = ruleNum;

    g_isNotMatch = new uint8_t[ruleNum];
}

void Predict() {
    cout << "start predict" << std::endl;
    for (const auto &[offset, condIdByLen]: g_category) {
        for (auto &[len, condIds]: condIdByLen) {
            uint32_t conflictNum = 0;
            for (int i = 0; i < condIds.size(); ++i) {
                auto srcCondId = condIds[i];
                auto &srcCond = g_conditions[srcCondId];
                for (int j = i + 1; j < condIds.size(); ++j) {
                    auto destCondId = condIds[j];
                    auto &destCond = g_conditions[destCondId];
                    // 两个条件的区间不重叠
                    if (srcCond.max < destCond.min || destCond.max < srcCond.min) {
                        if (srcCond.nott == 0 && destCond.nott == 0) {
                            g_conflictRelations[srcCondId].push_back(destCondId);
                            conflictNum++;
                        }
                        // dest区间包含src
                    }
//                    else if (srcCond.min >= destCond.min && srcCond.max <= destCond.max) {
//                        if (srcCond.nott == 0 && destCond.nott == 0) {
//                            g_containedRelations[srcCondId].push_back(destCondId);
//                        } else if (srcCond.nott == 0 && destCond.nott == 1) {
//                            g_conflictRelations[srcCondId].push_back(destCondId);
//                            conflictNum++;
//                        }
//                        // src区间包含dest
//                    } else if (srcCond.min <= destCond.min && srcCond.max >= destCond.max) {
//                        if (srcCond.nott == 0 && destCond.nott == 0) {
//                            g_containedRelations[srcCondId].push_back(destCondId);
//                        } else if (srcCond.nott == 1 && destCond.nott == 0) {
//                            g_conflictRelations[srcCondId].push_back(destCondId);
//                            conflictNum++;
//                        }
//                    }

                }
                cout << "index: " << i << ", conflict size: "
                     << g_conflictRelations[srcCondId].size()
                     << std::endl;
                cout << "index: " << i << ", contained size: "
                     << g_containedRelations[srcCondId].size()
                     << std::endl;
                if (conflictNum > 500) {
                    break;
                }
            }
        }
    }
    cout << "end predict" << std::endl;
}

// 实现该函数，会循环调用，逐个添加所有规则，不要直接保存入参的rule指针，该函数耗时不计分
void AddRule(const Rule *rule) {
    RuleEx ruleEx;
    ruleEx.action = rule->action;
    auto ruleId = g_rules.size();
    for (int i = 0; i < rule->condNum; ++i) {
        auto &cond = rule->cond[i];
        g_conditions.push_back(cond);

        auto condId = g_conditions.size() - 1;
        g_conditions[condId].condId = condId;
        g_conditions[condId].ruleId = ruleId;

        ruleEx.cond.push_back(condId);

        // 根据offset len分类
        g_category[cond.offset][cond.len].push_back(condId);

    }
    ruleEx.ruleId = g_rules.size();
    g_rules.push_back(ruleEx);

    if (g_rules.size() == g_totalRuleNum) {
        Predict();
    }
}

void ProcNonMatch(uint32_t condId) {
    if (g_containedRelations.count(condId) > 0) {
        auto &relations = g_containedRelations[condId];
        for (uint32_t id: relations) {
            g_conditions[id].isMatch = true;
        }
    }
}

void ProcMatch(uint32_t condId) {
    if (g_conflictRelations.count(condId) > 0) {
        auto &conflictRelations = g_conflictRelations[condId];
        for (uint32_t id: conflictRelations) {
            auto ruleId = g_conditions[id].ruleId;
            g_isNotMatch[ruleId] = 1;
        }
    }
}


// 实现该函数，报文匹配规则，msg是报文首地址，actions为输出，执行的动作放入actions中，maxLen为actions数组的最大长度
void Process(const void *msg, uint8_t *actions, uint32_t maxLen) {
    memset(g_cachedResult, 0, sizeof(g_cachedResult));
    memset(g_hasCached, 0, sizeof g_hasCached);
    memset(g_isNotMatch, 0, g_totalRuleNum);

    uint32_t index = 0;

    for (const auto &rule: g_rules) {
        if (g_isNotMatch[rule.ruleId]) {
            continue;
        }
        bool ruleMatched = true;
        for (auto &condId: rule.cond) {
            auto &cond = g_conditions[condId];
            if (!matchCondition(cond, static_cast<const uint8_t *>(msg))) {
                ruleMatched = false;
                break;
            } else {
                ProcMatch(condId);
            }
        }

        if (ruleMatched) {
            if (index < maxLen) {
                actions[index++] = rule.action;
            }
            if (rule.action <= 127) {
                break;  // Stop processing further rules
            }
        }
    }
}
