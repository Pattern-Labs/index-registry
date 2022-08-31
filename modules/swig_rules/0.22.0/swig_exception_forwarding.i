// Copyright (C) 2022 Pattern Labs, Inc - All Rights Reserved
//   Unauthorized copying of this file, via any medium is strictly prohibited
//   Proprietary and confidential

%include "exception.i"

%exception {
  try {
    $action
  }
  SWIG_CATCH_STDEXCEPT 
  catch (...) {
    SWIG_exception(SWIG_UnknownError, "unknown exception");
  }
}
