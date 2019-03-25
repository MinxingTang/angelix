//
//  ErrorHandling.h
//
//  Handling dynamic memory alloc errors and file write/read errors
//
//  Created by Minxing on 2019/3/21.
//

#ifndef ERROR_HANDLING_h
#define ERROR_HANDLING_h

void report_error_malloc_space();
void report_error_read_file();
void report_error_write_file();
void report_error_make_dir();

#endif /* ERROR_HANDLING_h */
