//
// Created by q00576748 on 2024/7/29.
//
#include <cstdint>
#include <cstring>
#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>

using namespace std;

#define LEN1_TO_UINT64(msg) ((uint64_t) * ((const uint8_t *)msg))
#define LEN2_TO_UINT64(msg) ((uint64_t) * ((const uint16_t *)msg))
#define LEN4_TO_UINT64(msg) ((uint64_t) * ((const uint32_t *)msg))
#define LEN6_TO_UINT64(arr)                                                   \
  ((uint64_t)arr[0] << 40 | (uint64_t)arr[1] << 32 | (uint64_t)arr[2] << 24 | \
   (uint64_t)arr[3] << 16 | (uint64_t)arr[4] << 8 | (uint64_t)arr[5])
#define LEN8_TO_UINT64(msg) (*((const uint64_t *)msg))

#define MAX_COND_NUM 8

struct Condition {
    uint16_t offset{0};
    uint8_t len{0};
    uint64_t min{0};
    uint64_t max{0};
    uint8_t nott{0};

    uint64_t getRange() const {
        uint64_t range = (max - min);
        if (nott) {
            range = UINT64_MAX - range;
        }
        return range;
    }

    // 重载小于运算符用于 set 的排序
    bool operator<(const Condition &other) const {

        uint32_t range = (max - min);
        if (nott) {
            range = UINT64_MAX - range;
        }

        // 如果 len 相同，比较 max - min
        // 范围小的排在前面
        auto leftRange = getRange();
        auto rightRange = other.getRange();
        if (leftRange != rightRange) {
            return leftRange < rightRange;
        }

        // 先比较 len，len 越大优先级越高
        if (len != other.len) {
            return len > other.len;
        }

        // 如果 len 和 max - min 相同，比较 offset
        return offset < other.offset;
    }
};

struct Rule {
    uint8_t action;                // 动作id
    Condition cond[MAX_COND_NUM];  // 规则列表
    uint8_t condNum;               // 规则数量
};

struct RuleEx {
    uint8_t action;                // 动作id
    std::set<Condition> cond;
};

vector<RuleEx> g_rules;
std::unordered_map<uint32_t, std::unordered_map<uint32_t, uint64_t>> g_cachedValues;

uint64_t extractValue(const uint8_t *packet, uint16_t offset, uint8_t len) {

    if (g_cachedValues.count(offset) != 0 && g_cachedValues.at(offset).count(len) != 0) {
        return g_cachedValues.at(offset).at(len);
    }

    uint64_t value = 0;
    packet = packet + offset;
    switch (len) {
        case 1: {
            value = LEN1_TO_UINT64(packet);
            break;
        }
        case 2: {
            value = LEN2_TO_UINT64(packet);
            break;
        }
        case 4: {
            value = LEN4_TO_UINT64(packet);
            break;
        }
        case 6: {
            value = LEN6_TO_UINT64(packet);
            break;
        }
        case 8: {
            value = LEN8_TO_UINT64(packet);
            break;
        }
        default:
            return 0;
    }
    g_cachedValues[offset][len] = value;
    return value;
}

bool matchCondition(const Condition &cond, const uint8_t *packet) {
    uint64_t value = extractValue(packet, cond.offset, cond.len);
    if (cond.nott == 1) {
        // Non-match
        return value < cond.min || value > cond.max;
    } else {
        // Normal match
        return value >= cond.min && value <= cond.max;
    }
}

void Init() { g_rules.clear(); }

// 实现该函数，会循环调用，逐个添加所有规则，不要直接保存入参的rule指针，该函数耗时不计分
void AddRule(const Rule *rule) {
    RuleEx ruleEx;
    ruleEx.action = rule->action;
    for (int i = 0; i < rule->condNum; ++i) {
        ruleEx.cond.insert(rule->cond[i]);
    }

    g_rules.push_back(ruleEx);
}

// 实现该函数，报文匹配规则，msg是报文首地址，actions为输出，执行的动作放入actions中，maxLen为actions数组的最大长度
void Process(const void *msg, uint8_t *actions, uint32_t maxLen) {
    g_cachedValues.clear();

    vector<uint8_t> results;
    for (const auto &rule: g_rules) {
        bool ruleMatched = true;
        for (auto &cond: rule.cond) {
            if (!matchCondition(cond, static_cast<const uint8_t *>(msg))) {
                ruleMatched = false;
                break;
            }
        }
        if (ruleMatched) {
            if (results.size() < maxLen) {
                results.push_back(rule.action);
            } else {
                break;
            }

            if (rule.action <= 127) {
                break;  // Stop processing further rules
            }
        }
    }

    if (!results.empty()) {
        std::memcpy(actions, results.data(), results.size());
    }
}
