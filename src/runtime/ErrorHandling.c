//
//  ErrorHandling.c
//  
//
//  Created by minxing on 2019/3/21.
//
#include <stdio.h>
#include <stdlib.h>
#include "ErrorHandling.h"

#define REPORT_ERROR_PROTO(type, msg)         \
  void report_error_##type() {                \
    fprintf(stderr, "Error in %s.\n", msg);   \
    abort();                                  \
  }

REPORT_ERROR_PROTO(malloc_space, "mallocing space")
REPORT_ERROR_PROTO(read_file, "reading file")
REPORT_ERROR_PROTO(write_file, "writing file")
REPORT_ERROR_PROTO(make_dir, "creating a new directory")
