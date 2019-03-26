//
//  ErrorHandling.h
//
//  Handling dynamic memory alloc errors and file write/read errors
//
//  Created by Minxing on 2019/3/21.
//

#ifndef ERROR_HANDLING_h
#define ERROR_HANDLING_h

#ifdef __cplusplus
extern "C"{
#endif
    void report_error_malloc_space();
    void report_error_read_file();
    void report_error_write_file();
    void report_error_make_dir();
#ifdef __cplusplus
}
#endif

#endif /* ERROR_HANDLING_h */
