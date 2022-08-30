// Copyright (C) 2022 Pattern Labs, Inc - All Rights Reserved
//   Unauthorized copying of this file, via any medium is strictly prohibited
//   Proprietary and confidential

// This file contains some pattern-specific SWIG utility macros.

%include "std_string.i"

%define %printable(TypeName)
%ignore operator<<(std::ostream&, const TypeName&);
%extend TypeName {
    std::string __repr__() const {
         std::ostringstream out;
         out << *$self;
         return out.str();
    }        
}
%enddef

%define %equality_comparable(TypeName)
%ignore operator==(const TypeName&, const TypeName&);
%ignore operator!=(const TypeName&, const TypeName&);
%extend TypeName {
    bool __eq__(const TypeName& other) const {
        return *$self == other;
    }  
    bool __ne__(const TypeName& other) const {
        return *$self != other;
    }       
}
%enddef

%define %multiplicable(LhsTypeName, RhsTypeName)
%ignore operator*(const LhsTypeName&, const RhsTypeName&);
%extend RhsTypeName {
    RhsTypeName __mul__(const LhsTypeName& other) const {
        return other * *$self;
    }       
}
%enddef
