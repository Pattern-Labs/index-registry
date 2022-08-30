// Copyright (C) 2022 Pattern Labs, Inc - All Rights Reserved
//   Unauthorized copying of this file, via any medium is strictly prohibited
//   Proprietary and confidential

#pragma once

#include <vector>

// This file exists as a placeholder to more-easily support future replacements
// of the glog library.
#include <ostream>
#include <stdexcept>

#include <glog/logging.h>

class LogMessageRaise : public google::LogMessage {
 public:
  LogMessageRaise(const char* file, int line)
      : google::LogMessage(file, line, google::GLOG_ERROR) {}
  LogMessageRaise(const char* file, int line,
                  const google::CheckOpString& result)
      : google::LogMessage(file, line, result) {}
  ~LogMessageRaise() noexcept(false) __attribute__((noreturn)) {
    Flush();
    throw std::runtime_error("Exception Log");
  }
};

#define RAISE_LOG LogMessageRaise(__FILE__, __LINE__).stream()
#define RAISE_LOG_IF(condition) \
  if (condition) RAISE_LOG

#define RCHECK(condition) \
  RAISE_LOG_IF(!(condition)) << "Check failed: " #condition " "

#define RCHECK_OP(a, b, op) \
  RAISE_LOG_IF(!((a)op(b))) << "Check failed: " #a " " #op " " #b " "

#define RCHECK_EQ(a, b) RCHECK_OP(a, b, ==)
#define RCHECK_NE(a, b) RCHECK_OP(a, b, !=)
#define RCHECK_GT(a, b) RCHECK_OP(a, b, >)
#define RCHECK_GE(a, b) RCHECK_OP(a, b, >=)
#define RCHECK_LT(a, b) RCHECK_OP(a, b, <)
#define RCHECK_LE(a, b) RCHECK_OP(a, b, <=)

template <typename ElementT>
std::ostream& operator<<(std::ostream& os, const std::vector<ElementT>& vec) {
  bool first = true;
  os << "[";
  for (const ElementT& element : vec) {
    os << (first ? "" : ", ") << element;
    first = false;
  }
  os << "]";
  return os;
}
